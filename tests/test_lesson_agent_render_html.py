"""Unit tests for `lesson_agent.render_html` — no LLM call, no API key needed."""

from __future__ import annotations

from pathlib import Path

from lesson_agent.read_notebook import LessonContext, NotebookCell
from lesson_agent.render_html import (
    ChartSeries,
    extract_numeric_series,
    render_html,
    write_lesson_html,
)
from lesson_agent.schemas import DocSection, ValidationFinding, ValidatorOutput, WriterOutput


def _context(cells: tuple[NotebookCell, ...], evidence=None) -> LessonContext:
    return LessonContext(
        lesson_id="fake-lesson",
        notebook_path=Path("notebooks/lezione-99-fake.ipynb"),
        doc_path=Path("docs/modules/fake-lesson.md"),
        doc_frontmatter={"sources": ["https://example.org/paper"]},
        doc_body="body",
        cells=cells,
        evidence=evidence,
    )


def _writer() -> WriterOutput:
    return WriterOutput(
        title="Titolo di prova",
        sections=[
            DocSection(heading="Teoria", body_markdown="Un **punto** importante."),
            DocSection(heading="Codice", body_markdown="```python\nx = 1\n```"),
        ],
    )


def _validator() -> ValidatorOutput:
    return ValidatorOutput(
        findings=[ValidationFinding(severity="warning", note="controllare la fonte X")],
        overall_assessment="Bozza sostanzialmente corretta.",
    )


def test_extract_numeric_series_finds_list_of_records() -> None:
    cell = NotebookCell(
        cell_type="code",
        source="...",
        output_text='[{"name": "a", "score": 0.5}, {"name": "b", "score": 0.9}]',
    )
    series = extract_numeric_series(_context((cell,)))
    assert series == ChartSeries(field="score", labels=("a", "b"), values=(0.5, 0.9))


def test_extract_numeric_series_none_for_single_record() -> None:
    # lezione-58's actual shape: one dict, not a comparable series.
    cell = NotebookCell(
        cell_type="code",
        source="...",
        output_text='{"memory_id": "mem_001", "importance": 0.42}',
    )
    assert extract_numeric_series(_context((cell,))) is None


def test_extract_numeric_series_none_when_no_json() -> None:
    cell = NotebookCell(cell_type="code", source="...", output_text="pipeline OK\n")
    assert extract_numeric_series(_context((cell,))) is None


def test_extract_numeric_series_ignores_markdown_cells() -> None:
    md_cell = NotebookCell(cell_type="markdown", source="[{\"a\": 1}, {\"a\": 2}]")
    assert extract_numeric_series(_context((md_cell,))) is None


def test_render_html_includes_sections_and_validator_report() -> None:
    ctx = _context((NotebookCell(cell_type="code", source="x", output_text="ok"),))
    out = render_html(ctx, _writer(), _validator())

    assert "<title>Titolo di prova</title>" in out
    assert "<h2>Teoria</h2>" in out
    assert "<strong>punto</strong>" in out  # markdown was converted to HTML
    assert "<h2>Codice</h2>" in out
    assert "controllare la fonte X" in out
    assert "Bozza sostanzialmente corretta." in out
    assert "https://example.org/paper" in out
    assert "<!doctype html>" in out.lower()


def test_render_html_embeds_chart_when_series_found() -> None:
    cell = NotebookCell(
        cell_type="code",
        source="...",
        output_text='[{"name": "a", "score": 0.5}, {"name": "b", "score": 0.9}]',
    )
    ctx = _context((cell,))
    out = render_html(ctx, _writer(), _validator())
    assert "data:image/png;base64," in out


def test_render_html_no_chart_section_without_series() -> None:
    cell = NotebookCell(cell_type="code", source="...", output_text="ok")
    ctx = _context((cell,))
    out = render_html(ctx, _writer(), _validator())
    assert "data:image/png;base64," not in out


def test_render_html_escapes_untrusted_text() -> None:
    ctx = _context((NotebookCell(cell_type="code", source="x", output_text="ok"),))
    writer = WriterOutput(title="<script>alert(1)</script>", sections=[])
    out = render_html(ctx, writer, _validator())
    assert "<script>alert(1)</script>" not in out
    assert "&lt;script&gt;" in out


def test_write_lesson_html_writes_to_slug_named_file(tmp_path) -> None:
    ctx = _context((NotebookCell(cell_type="code", source="x", output_text="ok"),))
    path = write_lesson_html(ctx, _writer(), _validator(), output_dir=tmp_path)
    assert path == tmp_path / "fake-lesson.html"
    assert path.exists()
    assert "Titolo di prova" in path.read_text(encoding="utf-8")
