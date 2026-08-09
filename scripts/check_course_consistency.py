"""Report where `course.yaml`, `course/progress.yaml` and the files on disk disagree.

This exists because the audit in `reports/SDD-remediation-2026-08-06.md` was done
by hand, and by the time it was written the two trackers had drifted far enough
that 17 declared lessons existed nowhere else in the repository — invisible both
as work done and as work missing.

It is a tool to run before a work session, not a CI gate: the course author has
said CI state is not itself a goal. Nothing here fails a build.

Usage:
    uv run python scripts/check_course_consistency.py            # human report
    uv run python scripts/check_course_consistency.py --strict   # exit 1 on findings

What it checks:

1. lessons declared in `course.yaml` but not tracked in `progress.yaml`;
2. lessons tracked in `progress.yaml` but not declared in `course.yaml`;
3. lessons whose tracked artifacts name a file that does not exist;
4. published pages under `docs/modules/` that no lesson declares;
5. lessons at `learner_review` or `done` carrying a quality gate that is not
   `pass` (or `not_applicable`), which would assert a state nothing supports.

Known exception: `pmle-en-translations` is tracked as a deliverable, not a
lesson — it records the seven English translations of the PMLE pages, which
have no lesson id of their own. It is reported under its own heading rather
than counted as drift.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

COURSE_PATH = Path("course/course.yaml")
PROGRESS_PATH = Path("course/progress.yaml")
MODULES_DIR = Path("docs/modules")

# Tracked on purpose without a lesson id in course.yaml; see the module docstring.
DELIVERABLE_ENTRIES = {"pmle-en-translations"}

REVIEWED_STATUSES = {"learner_review", "done"}
ACCEPTABLE_GATES = {"pass", "not_applicable"}


def load_declared(course: dict) -> dict[str, str]:
    """Map every lesson id declared in course.yaml to the module declaring it."""
    declared: dict[str, str] = {}
    for module in course.get("modules") or []:
        module_id = module.get("id")
        for lesson in module.get("lessons") or []:
            lesson_id = lesson if isinstance(lesson, str) else lesson.get("id")
            if lesson_id:
                declared[lesson_id] = module_id
    return declared


def load_tracked(progress: dict) -> dict[str, dict]:
    """Map every lesson id tracked in progress.yaml to its tracking entry."""
    tracked: dict[str, dict] = {}
    for module_id, module in (progress.get("modules") or {}).items():
        for lesson_id, entry in (module.get("lessons") or {}).items():
            tracked[lesson_id] = {"module": module_id, **(entry or {})}
    return tracked


def artifact_paths(entry: dict):
    """Yield (field, path) for artifact values that look like real repo paths.

    Values are skipped when they are null, when they carry a parenthetical note
    instead of a path, or when they use a glob — `progress.yaml` uses all three
    forms today and none of them names a single checkable file.
    """
    for field, value in (entry.get("artifacts") or {}).items():
        if not isinstance(value, str) or not value.strip():
            continue
        if "(" in value or "*" in value or ".." in value:
            continue
        yield field, value.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if anything is reported")
    args = parser.parse_args()

    course = yaml.safe_load(COURSE_PATH.read_text(encoding="utf-8"))
    progress = yaml.safe_load(PROGRESS_PATH.read_text(encoding="utf-8"))

    declared = load_declared(course)
    tracked = load_tracked(progress)
    pages = {p.stem for p in MODULES_DIR.glob("*.md")} - {"index"}

    findings = 0

    print(f"declared in course.yaml : {len(declared)}")
    print(f"tracked in progress.yaml: {len(tracked)}")
    print(f"pages in docs/modules/  : {len(pages)}")
    print()

    undeclared_tracked = sorted(set(tracked) - set(declared) - DELIVERABLE_ENTRIES)
    untracked = sorted(set(declared) - set(tracked))

    if untracked:
        findings += len(untracked)
        print(f"[1] declared but not tracked ({len(untracked)}):")
        for lesson_id in untracked:
            print(f"    {declared[lesson_id]:22} {lesson_id}")
        print()

    if undeclared_tracked:
        findings += len(undeclared_tracked)
        print(f"[2] tracked but not declared ({len(undeclared_tracked)}):")
        for lesson_id in undeclared_tracked:
            print(f"    {tracked[lesson_id]['module']:22} {lesson_id}")
        print()

    missing_artifacts = []
    for lesson_id, entry in sorted(tracked.items()):
        for field, value in artifact_paths(entry):
            if not Path(value).exists():
                missing_artifacts.append((lesson_id, field, value))
    if missing_artifacts:
        findings += len(missing_artifacts)
        print(f"[3] tracked artifacts that do not exist ({len(missing_artifacts)}):")
        for lesson_id, field, value in missing_artifacts:
            print(f"    {lesson_id:38} {field}: {value}")
        print()

    undeclared_pages = sorted(pages - set(declared) - DELIVERABLE_ENTRIES)
    if undeclared_pages:
        findings += len(undeclared_pages)
        print(f"[4] published pages no lesson declares ({len(undeclared_pages)}):")
        for page in undeclared_pages:
            print(f"    docs/modules/{page}.md")
        print()

    overstated = []
    for lesson_id, entry in sorted(tracked.items()):
        if entry.get("status") not in REVIEWED_STATUSES:
            continue
        for gate, value in (entry.get("quality_gates") or {}).items():
            if value not in ACCEPTABLE_GATES:
                overstated.append((lesson_id, entry["status"], gate, value))
    if overstated:
        findings += len(overstated)
        print(f"[5] reviewed lessons with a non-pass gate ({len(overstated)}):")
        for lesson_id, status, gate, value in overstated:
            print(f"    {lesson_id:38} status={status} {gate}={value}")
        print()

    present_deliverables = sorted(DELIVERABLE_ENTRIES & set(tracked))
    if present_deliverables:
        print("tracked deliverables (not lessons, not drift):")
        for lesson_id in present_deliverables:
            print(f"    {tracked[lesson_id]['module']:22} {lesson_id}")
        print()

    if findings == 0:
        print("OK: nothing to reconcile.")
    else:
        print(f"{findings} thing(s) to reconcile.")

    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
