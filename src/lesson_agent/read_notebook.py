"""Gather one lesson's notebook, doc page, and evidence pack into one context blob.

This is the first node of the lesson-agent `Workflow` (see
`reports/SDD-lesson-agent-2026-08-11.md` section 5) and the only one that
touches the filesystem instead of an LLM: everything here is deterministic
and unit-testable without a `GOOGLE_API_KEY`.

Why the doc page is found via `deliverables:`, not by parsing the notebook
filename: notebook numbering (`lezione-NN-<slug>.ipynb`) and doc slugs
(`docs/modules/<slug>.md`) drifted apart over the course's history — e.g.
`notebooks/lezione-06-numpy.ipynb` documents lesson `python-numpy-refresh`,
not `numpy`. `docs/modules/*.md` frontmatter's `deliverables:` list is the
one place that names the notebook file explicitly, so it is the source of
truth used here. The doc's `id:` (verified 2026-08-12 to equal every doc's
filename stem, with no exceptions across the whole corpus) then names the
matching `knowledge/<id>/evidence.yaml` pack, if one exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import nbformat
import yaml

NOTEBOOKS_DIR = Path("notebooks")
MODULES_DIR = Path("docs/modules")
KNOWLEDGE_DIR = Path("knowledge")

# The frontmatter block: everything between the first two `---` lines.
_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)", re.S)


@dataclass(frozen=True)
class NotebookCell:
    """One notebook cell, reduced to what the agents need.

    `output_text` concatenates `stream` output and the `text/plain`
    representation of `display_data`/`execute_result` (e.g. a printed JSON
    record, an assertion's stdout). Raw binary output (a matplotlib PNG) is
    represented only by `has_figure`, not embedded — it would bloat the LLM
    context without being readable by a text model anyway.
    """

    cell_type: str  # "markdown" or "code"
    source: str
    output_text: str = ""
    has_figure: bool = False


@dataclass(frozen=True)
class LessonContext:
    """Everything gathered about one lesson, ready to hand to the LLM agents."""

    lesson_id: str
    notebook_path: Path
    doc_path: Path
    doc_frontmatter: dict[str, Any]
    doc_body: str
    cells: tuple[NotebookCell, ...]
    evidence: dict[str, Any] | None  # parsed evidence.yaml, or None if the pack is missing


def _cell_text(value: str | list[str]) -> str:
    """nbformat stores cell source/output text as either a str or a list of lines."""

    return "".join(value) if isinstance(value, list) else value


def _cell_output(cell: dict[str, Any]) -> tuple[str, bool]:
    parts: list[str] = []
    has_figure = False
    for out in cell.get("outputs", []):
        kind = out.get("output_type")
        if kind == "stream":
            parts.append(_cell_text(out.get("text", "")))
        elif kind in ("execute_result", "display_data"):
            data = out.get("data", {})
            if "image/png" in data:
                has_figure = True
            if "text/plain" in data:
                parts.append(_cell_text(data["text/plain"]))
    return "".join(parts), has_figure


def _parse_frontmatter(doc_path: Path) -> tuple[dict[str, Any], str]:
    text = doc_path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{doc_path} has no --- frontmatter block")
    try:
        front = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"{doc_path} frontmatter is not valid YAML: {exc}") from exc
    return front, match.group(2)


def find_lesson_doc(notebook_path: Path, modules_dir: Path = MODULES_DIR) -> Path:
    """Find the docs/modules/*.md page whose `deliverables:` names this notebook."""

    name = notebook_path.name
    for doc_path in sorted(modules_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8")
        if not _FRONTMATTER_RE.match(text):
            continue  # e.g. docs/modules/index.md, a hand-written page with no frontmatter
        front, _ = _parse_frontmatter(doc_path)
        deliverables = front.get("deliverables") or []
        if any(name in deliverable for deliverable in deliverables):
            return doc_path
    raise LookupError(
        f"No {modules_dir}/*.md declares {name!r} in its deliverables list"
    )


def read_lesson_context(
    notebook_path: Path,
    knowledge_dir: Path = KNOWLEDGE_DIR,
    modules_dir: Path = MODULES_DIR,
) -> LessonContext:
    """Read a notebook plus its matching doc page and evidence pack.

    Raises `LookupError` if no doc page declares the notebook as a
    deliverable. A missing `evidence.yaml` is not an error — `evidence`
    is `None` and the downstream agents note the gap instead of citing
    unverified sources.
    """

    doc_path = find_lesson_doc(notebook_path, modules_dir)
    front, body = _parse_frontmatter(doc_path)
    lesson_id = front.get("id", doc_path.stem)

    notebook = nbformat.read(notebook_path, as_version=4)
    cells = []
    for cell in notebook["cells"]:
        source = _cell_text(cell.get("source", ""))
        if cell["cell_type"] == "code":
            output_text, has_figure = _cell_output(cell)
            cells.append(NotebookCell("code", source, output_text, has_figure))
        elif cell["cell_type"] == "markdown":
            cells.append(NotebookCell("markdown", source))
        # other cell types (e.g. "raw") are not used in this course's notebooks

    evidence_path = knowledge_dir / lesson_id / "evidence.yaml"
    evidence = (
        yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
        if evidence_path.exists()
        else None
    )

    return LessonContext(
        lesson_id=lesson_id,
        notebook_path=notebook_path,
        doc_path=doc_path,
        doc_frontmatter=front,
        doc_body=body.strip(),
        cells=tuple(cells),
        evidence=evidence,
    )


def format_context_for_agent(context: LessonContext) -> str:
    """Render a `LessonContext` as one plain-text block for an LLM prompt.

    This is what the agents actually read — not the dataclass itself.
    Seeded into the ADK session's initial state under the `lesson_context`
    key (see `src/lesson_agent/agents.py`), so every agent's `instruction`
    can pull it in via a `{lesson_context}` placeholder.
    """

    parts = [
        f"# Lezione: {context.lesson_id}",
        f"Notebook: {context.notebook_path}",
        "",
        "## Pagina di riferimento del corso",
        context.doc_body,
        "",
        "## Celle del notebook",
    ]
    for cell in context.cells:
        if cell.cell_type == "markdown":
            parts.append(f"--- markdown ---\n{cell.source}")
        else:
            parts.append(f"--- code ---\n{cell.source}")
            if cell.output_text:
                parts.append(f"--- output ---\n{cell.output_text}")
            if cell.has_figure:
                parts.append("(questa cella produce anche un grafico, non incluso qui)")

    if context.evidence:
        parts.append("\n## Fonti verificate (evidence.yaml)")
        for claim in context.evidence.get("claims", []):
            parts.append(
                f"- [{claim.get('status', 'unknown')}] {claim.get('claim', '')} "
                f"(fonte: {claim.get('source_title', '')}, {claim.get('source_url', '')})"
            )
    else:
        parts.append("\n## Fonti verificate (evidence.yaml)\nNessun evidence.yaml per questa lezione.")

    return "\n\n".join(parts)
