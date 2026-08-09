"""Tests for the queue picker that drives the remediation loop.

The picker is the only thing standing between a cold iteration and the work,
so its selection rules deserve tests of their own. The regression these were
written for is `test_in_progress_item_is_offered_again`: an item deliberately
left `in_progress` — the procedure's own way of splitting work too big for one
iteration — was never offered again, and the loop reported that everything was
waiting on a human decision when no decision was open.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "next_work_item.py"


def _load_picker() -> Any:
    """Import the picker by path: scripts/ is not an importable package."""

    spec = importlib.util.spec_from_file_location("next_work_item", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


picker = _load_picker()


def item(item_id: str, priority: str = "P2", status: str = "todo", **extra: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": item_id,
        "title": f"Titolo di {item_id}",
        "priority": priority,
        "status": status,
        "verify": ["uv run pytest"],
    }
    base.update(extra)
    return base


def queue_of(*items: dict[str, Any], decisions: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"meta": {"decisions": decisions or {}}, "items": list(items)}


def picked_ids(queue: dict[str, Any]) -> list[str]:
    return [chosen["id"] for chosen in picker.actionable(queue)]


def run_main(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, queue_text: str) -> int:
    """Run main() against a queue file written for the test."""

    queue_file = tmp_path / "queue.yaml"
    queue_file.write_text(queue_text, encoding="utf-8")
    monkeypatch.setattr(picker, "QUEUE_PATH", queue_file)
    monkeypatch.setattr(sys, "argv", ["next_work_item.py"])
    return picker.main()


class TestSelection:
    def test_in_progress_item_is_offered_again(self) -> None:
        """The regression: a split item must come back, not vanish."""

        queue = queue_of(item("WI-6", status="in_progress"), item("WI-9", status="done"))
        assert picked_ids(queue) == ["WI-6"]

    def test_in_progress_wins_the_tie_inside_one_priority(self) -> None:
        queue = queue_of(item("WI-8"), item("WI-6", status="in_progress"))
        assert picked_ids(queue) == ["WI-6", "WI-8"]

    def test_priority_still_outranks_a_started_item(self) -> None:
        """Continuity breaks the tie; it never beats a more urgent item."""

        queue = queue_of(item("WI-6", priority="P2", status="in_progress"), item("WI-1", "P0"))
        assert picked_ids(queue) == ["WI-1", "WI-6"]

    def test_done_and_cancelled_are_never_offered(self) -> None:
        queue = queue_of(item("WI-5", status="cancelled"), item("WI-9", status="done"))
        assert picked_ids(queue) == []

    def test_an_open_decision_still_holds_an_item_back(self) -> None:
        queue = queue_of(
            item("WI-12", status="in_progress", blocked_by=["D1"]),
            decisions={"D1": {"status": "open", "question": "?", "recommendation": "-"}},
        )
        assert picked_ids(queue) == []

    def test_an_unmet_dependency_still_holds_an_item_back(self) -> None:
        queue = queue_of(item("WI-1", status="todo"), item("WI-5", depends_on=["WI-1"]))
        assert picked_ids(queue) == ["WI-1"]


class TestDescribe:
    def test_a_resumed_item_is_marked_and_its_notes_labelled(self) -> None:
        text = picker.describe(item("WI-6", status="in_progress", notes="Restano le lezioni 34-60."))
        assert text.startswith("RESUME: WI-6")
        assert "handover from the previous iteration" in text
        assert "Restano le lezioni 34-60." in text

    def test_a_fresh_item_is_not_dressed_up_as_a_resume(self) -> None:
        text = picker.describe(item("WI-8", notes="Una nota."))
        assert text.startswith("NEXT: WI-8")
        assert "RESUME" not in text
        assert "Note: Una nota." in text


class TestStopMessages:
    def test_nothing_actionable_names_the_real_blocker(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        exit_code = run_main(
            monkeypatch,
            tmp_path,
            """
meta:
  decisions:
    D1: {status: open, question: "Quale percorso mlops?", recommendation: Ridurlo}
items:
  - {id: WI-12, title: mlops, priority: P3, status: todo, blocked_by: [D1]}
""",
        )
        out = capsys.readouterr().out
        assert exit_code == 2
        assert "SENTINEL: NOTHING-ACTIONABLE" in out
        assert "WI-12: decision D1" in out
        assert "Quale percorso mlops?" in out

    def test_a_cancelled_dependency_is_reported_as_dead(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A prerequisite nobody will ever finish is a queue bug, not a wait."""

        exit_code = run_main(
            monkeypatch,
            tmp_path,
            """
meta: {decisions: {}}
items:
  - {id: WI-5, title: esercizi, priority: P1, status: cancelled}
  - {id: WI-6, title: teoria, priority: P2, status: todo, depends_on: [WI-5]}
""",
        )
        out = capsys.readouterr().out
        assert exit_code == 2
        assert "dead dependency" in out
        assert "waits on a human decision" not in out

    def test_all_done_when_only_closed_items_remain(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        exit_code = run_main(
            monkeypatch,
            tmp_path,
            """
meta: {decisions: {}}
items:
  - {id: WI-5, title: esercizi, priority: P1, status: cancelled}
  - {id: WI-9, title: seed, priority: P2, status: done}
""",
        )
        out = capsys.readouterr().out
        assert exit_code == 2
        assert "SENTINEL: ALL-DONE" in out

    def test_a_stranded_in_progress_item_is_flagged(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        exit_code = run_main(
            monkeypatch,
            tmp_path,
            """
meta:
  decisions:
    D1: {status: open, question: "Quale percorso mlops?", recommendation: Ridurlo}
items:
  - {id: WI-12, title: mlops, priority: P3, status: in_progress, blocked_by: [D1]}
""",
        )
        out = capsys.readouterr().out
        assert exit_code == 2
        assert "WARNING: in_progress but not offerable: WI-12" in out

    def test_the_real_queue_offers_work(self) -> None:
        """The shipped queue must not be in the deadlock this fix removes."""

        queue = picker.load_queue(Path("reports/handover/queue.yaml"))
        assert picker.validate(queue) == []
        assert picked_ids(queue), "the remediation queue offers nothing to work"
