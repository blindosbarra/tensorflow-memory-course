"""Pydantic `output_schema`s for the five LLM agents.

Decided 2026-08-12 (see `reports/SDD-lesson-agent-2026-08-11.md` section 5):
every agent returns structured output, not free text, so `writer_agent` and
`render_html` can consume upstream results mechanically instead of
re-parsing prose. One class per agent role; `render_html` (the only
consumer outside the agent graph so far) only depends on `WriterOutput` and
`ValidatorOutput`.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class InfoBrief(BaseModel):
    """`gather_info_agent` output: the theory brief the other agents build on."""

    key_points: list[str] = Field(
        description="The lesson's theory points, one claim per item, in the "
        "order they should be explained."
    )
    summary: str = Field(description="A short prose summary of the lesson's theory.")
    open_questions: list[str] = Field(
        default_factory=list,
        description="Anything the notebook asserts without a source, worth "
        "flagging to the validator.",
    )


class MathExplanation(BaseModel):
    """`math_agent` output: the formulas in the lesson, explained."""

    formulas_latex: list[str] = Field(
        default_factory=list, description="Every formula in the lesson, as LaTeX."
    )
    explanation: str = Field(
        description="Markdown walking through what each formula means and why "
        "it's used here, for a reader who is not a mathematician."
    )


class CodeWalkthrough(BaseModel):
    """`code_agent` output: the notebook's Python cells, explained concept by concept."""

    concepts: list[str] = Field(
        description="The programming/library concepts the code cells demonstrate, "
        "in the order they appear."
    )
    explanation: str = Field(
        description="Markdown walking through the code cells for a reader who "
        "knows Python but not necessarily this library."
    )


class DocSection(BaseModel):
    """One section of the assembled lesson document."""

    heading: str
    body_markdown: str


class WriterOutput(BaseModel):
    """`writer_agent` output: the drafted lesson document, before validation."""

    title: str
    sections: list[DocSection]


class ValidationFinding(BaseModel):
    """One issue `validator_agent` found in the draft."""

    severity: str = Field(description='One of "info", "warning", "error".')
    note: str


class ValidatorOutput(BaseModel):
    """`validator_agent` output: a report appended to the document (v1 is report-only,
    no auto-revision loop — see SDD section 5)."""

    findings: list[ValidationFinding] = Field(default_factory=list)
    overall_assessment: str
