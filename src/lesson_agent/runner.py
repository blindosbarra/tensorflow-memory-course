"""One place that actually runs the five-agent pipeline, for both front-ends.

Before the GUI, this logic lived inside `scripts/generate_lesson_doc.py`.
The Streamlit app needs exactly the same run — same session seeding, same
state checks — plus a progress callback, so it moved here and the CLI became
a thin wrapper. Keeping one copy matters because the seeding is the part
that's easy to get subtly wrong: ADK raises at call time if an
`{placeholder}` in an instruction has no matching state key, so *every* key
an agent mentions must be seeded before the run, including the ones that are
logically optional (`learner_focus` when the learner has no specific doubt).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types

from lesson_agent.agents import build_workflow
from lesson_agent.profile import LearnerProfile
from lesson_agent.read_notebook import LessonContext, format_context_for_agent
from lesson_agent.render_html import write_lesson_html
from lesson_agent.schemas import ValidatorOutput, WriterOutput

APP_NAME = "lesson-agent"
USER_ID = "course-author"

NO_FOCUS = (
    "Lo studente non ha dichiarato un dubbio specifico: copri la lezione in "
    "modo equilibrato."
)

# Shown in the GUI while each node runs. Keys are ADK node names.
NODE_LABELS = {
    "gather_info_agent": "Raccolgo i punti di teoria…",
    "math_agent": "Spiego la matematica…",
    "code_agent": "Spiego il codice…",
    "math_code_join": "Unisco matematica e codice…",
    "writer_agent": "Scrivo il documento…",
    "validator_agent": "Revisione tecnica…",
}


@dataclass(frozen=True)
class LessonDocResult:
    """What a completed pipeline run produced."""

    output_path: Path
    writer: WriterOutput
    validator: ValidatorOutput


def build_initial_state(
    context: LessonContext,
    profile: LearnerProfile,
    focus: str = "",
) -> dict[str, str]:
    """Seed every `{placeholder}` the five agents' instructions reference.

    `learner_focus` gets an explicit sentence rather than an empty string
    when there is no doubt: an empty placeholder reads to the model as a
    truncated prompt, while a sentence that says "no specific doubt" is an
    instruction it can act on.
    """

    return {
        "lesson_context": format_context_for_agent(context),
        "learner_profile": profile.briefing(),
        "learner_focus": focus.strip() or NO_FOCUS,
    }


async def run_lesson_pipeline(
    context: LessonContext,
    profile: LearnerProfile,
    focus: str = "",
    on_progress: Callable[[str], None] | None = None,
    output_dir: Path | None = None,
) -> LessonDocResult:
    """Run gather → (math ∥ code) → writer → validator and write the HTML page.

    `on_progress` is called with a human-readable label each time a node
    emits its first event, which is what drives the GUI's status line. It is
    deliberately a plain callback rather than an async generator: Streamlit
    reruns are synchronous, and a callback is the smaller thing to get right.
    """

    workflow = build_workflow()
    runner = InMemoryRunner(node=workflow, app_name=APP_NAME)
    session_id = f"lesson-{context.lesson_id}"

    await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state=build_initial_state(context, profile, focus),
    )

    seen: set[str] = set()
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=types.UserContent(
            parts=[types.Part(text="Genera la documentazione per questa lezione.")]
        ),
    ):
        name = event.node_name
        if name and name not in seen:
            seen.add(name)
            if on_progress is not None:
                on_progress(NODE_LABELS.get(name, name))

    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    if session is None:
        raise RuntimeError(f"Session {session_id!r} scomparsa dopo la run.")

    missing = {"writer", "validator"} - session.state.keys()
    if missing:
        raise RuntimeError(
            f"Il workflow non ha prodotto {sorted(missing)} nello stato. "
            f"Chiavi presenti: {sorted(session.state.keys())}"
        )

    writer = WriterOutput.model_validate(session.state["writer"])
    validator = ValidatorOutput.model_validate(session.state["validator"])

    kwargs = {"output_dir": output_dir} if output_dir is not None else {}
    output_path = write_lesson_html(context, writer, validator, **kwargs)
    return LessonDocResult(output_path=output_path, writer=writer, validator=validator)
