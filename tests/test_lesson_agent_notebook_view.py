"""Tests for `lesson_agent.notebook_view` — the read-only notebook renderer."""

from __future__ import annotations

import base64
import json

import pytest

from lesson_agent import notebook_view
from lesson_agent.read_notebook import NOTEBOOKS_DIR

# A 1x1 transparent PNG, base64 — the smallest valid thing to assert on.
_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


def _write_notebook(path, cells) -> None:
    path.write_text(
        json.dumps(
            {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
        ),
        encoding="utf-8",
    )


def test_reads_real_course_notebook() -> None:
    cells = notebook_view.read_view_cells(
        NOTEBOOKS_DIR / "lezione-58-capstone-pipeline.ipynb"
    )
    assert cells
    assert {cell.cell_type for cell in cells} <= {"markdown", "code"}
    # 1-based and contiguous: the numbers are shown to the learner and used
    # in the "chiedi al tutor della cella N" prompt.
    assert [cell.index for cell in cells] == list(range(1, len(cells) + 1))


def test_images_survive_as_decodable_png(tmp_path) -> None:
    """`read_notebook` reduces figures to a boolean; here the learner sees them."""

    path = tmp_path / "nb.ipynb"
    _write_notebook(
        path,
        [
            {
                "cell_type": "code",
                "source": "plt.plot(x, y)",
                "outputs": [
                    {
                        "output_type": "display_data",
                        "data": {"image/png": _PNG_B64, "text/plain": "<Figure>"},
                    }
                ],
                "metadata": {},
                "execution_count": 1,
            }
        ],
    )
    (cell,) = notebook_view.read_view_cells(path)
    (output,) = cell.outputs
    assert output.kind == "image"
    assert base64.b64decode(output.image_base64)[:8] == b"\x89PNG\r\n\x1a\n"


def test_errors_are_distinguished_from_stdout(tmp_path) -> None:
    path = tmp_path / "nb.ipynb"
    _write_notebook(
        path,
        [
            {
                "cell_type": "code",
                "source": "1 / 0",
                "outputs": [
                    {"output_type": "stream", "name": "stdout", "text": "prima\n"},
                    {
                        "output_type": "error",
                        "ename": "ZeroDivisionError",
                        "evalue": "division by zero",
                        "traceback": ["Traceback...", "ZeroDivisionError"],
                    },
                ],
                "metadata": {},
                "execution_count": 1,
            }
        ],
    )
    (cell,) = notebook_view.read_view_cells(path)
    assert cell.has_error
    assert [output.kind for output in cell.outputs] == ["text", "error"]


def test_empty_and_raw_cells_are_skipped(tmp_path) -> None:
    path = tmp_path / "nb.ipynb"
    _write_notebook(
        path,
        [
            {"cell_type": "raw", "source": "non renderizzata", "metadata": {}},
            {"cell_type": "markdown", "source": "   ", "metadata": {}},
            {"cell_type": "markdown", "source": "# Titolo", "metadata": {}},
        ],
    )
    (cell,) = notebook_view.read_view_cells(path)
    assert cell.source == "# Titolo"
    assert cell.index == 1


@pytest.mark.parametrize("limit", [10, 600])
def test_cell_excerpt_never_exceeds_its_limit(limit: int) -> None:
    cell = notebook_view.ViewCell(index=1, cell_type="code", source="x = 1\n" * 500)
    excerpt = notebook_view.cell_excerpt(cell, limit=limit)
    assert len(excerpt) <= limit + 2  # the appended "\n…"
