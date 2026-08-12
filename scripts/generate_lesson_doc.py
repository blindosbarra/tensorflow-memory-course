"""Generate one lesson's interactive HTML page via the lesson-agent (Google ADK).

Usage:
    uv run python scripts/generate_lesson_doc.py capstone-pipeline
    uv run python scripts/generate_lesson_doc.py lezione-58-capstone-pipeline

Requires the `lesson-agent` extra (`uv sync --extra lesson-agent`) and a
`GOOGLE_API_KEY` in the environment (Google AI Studio, not Vertex AI — see
`reports/SDD-lesson-agent-2026-08-11.md` section 2.4). The key is never read
from a committed file; export it in the shell before running this script.

What this does, in order (see `src/lesson_agent/agents.py` for why steps 1
and 5 are plain Python, not `Workflow` nodes):

1. `read_lesson_context` — parse the notebook + its doc page + its evidence
   pack (no LLM call).
2. Run the five-agent ADK `Workflow` (gather_info -> math/code in parallel
   -> writer -> validator) with the lesson formatted into the session's
   initial state.
3. `write_lesson_html` — render the writer's draft + validator's report to
   `docs/lezioni-interattive/<lesson_id>.html` (no LLM call).
"""

from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types

from lesson_agent.agents import build_workflow
from lesson_agent.read_notebook import NOTEBOOKS_DIR, format_context_for_agent, read_lesson_context
from lesson_agent.render_html import write_lesson_html
from lesson_agent.schemas import ValidatorOutput, WriterOutput

APP_NAME = "lesson-agent"
USER_ID = "course-author"


def resolve_notebook_path(identifier: str) -> Path:
    """Accept a full notebook filename, its stem, or a bare lesson slug."""

    stem = identifier.removesuffix(".ipynb")
    direct = NOTEBOOKS_DIR / f"{stem}.ipynb"
    if direct.exists():
        return direct

    matches = sorted(NOTEBOOKS_DIR.glob(f"lezione-*-{stem}.ipynb"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(m.name for m in matches)
        raise SystemExit(f"'{identifier}' matches multiple notebooks: {names}")
    raise SystemExit(f"No notebook found for '{identifier}' under {NOTEBOOKS_DIR}/")


async def generate_lesson_doc(notebook_identifier: str) -> Path:
    notebook_path = resolve_notebook_path(notebook_identifier)
    context = read_lesson_context(notebook_path)
    lesson_context_text = format_context_for_agent(context)

    workflow = build_workflow()
    runner = InMemoryRunner(node=workflow, app_name=APP_NAME)
    session_id = f"lesson-{context.lesson_id}"

    await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state={"lesson_context": lesson_context_text},
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=types.UserContent(
            parts=[types.Part(text="Genera la documentazione per questa lezione.")]
        ),
    ):
        if event.node_name:
            print(f"  [{event.node_name}] evento ricevuto", file=sys.stderr)

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

    return write_lesson_html(context, writer, validator)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "lesson", help="Notebook filename, stem, or lesson slug (e.g. capstone-pipeline)"
    )
    args = parser.parse_args()

    if not os.environ.get("GOOGLE_API_KEY"):
        print(
            "GOOGLE_API_KEY non impostata nell'ambiente — impostala prima di eseguire "
            "questo script (vedi il docstring del modulo).",
            file=sys.stderr,
        )
        return 2

    output_path = asyncio.run(generate_lesson_doc(args.lesson))
    print(f"Scritto: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
