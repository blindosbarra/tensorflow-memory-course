# SDD — Interactive lesson-companion agent (Google ADK, multi-agent)

Status as of 2026-08-11: **design + API research complete, no code written
yet.** This document is the handover for whoever resumes tomorrow (a fresh
session with no memory of this conversation).

This is a **new feature track, independent of the remediation queue**
(`reports/handover/queue.yaml`, `reports/SDD-remediation-2026-08-06.md`,
`reports/handover/AGENT_LOOP.md`, WI-1..WI-15). Do **not** add this work to
`queue.yaml`: that file is polled by `scripts/next_work_item.py` for the
autonomous remediation loop, which expects notebook/doc fixes against the
existing WI list — an ADK multi-agent subsystem would confuse it. Track this
feature's own progress in this document instead, and update it at the end
of every session (like `queue.yaml`'s `notes`, but for this track).

---

## 1. What was asked

The course (`notebooks/`, 61 lessons) is theory-heavy. The user wants an
agent that accompanies each lesson: it prepares the standard lesson
documentation (theory, math, explanations), and the user then interacts
with it — asking it to add information or go deeper on specific points.
The agent must produce a set of HTML pages and charts explaining the
lesson tied to each notebook.

## 2. Decisions made this session (do not re-litigate)

Asked and answered via `AskUserQuestion`, in order:

1. **Agent framework:** not a Claude Code skill/subagent — the user
   explicitly asked for **Google ADK (Agent Development Kit) 2.x**, with a
   **multi-agent architecture**, naming five roles:
   1. an agent that **writes the output document**,
   2. an agent that **gathers information** and builds the content,
   3. an agent that **technically validates** the content,
   4. an agent focused on the **math**,
   5. an agent focused on the **Python code**, to help the user understand it.
2. **Output destination:** HTML + charts, **committed to the repo** (not
   published as ephemeral Artifacts).
3. **Initial scope:** build the tool first and validate it on 1-2 lessons
   on demand — do **not** batch-generate all 61 lessons yet.
4. **LLM backend:** **Google AI Studio** (`GOOGLE_API_KEY` env var), not
   Vertex AI. No GCP project exists in this repo for this purpose today.
   The key is provided by the user **outside the chat** (e.g. `!export
   GOOGLE_API_KEY=...` in this session, or a git-ignored `.env`) — never
   paste a key into the conversation, and never commit one.
5. **Model:** the user asked for "the most recent Gemini Flash" for **all
   five** agents (not the flash/pro split I offered). Verified against
   `ai.google.dev/gemini-api/docs/models` on 2026-08-11: the current
   stable, recommended general-purpose Flash model is **`gemini-3.6-flash`**.
   Put this string in exactly one place (a constants module) so bumping it
   later is a one-line change — model names move fast and this will be
   stale again within months.

## 3. Environment state

- `google-adk` **2.6.3** was installed for exploration with
  `uv pip install google-adk --python .venv` — this was **not** added to
  `pyproject.toml`, so it will vanish on a fresh `uv sync`. Tomorrow's
  first step is to add it properly (see §6).
- Network egress confirmed reachable from this sandbox: `pypi.org` (200)
  and `generativelanguage.googleapis.com` (404 on `/`, i.e. TLS+DNS work —
  a real request needs the API key) both responded.
- No `GOOGLE_API_KEY` is set in this environment yet.
- Confirmed by grepping the repo: there is **no existing** Vertex AI/ADK/
  Gemini-API integration anywhere in `src/`, `scripts/`, or config. The
  hits for "Vertex AI" etc. are all course *content* (the PMLE module
  teaches Vertex AI conceptually) — nothing to reconcile with, this is
  greenfield.

## 4. ADK API, verified against the installed source (not doc pages)

Early research via `WebFetch` on `ai.google.dev`/`adk.dev`/GitHub-raw pages
gave **inconsistent** answers about the current API (small fetch-model
summaries contradicted each other, e.g. on whether `Event.is_final_response()`
exists). Do not trust those summaries. Instead `google-adk` was installed
into `.venv` and its source read directly
(`.venv/lib/python3.12/site-packages/google/adk/`). These facts are
confirmed against **2.6.3** source, line references below:

- Top-level exports (`google/adk/__init__.py`): `Agent`, `Context`,
  `Event`, `Runner`, `Workflow`. **`InMemoryRunner` is not re-exported at
  top level** — import it from `google.adk.runners`:
  `from google.adk.runners import InMemoryRunner`.
- `Agent` (`google/adk/agents/llm_agent.py`, aliased at top level):
  `Agent(name=..., model=..., instruction=..., tools=[python_functions],
  sub_agents=[...], output_schema=SomePydanticModel)`. Plain Python
  functions can be tools directly (ADK wraps them; docstring becomes the
  tool description, e.g. `contributing/samples/workflows/sequence` in the
  upstream repo).
- `Workflow` (`google/adk/workflow/_workflow.py:145`) — **`class
  Workflow(BaseNode)`**, not a `BaseAgent`. This matters for how you hand
  it to the runner (next point). Built with:
  `Workflow(name=..., edges=[("START", node1, node2, ...)])` — a
  deterministic sequential graph. A node in the tuple can be a plain
  Python function or an `Agent`; output of one node becomes the input of
  the next automatically.
  - **Fan-out/fan-in:** an edge element can itself be a tuple of nodes,
    e.g. `("START", (math_node, code_node), join_node, next_node)` runs
    `math_node` and `code_node` in parallel; `JoinNode(name=...)` (from
    `google.adk.workflow`) collects their results into a `dict` keyed by
    each node's name, which the next function receives as its single
    argument.
  - `google.adk.workflow` also exports `FunctionNode`, `Node`/`node`
    (decorator), `RetryConfig`, `NodeTimeoutError`, `DEFAULT_ROUTE`,
    `Edge` — not yet explored in depth, only `Workflow`/`JoinNode` were
    needed for the plan in §5.
- `InMemoryRunner.__init__` (`google/adk/runners.py:2295`) takes
  `agent: Optional[BaseAgent]` **and separately** `node: Any = None`.
  Since `Workflow` is a `BaseNode`, not a `BaseAgent`, **pass it as
  `InMemoryRunner(node=my_workflow)`**, not `agent=`.
- **Sessions are not auto-created.** `Runner.__init__` has
  `auto_create_session: bool = False` (`runners.py:214`), and
  `InMemoryRunner.__init__` does **not** forward or expose this flag — it
  is hard-set to the base default. `run_async` calls
  `_get_or_create_session` (`runners.py:913`), which raises
  `SessionNotFoundError` if the session doesn't exist and
  `auto_create_session` is `False`. **You must create the session
  yourself first:**
  ```python
  await runner.session_service.create_session(
      app_name=runner.app_name, user_id=user_id, session_id=session_id,
  )
  ```
- Running and reading the result (`runners.py:1023` `run_async`, or the
  sync wrapper `run` at `runners.py:955` for a quick script):
  ```python
  from google.genai import types

  async for event in runner.run_async(
      user_id=user_id,
      session_id=session_id,
      new_message=types.UserContent(parts=[types.Part(text=prompt)]),
  ):
      if event.is_final_response() and event.content and event.content.parts:
          text = "".join(p.text for p in event.content.parts if p.text)
  ```
  `Event.is_final_response()` **does** exist
  (`google/adk/events/event.py:276`) — an earlier WebFetch summary that
  claimed otherwise was wrong; verified by reading the method body.
  `Event.node_name` (`event.py:263`) identifies which node in a `Workflow`
  produced a given event — useful for picking out one specific node's
  output (e.g. the final `render_html` node) when multiple nodes ran.

## 5. Proposed pipeline (design only — not implemented)

One run = one notebook (`notebooks/lezione-NN-*.ipynb`) in, one
self-contained HTML file out. Six nodes, wired as a `Workflow`:

1. **`read_notebook`** (plain function, no LLM) — parses the target
   notebook's markdown + code cells, pulls the matching
   `docs/modules/*.md` summary page and the matching
   `knowledge/<topic>/evidence.yaml` research pack, and produces one
   structured context blob. Fully unit-testable without any API key.
2. **`gather_info_agent`** (LLM) — role 2 from §2. Reads the context blob,
   produces an information brief: theory points, key facts, which sources
   back which claim.
3. **fan-out** to **`math_agent`** and **`code_agent`** (LLM, parallel) —
   roles 4 and 5. `math_agent` explains the formulas present in the lesson
   (LaTeX); `code_agent` walks the notebook's Python cells concept by
   concept for the reader.
4. **`JoinNode`** → **`writer_agent`** (LLM) — role 1. Drafts the
   structured lesson document (theory + math + code explanation sections)
   from the three upstream outputs.
5. **`validator_agent`** (LLM) — role 3. Technically reviews the draft
   against the notebook's actual code/printed output and the
   `evidence.yaml` sources; flags inaccuracies.
   **v1 decision: report-only** — it appends a validation section to the
   document rather than looping the writer for automatic revision. Keeps
   the first version simple, deterministic, and inspectable. An
   LLM-judge/retry loop is a plausible v2, not now.
6. **`render_html`** (plain function, no LLM) — assembles the writer's
   sections + the validator's report into one self-contained HTML file,
   with charts (matplotlib, following the `dataviz` skill's guidance —
   load it before writing any chart code) built from data actually present
   in the notebook where possible (real printed metrics) rather than
   decorative filler. Writes to
   `docs/lezioni-interattive/lezione-NN.html` (proposed path — confirm
   naming against `docs/modules/` conventions before implementing) and
   commits it like any other repo file.

Not decided yet, resolve while implementing:
- Whether `math_agent`/`code_agent`/`writer_agent` return plain text or a
  Pydantic `output_schema` (structured output is more reliable for
  `render_html` to consume mechanically — leans toward yes, but adds a
  schema per agent to design).
- Exact instructions/system prompt for each of the 5 agents — none
  written yet.
- Exact repo layout: proposal is `src/lesson_agent/` (mirrors
  `src/memory_ai/`'s package convention) with a CLI entry point
  `scripts/generate_lesson_doc.py <lezione-id>`, but this wasn't checked
  against `pyproject.toml`'s `[tool.hatch.build.targets.wheel] packages`
  list (currently only `src/memory_ai`) — would need a second package
  entry, or nest under `src/memory_ai/` some other way; pick one
  deliberately, don't default silently.
- Whether this needs its own test suite under `tests/` (the repo's `pytest`
  gate runs `tests/` unconditionally — an ADK agent test that makes a real
  Gemini API call would make `uv run pytest` flaky/networked/costly unless
  mocked or explicitly excluded; decide this before adding any test that
  touches the LLM).

## 6. Resume checklist for tomorrow

1. Add `google-adk` as a new optional-dependency group in
   `pyproject.toml` (pattern already exists for `ml`), e.g.:
   ```toml
   [project.optional-dependencies]
   lesson-agent = ["google-adk>=2.6"]
   ```
   then `uv sync --extra lesson-agent` (regenerates `uv.lock`).
2. Set `GOOGLE_API_KEY` in the shell (user-provided, outside any committed
   file) before attempting a real run.
3. Decide the two open layout questions in §5 (package location, test
   strategy) — they're cheap to decide once, expensive to redo after code
   exists.
4. Implement `read_notebook` and `render_html` first — they need no API
   key and are the easiest to get right and test in isolation.
5. Write the three simplest agent instructions (`gather_info_agent`,
   `math_agent`, `code_agent`) and wire the `Workflow` through step 4 of
   §5 (the `JoinNode`); confirm one real end-to-end LLM call works before
   adding `writer_agent`/`validator_agent` on top.
6. Validate end to end on **one** lesson before generalizing — lezione-58
   is a reasonable first target (already deeply familiar from WI-13,
   small, and its `MemoryAILab` assembly is a good test of the code/math
   agents against real content).
7. Only after a human has looked at that one generated HTML page and is
   happy with it, decide whether/how to batch the rest.

## 7. Change log

- **2026-08-11** — Initial write-up. Requirements gathered via
  `AskUserQuestion` (§2), ADK API verified against installed source (§4),
  pipeline designed (§5). No code written.
