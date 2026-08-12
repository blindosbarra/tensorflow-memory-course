"""Render the writer's draft + validator's report into one self-contained HTML page.

The second (and last) non-LLM node of the lesson-agent `Workflow` (see
`reports/SDD-lesson-agent-2026-08-11.md` section 5) — a pure function of
already-produced data, no API key needed.

Charts come from data the notebook actually printed, not from anything an
LLM said: `extract_numeric_series` looks for a JSON list of same-shaped
records in a code cell's output and, if the notebook doesn't print one (most
lessons show one record or one scalar — not a comparable series), the page
simply has no chart section rather than a decorative one. Colors follow the
`dataviz` skill's reference palette (`references/palette.md`), light mode
only: this is a static page committed to the repo, not an Artifact with a
theme toggle.

Output path: `docs/lezioni-interattive/<lesson_id>.html`, using the lesson's
slug (e.g. `capstone-pipeline`), not the notebook's `lezione-NN` number —
this matches how `docs/modules/*.md` is named, and is stable across the
renumbering that has already happened once in this course's history (see
`read_notebook.py`'s docstring).
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import date
import html as html_module
import io
import json
from pathlib import Path
from typing import Any

import markdown as _markdown
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402 (backend must be set first)

from lesson_agent.read_notebook import LessonContext
from lesson_agent.schemas import ValidatorOutput, WriterOutput

OUTPUT_DIR = Path("docs/lezioni-interattive")

# dataviz skill reference palette (references/palette.md), light mode only.
_SURFACE = "#fcfcfb"
_PRIMARY_INK = "#0b0b0b"
_SECONDARY_INK = "#52514e"
_MUTED_INK = "#898781"
_GRIDLINE = "#e1e0d9"
_BASELINE = "#c3c2b7"
_SERIES_1 = "#2a78d6"  # categorical slot 1 (blue)


@dataclass(frozen=True)
class ChartSeries:
    """A comparable numeric field pulled from a printed list of records."""

    field: str
    labels: tuple[str, ...]
    values: tuple[float, ...]


def extract_numeric_series(context: LessonContext) -> ChartSeries | None:
    """Find the first JSON list of comparable records a code cell printed.

    Returns `None` when nothing qualifies — a single printed record (like
    lezione-58's `MemoryAILab.process` output) is not a series, and this
    function deliberately does not invent one.
    """

    for cell in context.cells:
        if cell.cell_type != "code" or not cell.output_text:
            continue
        records = _find_list_of_records(cell.output_text)
        if records is None:
            continue
        series = _series_from_records(records)
        if series is not None:
            return series
    return None


def _find_list_of_records(text: str) -> list[dict[str, Any]] | None:
    """Scan for the first `[...]` substring that decodes to a list of dicts."""

    decoder = json.JSONDecoder()
    idx = text.find("[")
    while idx != -1:
        try:
            obj, _ = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            idx = text.find("[", idx + 1)
            continue
        if isinstance(obj, list) and len(obj) >= 2 and all(isinstance(x, dict) for x in obj):
            return obj
        idx = text.find("[", idx + 1)
    return None


def _series_from_records(records: list[dict[str, Any]]) -> ChartSeries | None:
    """Pick one numeric field shared by every record, and a label field if one exists.

    Field choice is alphabetical for determinism, not "most interesting" —
    a heuristic here would be a claim this function can't back up.
    """

    common_keys = set(records[0])
    for record in records[1:]:
        common_keys &= set(record)
    numeric_fields = sorted(
        key
        for key in common_keys
        if all(isinstance(r[key], (int, float)) and not isinstance(r[key], bool) for r in records)
    )
    if not numeric_fields:
        return None
    field = numeric_fields[0]
    label_fields = sorted(
        key for key in common_keys if all(isinstance(r[key], str) for r in records)
    )
    label_field = label_fields[0] if label_fields else None
    labels = tuple(str(r[label_field]) if label_field else str(i) for i, r in enumerate(records))
    values = tuple(float(r[field]) for r in records)
    return ChartSeries(field=field, labels=labels, values=values)


def _render_chart_png(series: ChartSeries) -> bytes:
    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=150)
    fig.patch.set_facecolor(_SURFACE)
    ax.set_facecolor(_SURFACE)
    ax.barh(series.labels, series.values, color=_SERIES_1, height=0.6)
    ax.set_title(series.field, color=_PRIMARY_INK, fontsize=11, loc="left")
    ax.tick_params(colors=_SECONDARY_INK, labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(_BASELINE)
    ax.xaxis.grid(True, color=_GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=_SURFACE)
    plt.close(fig)
    return buf.getvalue()


def _markdown_to_html(text: str) -> str:
    return str(_markdown.markdown(text, extensions=["fenced_code", "tables"]))


_STYLE = f"""
body {{
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  background: #f9f9f7;
  color: {_PRIMARY_INK};
  max-width: 820px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  line-height: 1.55;
}}
header {{ border-bottom: 1px solid {_GRIDLINE}; margin-bottom: 1.5rem; padding-bottom: 1rem; }}
header p {{ color: {_SECONDARY_INK}; margin: 0.2rem 0; }}
section {{ margin-bottom: 2rem; }}
h1 {{ font-size: 1.6rem; }}
h2 {{ font-size: 1.2rem; border-bottom: 1px solid {_GRIDLINE}; padding-bottom: 0.3rem; }}
code, pre {{ background: {_SURFACE}; border: 1px solid {_GRIDLINE}; border-radius: 4px; }}
pre {{ padding: 0.75rem; overflow-x: auto; }}
.chart {{ background: {_SURFACE}; border: 1px solid {_GRIDLINE}; border-radius: 6px; padding: 0.5rem; }}
.chart img {{ max-width: 100%; display: block; }}
.validator {{ background: {_SURFACE}; border: 1px solid {_GRIDLINE}; border-radius: 6px; padding: 1rem; }}
.finding {{ margin: 0.4rem 0; }}
.finding .severity {{ font-weight: 600; color: {_MUTED_INK}; text-transform: uppercase;
  font-size: 0.75rem; margin-right: 0.4rem; }}
footer {{ color: {_MUTED_INK}; font-size: 0.85rem; border-top: 1px solid {_GRIDLINE};
  margin-top: 2rem; padding-top: 1rem; }}
"""


def render_html(
    context: LessonContext,
    writer: WriterOutput,
    validator: ValidatorOutput,
    generated_on: date | None = None,
) -> str:
    """Assemble the writer's sections + the validator's report into one HTML page."""

    generated_on = generated_on or date.today()
    title = html_module.escape(writer.title)

    sections_html = "\n".join(
        f"<section><h2>{html_module.escape(s.heading)}</h2>"
        f"{_markdown_to_html(s.body_markdown)}</section>"
        for s in writer.sections
    )

    series = extract_numeric_series(context)
    chart_html = ""
    if series is not None:
        png = _render_chart_png(series)
        b64 = base64.b64encode(png).decode("ascii")
        chart_html = (
            "<section><h2>Dati dal notebook</h2>"
            f'<div class="chart"><img src="data:image/png;base64,{b64}" '
            f'alt="{html_module.escape(series.field)}"></div></section>'
        )

    findings_html = "".join(
        f'<div class="finding"><span class="severity">{html_module.escape(f.severity)}</span>'
        f"{html_module.escape(f.note)}</div>"
        for f in validator.findings
    )
    validator_html = (
        '<section><h2>Validazione</h2><div class="validator">'
        f"<p>{html_module.escape(validator.overall_assessment)}</p>"
        f"{findings_html}</div></section>"
    )

    sources = context.doc_frontmatter.get("sources") or []
    sources_html = "".join(
        f'<li><a href="{html_module.escape(u)}">{html_module.escape(u)}</a></li>' for u in sources
    )

    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{_STYLE}</style>
</head>
<body>
<header>
<h1>{title}</h1>
<p>Lezione: {html_module.escape(context.lesson_id)} &middot; notebook:
{html_module.escape(str(context.notebook_path))}</p>
<p>Generato il {generated_on.isoformat()} dal lesson-agent (Google ADK) &mdash;
non ancora revisionato da un umano.</p>
</header>
{sections_html}
{chart_html}
{validator_html}
<footer><p>Fonti citate nella pagina del corso:</p><ul>{sources_html}</ul></footer>
</body>
</html>
"""


def write_lesson_html(
    context: LessonContext,
    writer: WriterOutput,
    validator: ValidatorOutput,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """Render and write the lesson page to `output_dir/<lesson_id>.html`."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{context.lesson_id}.html"
    output_path.write_text(render_html(context, writer, validator), encoding="utf-8")
    return output_path
