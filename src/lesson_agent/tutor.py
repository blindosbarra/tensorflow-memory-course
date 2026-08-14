"""The doubt channel: a conversational tutor grounded in one lesson.

This is the piece the original design had no answer for. The five-agent
`Workflow` is a one-shot document generator — you point it at a notebook and
it emits a page. There was no way to say *"I don't understand why the join
happens before the writer"* and get an answer, which is most of what a
learner actually needs.

`TutorSession` is a single ADK `Agent` (no `output_schema` — the answer is
markdown prose, not a record to render mechanically) running against a
persistent ADK session. Two consequences worth stating:

- **The conversation is real.** ADK keeps prior turns in the session's
  contents, so follow-ups like "and why does that matter?" resolve against
  what was just said. The GUI keeps one `TutorSession` per lesson in
  `st.session_state`, so switching lessons and coming back keeps the thread.
- **It is grounded, not general.** `{lesson_context}` seeds the notebook's
  cells, real outputs, doc page and verified sources into session state, and
  the instruction forbids answering from outside that material without
  labelling it. A tutor that silently invents a plausible answer about the
  learner's own course is worse than one that says "the notebook doesn't
  cover this".
"""

from __future__ import annotations

from dataclasses import dataclass, field
import uuid

from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

from lesson_agent.agents import MODEL
from lesson_agent.profile import LearnerProfile
from lesson_agent.read_notebook import LessonContext, format_context_for_agent

APP_NAME = "lesson-tutor"
USER_ID = "learner"

TUTOR_INSTRUCTION = (
    "Sei il tutor personale di uno studente che sta seguendo il corso "
    "'TensorFlow Memory AI Lab'. Lo studente sta studiando la lezione il cui "
    "materiale completo trovi qui sotto, e ti fa domande su cio' che non ha "
    "capito.\n\n"
    "Regole non negoziabili:\n\n"
    "- Rispondi **basandoti sul materiale della lezione qui sotto**: le celle, "
    "gli output reali che il notebook ha stampato, la pagina del corso e le "
    "fonti verificate. Quando citi un numero, dev'essere un numero che "
    "compare davvero nel materiale.\n"
    "- Se la domanda riguarda qualcosa che questa lezione non copre, dillo "
    "chiaramente in una riga, poi rispondi comunque con le tue conoscenze "
    "generali marcando la risposta come 'fuori dal materiale della lezione'. "
    "Non spacciare mai conoscenza generale per contenuto del corso.\n"
    "- Se lo studente ha un'idea sbagliata, correggila esplicitamente invece "
    "di aggirarla con una risposta educata.\n"
    "- Rispondi in italiano, in markdown. Per le formule usa LaTeX fra `$$` "
    "(display) o `\\(...\\)` (inline).\n"
    "- Chiudi con **una** domanda di controllo che verifichi se lo studente "
    "ha capito, solo se la risposta era concettuale; non farlo per domande "
    "puramente pratiche ('dove sta questa funzione?').\n\n"
    "{learner_profile}\n\n"
    "## Materiale della lezione\n{lesson_context}"
)


def build_tutor_agent() -> Agent:
    """The tutor agent. Free-text output: this is a conversation, not a record."""

    return Agent(
        name="tutor_agent",
        model=MODEL,
        instruction=TUTOR_INSTRUCTION,
    )


@dataclass
class TutorTurn:
    """One exchange, kept for rendering the chat transcript in the GUI."""

    question: str
    answer: str


@dataclass
class TutorSession:
    """A live, per-lesson conversation with the tutor.

    Construct with `TutorSession.create(...)`, not directly: the ADK session
    has to exist (and be seeded) before the first question, and that is an
    async call.
    """

    lesson_id: str
    runner: InMemoryRunner
    session_id: str
    turns: list[TutorTurn] = field(default_factory=list)

    @classmethod
    async def create(cls, context: LessonContext, profile: LearnerProfile) -> TutorSession:
        runner = InMemoryRunner(agent=build_tutor_agent(), app_name=APP_NAME)
        # A fresh id per TutorSession: reusing `lesson-<id>` would silently
        # resume a stale conversation seeded with an older learner profile.
        session_id = f"tutor-{context.lesson_id}-{uuid.uuid4().hex[:8]}"
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state={
                "lesson_context": format_context_for_agent(context),
                "learner_profile": profile.briefing(),
            },
        )
        return cls(lesson_id=context.lesson_id, runner=runner, session_id=session_id)

    async def ask(self, question: str) -> str:
        """Send one question and return the tutor's full answer.

        Collects only final (non-partial) model text: ADK may emit streaming
        chunks with `partial=True` followed by the aggregated event, and
        concatenating both would duplicate the answer.
        """

        chunks: list[str] = []
        async for event in self.runner.run_async(
            user_id=USER_ID,
            session_id=self.session_id,
            new_message=types.UserContent(parts=[types.Part(text=question)]),
        ):
            if event.partial or not event.content or not event.content.parts:
                continue
            if event.author == USER_ID:
                continue
            for part in event.content.parts:
                if part.text:
                    chunks.append(part.text)

        answer = "".join(chunks).strip() or (
            "(Il tutor non ha prodotto testo. Riprova, o riformula la domanda.)"
        )
        self.turns.append(TutorTurn(question=question, answer=answer))
        return answer
