"""Pick the next actionable work item from the remediation queue.

The remediation loop starts cold on every iteration, so the queue file is the
only state that survives between them. This script reads it, resolves
dependencies and open decisions, and prints the one item to work on next.

Usage:
    uv run python scripts/next_work_item.py           # next actionable item
    uv run python scripts/next_work_item.py --board    # full status board
    uv run python scripts/next_work_item.py --check    # validate the queue only

Exit codes:
    0  an actionable item was printed (or --board/--check succeeded)
    2  nothing actionable: everything is done, or the rest needs a decision
    3  the queue file is missing or malformed

Exit codes alone are not a safe control signal for the loop: a *missing*
script makes the interpreter itself exit 2, which is indistinguishable from
"nothing actionable" and silently ends a loop that has done no work. That
happened on 2026-08-07 (see the postmortem in the SDD, section 6). Every run
therefore prints a sentinel as its first stdout line, and the loop must key
on the sentinel:

    SENTINEL: PICK <id>          an item was selected, work it
    SENTINEL: ALL-DONE           the queue is finished
    SENTINEL: NOTHING-ACTIONABLE everything left waits on a human decision
    SENTINEL: QUEUE-MALFORMED    the queue file is unusable
    SENTINEL: QUEUE-MISSING      the queue file is not there at all
    SENTINEL: BOARD / CHECK-OK   informational modes

No sentinel line at all means this script did not run. That is an
environment problem, never a statement about the work.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import yaml

QUEUE_PATH = Path("reports/handover/queue.yaml")
PRIORITY_ORDER = ("P0", "P1", "P2", "P3")
VALID_STATUS = frozenset({"todo", "in_progress", "done", "blocked", "cancelled"})
# Statuses that need no further work. `cancelled` means the course author
# decided against the item; it must never be offered again, and it must not
# keep the loop from reporting ALL-DONE.
CLOSED_STATUS = frozenset({"done", "cancelled"})


def sentinel(name: str) -> None:
    """Print the machine-readable control line the loop keys on."""

    print(f"SENTINEL: {name}")


def load_queue(path: Path) -> dict[str, Any]:
    """Read the queue file and fail loudly if it is not usable."""

    if not path.exists():
        sentinel("QUEUE-MISSING")
        print(f"Queue file not found: {path}", file=sys.stderr)
        print(
            "Run from the repository root, on a branch that carries "
            "reports/handover/queue.yaml.",
            file=sys.stderr,
        )
        raise SystemExit(3)
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        sentinel("QUEUE-MALFORMED")
        print(f"{path}: not valid YAML: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc
    if not isinstance(loaded, dict):
        sentinel("QUEUE-MALFORMED")
        print(f"{path}: expected a mapping at the top level", file=sys.stderr)
        raise SystemExit(3)
    return loaded


def validate(queue: dict[str, Any]) -> list[str]:
    """Return a list of structural problems; empty means the queue is sound."""

    problems: list[str] = []
    items = queue.get("items")
    if not isinstance(items, list) or not items:
        return [f"{QUEUE_PATH}: 'items' must be a non-empty list"]

    known_ids = {item.get("id") for item in items}
    decisions = (queue.get("meta") or {}).get("decisions") or {}

    for item in items:
        item_id = item.get("id", "<missing id>")
        status = item.get("status")
        if status not in VALID_STATUS:
            problems.append(f"{item_id}: invalid status {status!r}")
        if item.get("priority") not in PRIORITY_ORDER:
            problems.append(f"{item_id}: invalid priority {item.get('priority')!r}")
        for dep in item.get("depends_on") or []:
            if dep not in known_ids:
                problems.append(f"{item_id}: depends_on unknown item {dep!r}")
        for decision in item.get("blocked_by") or []:
            if decision not in decisions:
                problems.append(f"{item_id}: blocked_by unknown decision {decision!r}")
        if status == "blocked" and not (item.get("blocked_by") or item.get("depends_on")):
            problems.append(f"{item_id}: status 'blocked' but nothing blocks it")

    return problems


def unresolved_decisions(queue: dict[str, Any], item: dict[str, Any]) -> list[str]:
    """Names of the decisions this item is still waiting on."""

    decisions = (queue.get("meta") or {}).get("decisions") or {}
    return [
        name
        for name in (item.get("blocked_by") or [])
        if (decisions.get(name) or {}).get("status") != "resolved"
    ]


def unmet_dependencies(item: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> list[str]:
    """Ids of the prerequisite items that are not done yet."""

    return [
        dep
        for dep in (item.get("depends_on") or [])
        if (by_id.get(dep) or {}).get("status") != "done"
    ]


def actionable(queue: dict[str, Any]) -> list[dict[str, Any]]:
    """Items that can be started right now, most important first."""

    items: list[dict[str, Any]] = queue["items"]
    by_id = {item["id"]: item for item in items}
    ready = [
        item
        for item in items
        if item.get("status") in {"todo", "blocked"}
        and not unresolved_decisions(queue, item)
        and not unmet_dependencies(item, by_id)
    ]
    return sorted(ready, key=lambda item: PRIORITY_ORDER.index(item["priority"]))


def describe(item: dict[str, Any]) -> str:
    """Render the picked item as the instructions for one loop iteration."""

    lines = [
        f"NEXT: {item['id']} [{item['priority']}] {item['title']}",
        "",
        "Read the specification for this item in:",
        f"  reports/SDD-remediation-2026-08-06.md  (section {item['id']})",
        "",
        "Files in scope:",
    ]
    lines += [f"  {path}" for path in item.get("files") or []]
    if item.get("verify_fast"):
        lines += [
            "",
            "Verify (fast gate — run first, cheap, must pass):",
        ]
        lines += [f"  {command}" for command in item["verify_fast"]]
    lines += ["", "Verify (full gate — the item is not done until these pass):"]
    lines += [f"  {command}" for command in item.get("verify") or []]
    lines += ["", f"Expect: {item.get('expect', '-')}"]
    if item.get("verify_env"):
        lines += ["", f"Environment needed: {item['verify_env']}"]
    if item.get("notes"):
        lines += ["", f"Note: {item['notes'].strip()}"]
    return "\n".join(lines)


def board(queue: dict[str, Any]) -> str:
    """Render every item with the reason it is or is not actionable."""

    items: list[dict[str, Any]] = queue["items"]
    by_id = {item["id"]: item for item in items}
    ready_ids = {item["id"] for item in actionable(queue)}

    lines = [f"{'ID':<6} {'PRI':<4} {'STATUS':<12} REASON / TITLE"]
    for item in items:
        reasons: list[str] = []
        if item["id"] not in ready_ids and item.get("status") not in (
            CLOSED_STATUS | {"in_progress"}
        ):
            waiting = unresolved_decisions(queue, item)
            missing = unmet_dependencies(item, by_id)
            if waiting:
                reasons.append("needs " + ", ".join(waiting))
            if missing:
                reasons.append("after " + ", ".join(missing))
        suffix = f"({'; '.join(reasons)}) " if reasons else ""
        lines.append(
            f"{item['id']:<6} {item['priority']:<4} {item['status']:<12} {suffix}{item['title']}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", action="store_true", help="show every item and its state")
    parser.add_argument("--check", action="store_true", help="validate the queue and exit")
    args = parser.parse_args()

    queue = load_queue(QUEUE_PATH)

    problems = validate(queue)
    if problems:
        sentinel("QUEUE-MALFORMED")
        print("Queue file is malformed:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 3

    if args.check:
        sentinel("CHECK-OK")
        print(f"{QUEUE_PATH}: OK ({len(queue['items'])} items)")
        return 0

    if args.board:
        sentinel("BOARD")
        print(board(queue))
        return 0

    stale = [item for item in queue["items"] if item.get("status") == "in_progress"]
    if stale:
        ids = ", ".join(item["id"] for item in stale)
        print(f"WARNING: left in_progress by an earlier iteration: {ids}")
        print("Check git log for a commit referencing it. If none, reset it to 'todo'.")
        print()

    ready = actionable(queue)
    if not ready:
        remaining = [
            item for item in queue["items"] if item.get("status") not in CLOSED_STATUS
        ]
        if not remaining:
            sentinel("ALL-DONE")
            print("All work items are done.")
            return 2
        sentinel("NOTHING-ACTIONABLE")
        print("Nothing is actionable. Every remaining item waits on a human decision.")
        print()
        print(board(queue))
        print()
        decisions = (queue.get("meta") or {}).get("decisions") or {}
        for name, decision in decisions.items():
            if decision.get("status") != "resolved":
                print(f"{name}: {decision.get('question')}")
                print(f"    suggested: {decision.get('recommendation')}")
        return 2

    sentinel(f"PICK {ready[0]['id']}")
    print(describe(ready[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
