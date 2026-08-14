"""The course as the *learner* sees it: modules, lessons, and their own progress.

Three sources have to be joined to render a syllabus, and none of them alone
is enough:

- `course/course.yaml` — the module → lesson-id ordering, i.e. the intended
  study path. It is the only place that says lesson `capstone-pipeline`
  belongs to module `capstone` and comes after `capstone-evaluation`.
- `docs/modules/*.md` frontmatter — the lesson's title, estimated minutes,
  prerequisites, sources, and the `deliverables:` list naming its notebook.
  As `read_notebook.py` documents, notebook numbering and lesson slugs
  drifted apart, so `deliverables:` is the only reliable notebook link.
- `.learner/progress.json` — **the learner's own** progress. Deliberately not
  `course/progress.yaml`: that file is committed and tracks whether the
  *authors* finished writing a lesson (`learner_review`, quality gates). Two
  different questions that happen to share the word "progress"; conflating
  them would have the GUI tell the learner they'd completed lessons they
  have never opened.

The doc index is built once per call (69 files, one pass) instead of
`find_lesson_doc`'s per-notebook scan, which was O(notebooks × docs).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import json
from pathlib import Path
import re
from typing import Any

import yaml

from lesson_agent.read_notebook import KNOWLEDGE_DIR, MODULES_DIR, NOTEBOOKS_DIR, parse_frontmatter
from lesson_agent import settings
from lesson_agent.settings import REPO_ROOT

COURSE_YAML = REPO_ROOT / "course" / "course.yaml"
PROGRESS_FILENAME = "progress.json"

_LESSON_NUMBER_RE = re.compile(r"lezione-(\d+)-")


class Status(str, Enum):
    """The learner's own state on a lesson."""

    DA_FARE = "da_fare"
    IN_CORSO = "in_corso"
    COMPLETATA = "completata"

    @property
    def label(self) -> str:
        return {
            Status.DA_FARE: "Da fare",
            Status.IN_CORSO: "In corso",
            Status.COMPLETATA: "Completata",
        }[self]

    @property
    def icon(self) -> str:
        return {Status.DA_FARE: "⚪", Status.IN_CORSO: "🟡", Status.COMPLETATA: "🟢"}[self]


@dataclass(frozen=True)
class Lesson:
    """One lesson, joined across course.yaml, its doc page and the filesystem."""

    lesson_id: str
    title: str
    module_id: str
    module_title: str
    doc_path: Path | None
    notebook_path: Path | None
    estimated_minutes: int | None
    prerequisites: tuple[str, ...]
    sources: tuple[str, ...]
    has_evidence: bool

    @property
    def number(self) -> int | None:
        """The `NN` from `lezione-NN-slug.ipynb`, for display and ordering."""

        if self.notebook_path is None:
            return None
        match = _LESSON_NUMBER_RE.search(self.notebook_path.name)
        return int(match.group(1)) if match else None

    @property
    def has_notebook(self) -> bool:
        return self.notebook_path is not None

    @property
    def is_published(self) -> bool:
        """False for lessons `course.yaml` plans but nobody has written yet.

        Three of them exist today — the MLOps phase (`reproducible-project`,
        `containers-artifacts`, `local-training-pipeline`), which
        `course/progress.yaml` records as "fase 7 non costruita". They are
        real entries in the syllabus, so the GUI lists them; it just must not
        offer to open a page that does not exist.
        """

        return self.doc_path is not None

    @property
    def display_title(self) -> str:
        number = self.number
        return f"{number:02d} · {self.title}" if number is not None else self.title


@dataclass(frozen=True)
class Module:
    """A course module and its lessons, in the intended study order."""

    module_id: str
    title: str
    optional: bool
    lessons: tuple[Lesson, ...]


