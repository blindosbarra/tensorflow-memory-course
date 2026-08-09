"""Guard the notebook source text against corruption no other gate can see.

On 2026-08-09 an iteration deepening lesson 40 wrote `\\right)` into a markdown
cell through a layer that interpreted the escape, leaving a literal carriage
return followed by `ight)`; `\\alpha` became a BEL character followed by `lpha`.
The formula for the LoRA forward pass rendered broken, in the lesson whose whole
point is the alpha/r scaling factor.

Every gate passed. `execute_notebooks.py` runs code cells, and these were
markdown, so 61/61 held. `nbformat.validate` passed because the JSON is
well-formed. `mkdocs build --strict` builds `docs/modules/`, not notebooks. The
whole battery is blind to what the student actually reads, which is why this
lives in pytest: it costs nothing, needs no ml extra, and runs on every
iteration.

See section 4.3 of reports/SDD-remediation-2026-08-06.md for the editing
mechanics that make this class of damage easy to cause and hard to notice.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

import pytest

NOTEBOOKS = sorted((Path(__file__).resolve().parents[1] / "notebooks").glob("*.ipynb"))

# Everything below 0x20 except tab and newline: those two are the only control
# characters a notebook source line has any reason to contain.
FORBIDDEN = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")

# The two seen in the wild, with the escape each one came from.
LIKELY_CAUSE = {
    "\r": r"\r — probably a mangled \right, \rho or \rangle",
    "\x07": r"\a — probably a mangled \alpha or \angle",
    "\x08": r"\b — probably a mangled \beta or \bar",
    "\x0c": r"\f — probably a mangled \frac or \forall",
    "\x0b": r"\v — probably a mangled \vec or \varphi",
}


def test_notebooks_exist() -> None:
    """A silent empty glob would make every other test in this file vacuous."""

    assert NOTEBOOKS, "nessun notebook trovato: il test passerebbe a vuoto"


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda p: p.name)
def test_no_control_characters_in_source(notebook: Path) -> None:
    """No notebook source line may carry a stray control character."""

    cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
    damage: list[str] = []
    for index, cell in enumerate(cells):
        for line_number, line in enumerate(cell.get("source") or []):
            for match in FORBIDDEN.finditer(line):
                char = match.group()
                cause = LIKELY_CAUSE.get(char, "escape interpretato per errore")
                damage.append(
                    f"  cella {index}, riga {line_number}, colonna {match.start()}: "
                    f"{char!r} ({cause})\n"
                    f"    {line!r}"
                )

    assert not damage, (
        f"{notebook.name} contiene caratteri di controllo nel testo sorgente.\n"
        + "\n".join(damage)
        + "\n\nQuasi sempre significa che una sequenza LaTeX e' stata scritta "
        "attraverso uno strato che ne ha interpretato l'escape: '\\right' "
        "diventa CR + 'ight', '\\alpha' diventa BEL + 'lpha'. Nessun altro gate "
        "lo vede, perche' le celle markdown non vengono eseguite. Vedi la "
        "sezione 4.3 della SDD per come editare i notebook senza causarlo."
    )
