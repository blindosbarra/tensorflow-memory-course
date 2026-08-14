"""Tests for `lesson_agent.catalog` — the syllabus join and the learner's progress."""

from __future__ import annotations

import json

from lesson_agent import catalog
from lesson_agent.catalog import LessonProgress, Status


def test_load_modules_joins_course_yaml_with_doc_frontmatter() -> None:
    modules = catalog.load_modules()
    assert modules, "course.yaml deve produrre almeno un modulo"

    lesson = catalog.find_lesson(modules, "capstone-pipeline")
    assert lesson is not None
    assert lesson.module_id == "capstone"
    assert lesson.title == "La pipeline: MemoryAILab"
    assert lesson.notebook_path is not None
    assert lesson.notebook_path.name == "lezione-58-capstone-pipeline.ipynb"
    assert lesson.number == 58
    assert lesson.display_title.startswith("58 · ")


def test_notebook_is_resolved_through_deliverables_not_the_filename() -> None:
    """Numbering and slugs drifted apart; `deliverables:` is the real link.

    `python-numpy-refresh` is the canonical example — its notebook is
    `lezione-06-numpy.ipynb`, which no filename-based rule would find.
    """

    lesson = catalog.find_lesson(catalog.load_modules(), "python-numpy-refresh")
    assert lesson is not None
    assert lesson.notebook_path is not None
    assert lesson.notebook_path.name == "lezione-06-numpy.ipynb"


def test_unwritten_lessons_are_listed_but_not_published() -> None:
    """The MLOps phase is planned in course.yaml and has no doc page yet."""

    modules = catalog.load_modules()
    lesson = catalog.find_lesson(modules, "reproducible-project")
    assert lesson is not None, "la lezione deve restare visibile nel syllabus"
    assert not lesson.is_published
    assert not lesson.has_notebook


def test_theory_only_lessons_are_published_without_a_notebook() -> None:
    lesson = catalog.find_lesson(
        catalog.load_modules(), "pmle-01-architect-low-code-ai-solutions"
    )
    assert lesson is not None
    assert lesson.is_published
    assert not lesson.has_notebook


def test_progress_roundtrip(tmp_path) -> None:
    progress = {"a-lesson": LessonProgress(status=Status.COMPLETATA, notes="fatto")}
    catalog.save_progress(progress, tmp_path)
    assert catalog.load_progress(tmp_path) == progress


def test_missing_or_corrupt_progress_is_empty(tmp_path) -> None:
    assert catalog.load_progress(tmp_path) == {}
    (tmp_path / "progress.json").write_text("[]", encoding="utf-8")
    assert catalog.load_progress(tmp_path) == {}
    (tmp_path / "progress.json").write_text("{ broken", encoding="utf-8")
    assert catalog.load_progress(tmp_path) == {}


def test_unknown_status_on_disk_falls_back_to_da_fare(tmp_path) -> None:
    (tmp_path / "progress.json").write_text(
        json.dumps({"x": {"status": "inventato"}}), encoding="utf-8"
    )
    assert catalog.load_progress(tmp_path)["x"].status is Status.DA_FARE


def test_touch_promotes_da_fare_to_in_corso_but_never_completes(tmp_path) -> None:
    """Opening a lesson is not the same claim as having understood it."""

    progress: dict[str, LessonProgress] = {}
    progress = catalog.touch_lesson(progress, "x", tmp_path)
    assert progress["x"].status is Status.IN_CORSO
    assert progress["x"].last_opened

    progress = catalog.set_status(progress, "x", Status.COMPLETATA, tmp_path)
    progress = catalog.touch_lesson(progress, "x", tmp_path)
    assert progress["x"].status is Status.COMPLETATA


def test_notes_and_generated_docs_survive_a_status_change(tmp_path) -> None:
    progress: dict[str, LessonProgress] = {}
    progress = catalog.save_notes(progress, "x", "le mie note", tmp_path)
    progress = catalog.record_generated_doc(progress, "x", tmp_path)
    progress = catalog.set_status(progress, "x", Status.COMPLETATA, tmp_path)

    reloaded = catalog.load_progress(tmp_path)["x"]
    assert reloaded.notes == "le mie note"
    assert reloaded.docs_generated == 1
    assert reloaded.status is Status.COMPLETATA