def _build_doc_index(modules_dir: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    """Map lesson id → (doc path, frontmatter), in one pass over docs/modules."""

    index: dict[str, tuple[Path, dict[str, Any]]] = {}
    for doc_path in sorted(modules_dir.glob("*.md")):
        try:
            front, _ = parse_frontmatter(doc_path)
        except ValueError:
            continue  # e.g. docs/modules/index.md — hand-written, no frontmatter
        lesson_id = front.get("id") or doc_path.stem
        index[str(lesson_id)] = (doc_path, front)
    return index


def _notebook_for(front: dict[str, Any], notebooks_dir: Path) -> Path | None:
    """Resolve the lesson's notebook from its `deliverables:` list, if any.

    Lessons in the PMLE certification module are theory-only and legitimately
    have no notebook, so `None` is a normal answer, not an error.
    """

    for deliverable in front.get("deliverables") or []:
        name = Path(str(deliverable)).name
        if not name.endswith(".ipynb"):
            continue
        candidate = notebooks_dir / name
        if candidate.exists():
            return candidate
    return None


def load_modules(
    course_yaml: Path = COURSE_YAML,
    modules_dir: Path = MODULES_DIR,
    notebooks_dir: Path = NOTEBOOKS_DIR,
    knowledge_dir: Path = KNOWLEDGE_DIR,
) -> list[Module]:
    """Read the whole course structure, ready for the GUI's syllabus view."""

    data = yaml.safe_load(course_yaml.read_text(encoding="utf-8")) or {}
    doc_index = _build_doc_index(modules_dir)

    modules: list[Module] = []
    for raw_module in data.get("modules") or []:
        module_id = str(raw_module.get("id", ""))
        module_title = str(raw_module.get("title", module_id))
        lessons: list[Lesson] = []

        for lesson_id in raw_module.get("lessons") or []:
            lesson_id = str(lesson_id)
            doc_path, front = doc_index.get(lesson_id, (None, {}))
            notebook_path = _notebook_for(front, notebooks_dir) if front else None
            minutes = front.get("estimated_minutes")
            lessons.append(
                Lesson(
                    lesson_id=lesson_id,
                    title=str(front.get("title") or lesson_id),
                    module_id=module_id,
                    module_title=module_title,
                    doc_path=doc_path,
                    notebook_path=notebook_path,
                    estimated_minutes=int(minutes) if isinstance(minutes, int) else None,
                    prerequisites=tuple(str(p) for p in (front.get("prerequisites") or [])),
                    sources=tuple(str(s) for s in (front.get("sources") or [])),
                    has_evidence=(knowledge_dir / lesson_id / "evidence.yaml").exists(),
                )
            )

        modules.append(
            Module(
                module_id=module_id,
                title=module_title,
                optional=bool(raw_module.get("optional", False)),
                lessons=tuple(lessons),
            )
        )
    return modules


def all_lessons(modules: list[Module]) -> list[Lesson]:
    return [lesson for module in modules for lesson in module.lessons]


def find_lesson(modules: list[Module], lesson_id: str) -> Lesson | None:
    for lesson in all_lessons(modules):
        if lesson.lesson_id == lesson_id:
            return lesson
    return None


# --------------------------------------------------------------------------
# The learner's own progress (git-ignored, never mixed with course/progress.yaml)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class LessonProgress:
    """What the learner has done with one lesson."""

    status: Status = Status.DA_FARE
    notes: str = ""
    last_opened: str = ""
    docs_generated: int = 0


def progress_path(learner_dir: Path | None = None) -> Path:
    """Where the learner's progress lives.

    Resolved at call time (not as a default argument) so `settings.LEARNER_DIR`
    can be redirected — the GUI tests must never write into the real
    `.learner/`.
    """

    return (learner_dir or settings.LEARNER_DIR) / PROGRESS_FILENAME


def load_progress(learner_dir: Path | None = None) -> dict[str, LessonProgress]:
    path = progress_path(learner_dir)
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(raw, dict):
        return {}

    progress: dict[str, LessonProgress] = {}
    for lesson_id, entry in raw.items():
        if not isinstance(entry, dict):
            continue
        try:
            status = Status(entry.get("status"))
        except ValueError:
            status = Status.DA_FARE
        progress[str(lesson_id)] = LessonProgress(
            status=status,
            notes=str(entry.get("notes") or ""),
            last_opened=str(entry.get("last_opened") or ""),
            docs_generated=int(entry.get("docs_generated") or 0),
        )
    return progress


def save_progress(progress: dict[str, LessonProgress], learner_dir: Path | None = None) -> Path:
    path = progress_path(learner_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        lesson_id: {
            "status": entry.status.value,
            "notes": entry.notes,
            "last_opened": entry.last_opened,
            "docs_generated": entry.docs_generated,
        }
        for lesson_id, entry in sorted(progress.items())
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def touch_lesson(
    progress: dict[str, LessonProgress],
    lesson_id: str,
    learner_dir: Path | None = None,
) -> dict[str, LessonProgress]:
    """Record that the learner opened a lesson; promote `da_fare` → `in_corso`.

    Only the automatic transition happens here. Marking a lesson *completed*
    stays an explicit act in the GUI: auto-completing on open would make the
    progress view a list of pages visited, which is not the same claim.
    """

    current = progress.get(lesson_id, LessonProgress())
    progress[lesson_id] = LessonProgress(
        status=Status.IN_CORSO if current.status is Status.DA_FARE else current.status,
        notes=current.notes,
        last_opened=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        docs_generated=current.docs_generated,
    )
    save_progress(progress, learner_dir)
    return progress


def set_status(
    progress: dict[str, LessonProgress],
    lesson_id: str,
    status: Status,
    learner_dir: Path | None = None,
) -> dict[str, LessonProgress]:
    current = progress.get(lesson_id, LessonProgress())
    progress[lesson_id] = LessonProgress(
        status=status,
        notes=current.notes,
        last_opened=current.last_opened,
        docs_generated=current.docs_generated,
    )
    save_progress(progress, learner_dir)
    return progress


def record_generated_doc(
    progress: dict[str, LessonProgress],
    lesson_id: str,
    learner_dir: Path | None = None,
) -> dict[str, LessonProgress]:
    current = progress.get(lesson_id, LessonProgress())
    progress[lesson_id] = LessonProgress(
        status=current.status,
        notes=current.notes,
        last_opened=current.last_opened,
        docs_generated=current.docs_generated + 1,
    )
    save_progress(progress, learner_dir)
    return progress


def save_notes(
    progress: dict[str, LessonProgress],
    lesson_id: str,
    notes: str,
    learner_dir: Path | None = None,
) -> dict[str, LessonProgress]:
    current = progress.get(lesson_id, LessonProgress())
    progress[lesson_id] = LessonProgress(
        status=current.status,
        notes=notes,
        last_opened=current.last_opened,
        docs_generated=current.docs_generated,
    )
    save_progress(progress, learner_dir)
    return progress
