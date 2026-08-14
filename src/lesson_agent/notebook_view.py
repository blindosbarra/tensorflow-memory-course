"""Notebook cells prepared for on-screen reading, images included.

`read_notebook.NotebookCell` exists to feed an LLM: it flattens outputs to
text and reduces a matplotlib figure to `has_figure=True`, because embedding
a PNG in a prompt would cost context for something a text model can't read.
The GUI has the opposite need — the learner *should* see the plot — so this
module re-reads the notebook keeping the image bytes, and adds the small
things a reader wants that a prompt doesn't: cell numbering, error outputs
kept distinct from normal stdout, and a per-cell anchor the tutor can be
pointed at ("spiegami la cella 7").

Kept separate from `read_notebook` rather than bolted onto it so the LLM
path stays exactly as cheap as it was.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from pathlib import Path

from typing import Any

from lesson_agent.read_notebook import _cell_text, read_notebook_json


@dataclass(frozen=True)
class CellOutput:
    """One rendered output of a code cell."""

    kind: str  # "text" | "image" | "error"
    text: str = ""
    image_base64: str = ""


@dataclass(frozen=True)
class ViewCell:
    """One notebook cell, ready to render."""

    index: int  # 1-based, counting only code+markdown cells (what the reader sees)
    cell_type: str  # "markdown" | "code"
    source: str
    outputs: tuple[CellOutput, ...] = field(default_factory=tuple)

    @property
    def is_empty(self) -> bool:
        return not self.source.strip()

    @property
    def has_error(self) -> bool:
        return any(out.kind == "error" for out in self.outputs)


def _outputs_for(cell: dict[str, Any]) -> tuple[CellOutput, ...]:
    outputs: list[CellOutput] = []
    for out in cell.get("outputs", []):
        kind = out.get("output_type")
        if kind == "stream":
            text = _cell_text(out.get("text", ""))
            if text.strip():
                outputs.append(CellOutput("text", text=text))
        elif kind == "error":
            # Kept separate from stdout: a traceback in a lesson notebook is
            # either intentional (demonstrating a failure) or a broken cell,
            # and the reader needs to be able to tell at a glance.
            traceback = "\n".join(out.get("traceback") or [])
            outputs.append(
                CellOutput(
                    "error",
                    text=traceback or f"{out.get('ename', '')}: {out.get('evalue', '')}",
                )
            )
        elif kind in ("execute_result", "display_data"):
            data = out.get("data", {})
            if "image/png" in data:
                png = data["image/png"]
                # nbformat gives base64 already for image/png in v4 JSON.
                image = png if isinstance(png, str) else base64.b64encode(png).decode("ascii")
                outputs.append(CellOutput("image", image_base64=image.replace("\n", "")))
            elif "text/plain" in data:
                outputs.append(CellOutput("text", text=_cell_text(data["text/plain"])))
    return tuple(outputs)


def read_view_cells(notebook_path: Path) -> tuple[ViewCell, ...]:
    """Read a notebook into displayable cells, skipping empty and `raw` ones."""

    notebook = read_notebook_json(notebook_path)
    cells: list[ViewCell] = []
    index = 0
    for cell in notebook["cells"]:
        cell_type = cell["cell_type"]
        if cell_type not in ("markdown", "code"):
            continue
        source = _cell_text(cell.get("source", ""))
        if not source.strip():
            continue
        index += 1
        cells.append(
            ViewCell(
                index=index,
                cell_type=cell_type,
                source=source,
                outputs=_outputs_for(cell) if cell_type == "code" else (),
            )
        )
    return tuple(cells)


def cell_excerpt(cell: ViewCell, limit: int = 600) -> str:
    """A short quote of a cell, for pre-filling a question to the tutor."""

    source = cell.source.strip()
    if len(source) <= limit:
        return source
    return source[:limit].rstrip() + "\n…"
