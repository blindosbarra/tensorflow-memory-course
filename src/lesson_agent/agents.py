"""The five LLM agents and the `Workflow` that wires them together.

Implements section 5's roles 1-5 (see
`reports/SDD-lesson-agent-2026-08-11.md`). `read_notebook`/`render_html`
(roles handled by plain functions, no LLM) live outside this module and
outside the `Workflow` entirely — see the module docstring note below.

## How data actually flows between nodes (reverse-engineered 2026-08-12
from the installed `google-adk==2.6.3` source, since no bundled example
covers this)

An ADK `Workflow` edge only passes the **immediately preceding** node's
return value to the next node, wrapped as a user-role message
(`to_user_content` in `google/adk/utils/content_utils.py`) for an `Agent`
node. That is fine for a strictly linear chain, but this pipeline has
nodes that each need a *different* earlier result (e.g. `validator_agent`
needs both the original lesson text and `writer_agent`'s draft, not just
the draft). ADK's answer to that is **session state**, not the edge chain:

- `LlmAgent.instruction` supports `{state_key}` placeholders, resolved
  from the session's state at call time (`llm_agent.py`, `instruction`
  field docstring).
- Setting `output_key="foo"` on an `Agent` writes its structured output
  (already a plain `dict`, via `output_schema.model_validate_json(...)
  .model_dump()` — see `_llm_agent_wrapper.py:process_llm_agent_output`)
  into `ctx.actions.state_delta["foo"]`, which lands in session state.
- Initial state can be seeded directly at `create_session(state={...})`
  (`sessions/base_session_service.py`).

So every agent below pulls its real input from `{lesson_context}` /
`{info_brief}` / `{math}` / `{code}` / `{writer}` placeholders in its
`instruction`, seeded/written into session state — not from the graph
edge's `node_input`. The edges still matter: they are what makes ADK
actually run `math_agent`/`code_agent` in parallel and wait for both
(`JoinNode`) before `writer_agent`, i.e. they encode *execution order*,
while state carries the *payloads*.

## Why `read_notebook`/`render_html` are not `Workflow` nodes

The original section-5 sketch put all six steps in one `Workflow`. In
practice `LessonContext` (dataclass, `Path` fields, tuples of
`NotebookCell`) is not the kind of value session state is meant to carry,
and neither function needs any ADK machinery — they are plain,
already-tested Python. Splitting them out keeps them exactly as testable
as sections 2/3 of the checklist intended, and makes the `Workflow` here
contain only the five nodes that actually need an LLM. The CLI
(`scripts/generate_lesson_doc.py`) calls `read_lesson_context` before
building the session, and `write_lesson_html` after the run — see that
script for the full pipeline. Decided while implementing (2026-08-12);
not something the SDD anticipated, recorded here since it changes what
"the six-node pipeline" means in practice.
"""

from __future__ import annotations

from google.adk import Agent, Workflow
from google.adk.workflow import JoinNode

from lesson_agent.constants import MODEL
from lesson_agent.schemas import (
    CodeWalkthrough,
    InfoBrief,
    MathExplanation,
    ValidatorOutput,
    WriterOutput,
)

gather_info_agent = Agent(
    name="gather_info_agent",
    model=MODEL,
    instruction=(
        "Sei un tutor che prepara il materiale di una lezione del corso "
        "'TensorFlow Memory AI Lab'. Leggi il materiale della lezione qui sotto "
        "ed estrai i punti di teoria essenziali, in ordine logico. Segnala in "
        "`open_questions` qualunque affermazione del notebook che non sia "
        "supportata da una fonte nella sezione 'Fonti verificate'.\n\n"
        "{lesson_context}"
    ),
    output_schema=InfoBrief,
    output_key="info_brief",
)

