"""Unit tests for `lesson_agent.read_notebook` — no LLM call, no API key needed."""

from __future__ import annotations

from pathlib import Path

import pytest

from lesson_agent.read_notebook import find_lesson_doc, read_lesson_context

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
MODULES_DIR = REPO_ROOT / "docs" / "modules"
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"

LEZIONE_58 = NOTEBOOKS_DIR / "lezione-58-capstone-pipeline.ipynb"


def test_find_lesson_doc_matches_by_deliverable() -> None:
    doc_path = find_lesson_doc(LEZIONE_58, modules_dir=MODULES_DIR)
    assert doc_path == MODULES_DIR / "capstone-pipeline.md"


def test_find_lesson_doc_handles_slug_drift() -> None:
    # lezione-06-numpy.ipynb documents python-numpy-refresh, not "numpy" —
    # the doc lookup must go through `deliverables:`, not the filename slug.
    doc_path = find_lesson_doc(
        NOTEBOOKS_DIR / "lezione-06-numpy.ipynb", modules_dir=MODULES_DIR
    )
    assert doc_path == MODULES_DIR / "python-numpy-refresh.md"


def test_find_lesson_doc_raises_for_unknown_notebook() -> None:
    with pytest.raises(LookupError):
        find_lesson_doc(NOTEBOOKS_DIR / "lezione-999-nope.ipynb", modules_dir=MODULES_DIR)


def test_read_lesson_context_lezione_58() -> None:
    ctx = read_lesson_context(
        LEZIONE_58, knowledge_dir=KNOWLEDGE_DIR, modules_dir=MODULES_DIR
    )

    assert ctx.lesson_id == "capstone-pipeline"
    assert ctx.doc_path == MODULES_DIR / "capstone-pipeline.md"
    assert ctx.doc_frontmatter["module"] == "capstone"
    assert "MemoryAILab" in ctx.doc_body

    assert len(ctx.cells) == 7
    assert ctx.cells[0].cell_type == "markdown"
    assert "MemoryAILab" in ctx.cells[0].source

    code_cells = [c for c in ctx.cells if c.cell_type == "code"]
    assert len(code_cells) == 3
    # The cell that prints the JSON record via json.dumps has real stdout.
    printed = [c for c in code_cells if "mem_001" in c.output_text]
    assert len(printed) == 1
    assert '"type": "episodic"' in printed[0].output_text
    assert not printed[0].has_figure

    assert ctx.evidence is not None
    assert ctx.evidence["lesson_id"] == "capstone-pipeline"
    assert len(ctx.evidence["claims"]) == 2


def test_read_lesson_context_missing_evidence_is_none(tmp_path) -> None:
    # A lesson doc with no matching knowledge/<id>/evidence.yaml must not
    # error out — evidence is optional context, not a hard dependency.
    ctx = read_lesson_context(
        LEZIONE_58, knowledge_dir=tmp_path, modules_dir=MODULES_DIR
    )
    assert ctx.evidence is None
