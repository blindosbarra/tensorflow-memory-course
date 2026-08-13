"""Tests for `lesson_agent.agents`.

Graph construction is checked unconditionally (no API key, no network — it's
just Pydantic object construction and ADK's graph validator). The real
end-to-end run is skipped unless `GOOGLE_API_KEY` is set, per the test
strategy decided in `reports/SDD-lesson-agent-2026-08-11.md` section 5.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest

from lesson_agent.agents import build_workflow

REPO_ROOT = Path(__file__).resolve().parents[1]

_NO_KEY = not os.environ.get("GOOGLE_API_KEY")


def test_build_workflow_graph_shape() -> None:
    workflow = build_workflow()
    node_names = {n.name for n in workflow.graph.nodes}
    assert node_names == {
        "__START__",
        "gather_info_agent",
        "math_agent",
        "code_agent",
        "math_code_join",
        "writer_agent",
        "validator_agent",
    }
    edges = {(e.from_node.name, e.to_node.name) for e in workflow.graph.edges}
    # gather_info_agent fans out to both parallel branches...
    assert ("gather_info_agent", "math_agent") in edges
    assert ("gather_info_agent", "code_agent") in edges
    # ...and both join before writer_agent, which precedes validator_agent.
    assert ("math_agent", "math_code_join") in edges
    assert ("code_agent", "math_code_join") in edges
    assert ("math_code_join", "writer_agent") in edges
    assert ("writer_agent", "validator_agent") in edges


@pytest.mark.skipif(_NO_KEY, reason="requires GOOGLE_API_KEY (real Gemini call)")
def test_generate_lesson_doc_lezione_58(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(REPO_ROOT)
    monkeypatch.setattr(
        "lesson_agent.render_html.OUTPUT_DIR", tmp_path, raising=False
    )
    from scripts.generate_lesson_doc import generate_lesson_doc

    # write_lesson_html's default output_dir is bound at import time in the
    # script, so patch it there too.
    import scripts.generate_lesson_doc as script

    original_write = script.write_lesson_html

    def _write_to_tmp(context, writer, validator):
        return original_write(context, writer, validator, output_dir=tmp_path)

    monkeypatch.setattr(script, "write_lesson_html", _write_to_tmp)

    output_path = asyncio.run(generate_lesson_doc("capstone-pipeline"))
    assert output_path.exists()
    html = output_path.read_text(encoding="utf-8")
    assert "<!doctype html>" in html.lower()
    assert "MemoryAILab" in html or "memoryailab" in html.lower()
