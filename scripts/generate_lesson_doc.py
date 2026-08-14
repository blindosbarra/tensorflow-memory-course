"""Generate one lesson's interactive HTML page via the lesson-agent (Google ADK).

Usage:
    uv run python scripts/generate_lesson_doc.py capstone-pipeline
    uv run python scripts/generate_lesson_doc.py lezione-58-capstone-pipeline
    uv run python scripts/generate_lesson_doc.py pca-umap --level avanzato \\
        --focus "perche' UMAP e non t-SNE?"

Most people should use the GUI instead — `uv run streamlit run
app/streamlit_app.py` — which does the same thing with the learner profile,
the tutor and the notebook side by side. This CLI stays for scripted or
batch generation.

Requires the `lesson-agent` extra (`uv sync --extra dev --extra lesson-agent`)
and a `GOOGLE_API_KEY`, from the environment or from a git-ignored `.env` at
the repo root (see `src/lesson_agent/settings.py`). The key is never read
from a committed file.

What this does, in order (see `src/lesson_agent/agents.py` for why steps 1
and 3 are plain Python, not `Workflow` nodes):

1. `read_lesson_context` — parse the notebook + its doc page + its evidence
   pack (no LLM call).
2. `run_lesson_pipeline` — the five-agent ADK `Workflow` (gather_info ->
   math/code in parallel -> writer -> validator), with the lesson, the
   learner profile and the learner's doubt seeded into session state.
3. `write_lesson_html` — render the writer's draft + validator's report to
   `docs/lezioni-interattive/<lesson_id>.html` (no LLM call).

By default the profile is whatever `.learner/profile.json` holds (i.e. what
you set in the GUI), so CLI and GUI produce the same document for the same
person. `--level`/`--depth` override it for one run without saving.
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import replace
from pathlib import Path
import sys

from lesson_agent.profile import Depth, LearnerProfile, Level, load_profile
from lesson_agent.read_notebook import NOTEBOOKS_DIR, read_lesson_context
from lesson_agent.runner import run_lesson_pipeline
from lesson_agent.settings import api_key, model_name


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


def resolve_profile(args: argparse.Namespace) -> LearnerProfile:
    """The saved profile, with any per-run CLI overrides applied on top."""

    profile = load_profile()
    if args.level:
        profile = replace(profile, level=Level(args.level))
    if args.depth:
        profile = replace(profile, depth=Depth(args.depth))
    return profile


async def generate_lesson_doc(
    notebook_identifier: str,
    profile: LearnerProfile,
    focus: str = "",
) -> Path:
    context = read_lesson_context(resolve_notebook_path(notebook_identifier))
    result = await run_lesson_pipeline(
        context,
        profile,
        focus=focus,
        on_progress=lambda label: print(f"  {label}", file=sys.stderr),
    )
    return result.output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "lesson", help="Notebook filename, stem, or lesson slug (e.g. capstone-pipeline)"
    )
    parser.add_argument(
        "--focus",
        default="",
        help="A specific doubt to put at the centre of the document.",
    )
    parser.add_argument(
        "--level",
        choices=[level.value for level in Level],
        help="Override the saved profile's level for this run only.",
    )
    parser.add_argument(
        "--depth",
        choices=[depth.value for depth in Depth],
        help="Override the saved profile's depth for this run only.",
    )
    args = parser.parse_args()

    if not api_key():
        print(
            "GOOGLE_API_KEY non impostata. Esportala nella shell, mettila in "
            "un `.env` git-ignored alla radice del repo, oppure incollala nel "
            "pannello Impostazioni della GUI.",
            file=sys.stderr,
        )
        return 2

    profile = resolve_profile(args)
    print(f"Modello: {model_name()} · livello: {profile.level.value}", file=sys.stderr)

    output_path = asyncio.run(generate_lesson_doc(args.lesson, profile, args.focus))
    print(f"Scritto: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