math_agent = Agent(
    name="math_agent",
    model=MODEL,
    instruction=(
        "Sei un tutor di matematica per un corso di machine learning. Nel "
        "materiale della lezione qui sotto, individua ogni formula "
        "(esplicita o implicita nel codice, es. una soglia o una funzione di "
        "punteggio) e spiegala in modo che uno studente che sa programmare "
        "ma non ha una formazione matematica avanzata la capisca. Se la "
        "lezione non contiene formule, restituisci una lista vuota in "
        "`formulas_latex` e dillo esplicitamente in `explanation`.\n\n"
        "Usa SEMPRE il valore reale che compare nel codice o nel suo output "
        "(es. il default di un parametro, un numero stampato), mai un "
        "'es.' generico, quando quel valore reale e' disponibile nel "
        "materiale qui sotto — se il codice fissa `soglia=0.4`, scrivi "
        "'qui e' 0.4', non 'ad esempio 0.4'. Se una formula e' gia' stata "
        "insegnata in una lezione precedente (il materiale lo dice), non "
        "riderivarla: nomina la lezione e spiega solo cosa fa QUI, in "
        "questa lezione — non gonfiare l'explanation con un blocco intero "
        "per un fatto banale (es. un bound che viene solo verificato da un "
        "assert, non calcolato).\n\n"
        "{lesson_context}"
    ),
    output_schema=MathExplanation,
    output_key="math",
)

code_agent = Agent(
    name="code_agent",
    model=MODEL,
    instruction=(
        "Sei un tutor di programmazione Python. Nel materiale della lezione "
        "qui sotto, spiega le celle di codice concetto per concetto, per uno "
        "studente che conosce Python ma non necessariamente le librerie "
        "usate. Cita l'output reale delle celle quando è presente, non "
        "inventarne uno.\n\n"
        "{lesson_context}"
    ),
    output_schema=CodeWalkthrough,
    output_key="code",
)

writer_agent = Agent(
    name="writer_agent",
    model=MODEL,
    instruction=(
        "Sei il redattore che assembla la documentazione di una lezione a "
        "partire dal lavoro di tre colleghi. Scrivi un documento con un "
        "titolo e alcune sezioni (almeno: teoria, matematica, codice), "
        "in italiano, in markdown, basandoti SOLO sui contenuti forniti qui "
        "sotto — non aggiungere fatti che non provengono da queste fonti.\n\n"
        "Il notebook contiene gia' celle di teoria scritte da un umano: non "
        "parafrasarle. Il tuo valore aggiunto e' quello che NON c'e' gia' "
        "nel notebook — collega i punti, mostra un esempio concreto con i "
        "valori reali stampati dalle celle di codice (non inventarne), "
        "anticipa una domanda che uno studente farebbe leggendo il codice. "
        "Se una sezione non avrebbe nulla da aggiungere oltre a ripetere il "
        "notebook, tienila breve invece di riempirla di riformulazioni.\n\n"
        "Formatta gli elenchi puntati/numerati con un a-capo reale prima di "
        "ogni voce (`\\n- voce`, non `... : - voce - voce` sulla stessa "
        "riga) — sono liste markdown vere, non prosa con dei trattini.\n\n"
        "## Materiale originale della lezione\n{lesson_context}\n\n"
        "## Brief di teoria\n{info_brief}\n\n"
        "## Spiegazione matematica\n{math}\n\n"
        "## Spiegazione del codice\n{code}"
    ),
    output_schema=WriterOutput,
    output_key="writer",
)

validator_agent = Agent(
    name="validator_agent",
    model=MODEL,
    instruction=(
        "Sei un revisore tecnico. Confronta la bozza qui sotto con il "
        "materiale originale della lezione (codice, output reali, fonti "
        "verificate) e segnala ogni imprecisione, affermazione non "
        "supportata, o numero che non corrisponde a un output reale del "
        "notebook. Questa è una revisione di sola segnalazione: NON "
        "riscrivere la bozza, elenca solo i problemi trovati (o dichiara "
        "che non ce ne sono) e dai una valutazione complessiva breve.\n\n"
        "## Materiale originale della lezione\n{lesson_context}\n\n"
        "## Bozza da revisionare\n{writer}"
    ),
    output_schema=ValidatorOutput,
    output_key="validator",
)


def build_workflow() -> Workflow:
    """Assemble the five agents into the pipeline described in SDD section 5.

    gather_info_agent -> (math_agent, code_agent) in parallel -> join ->
    writer_agent -> validator_agent. The join's own output is unused (see
    module docstring) — it only makes the graph wait for both parallel
    branches before running `writer_agent`.
    """

    join = JoinNode(name="math_code_join")
    return Workflow(
        name="lesson_agent_pipeline",
        edges=[
            (
                "START",
                gather_info_agent,
                (math_agent, code_agent),
                join,
                writer_agent,
                validator_agent,
            ),
        ],
    )
