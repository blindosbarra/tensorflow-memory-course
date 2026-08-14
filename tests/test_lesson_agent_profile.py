"""Tests for `lesson_agent.profile` — the learner model the agents read."""

from __future__ import annotations

import json

from lesson_agent.profile import (
    Comfort,
    Depth,
    LearnerProfile,
    Level,
    load_profile,
    save_profile,
)


def test_briefing_differs_by_level() -> None:
    """The whole point of the profile: different learners get different prompts."""

    beginner = LearnerProfile(level=Level.PRINCIPIANTE).briefing()
    expert = LearnerProfile(level=Level.AVANZATO).briefing()
    assert beginner != expert
    assert "principiante" in beginner
    assert "Salta le basi" in expert


def test_briefing_includes_free_text_fields_only_when_filled() -> None:
    bare = LearnerProfile().briefing()
    assert "Background dichiarato" not in bare
    assert "Obiettivo dichiarato" not in bare

    filled = LearnerProfile(
        background="backend Python",
        goals="memoria per un chatbot",
        known_topics=["pandas", "algebra lineare"],
    ).briefing()
    assert "backend Python" in filled
    assert "memoria per un chatbot" in filled
    assert "pandas, algebra lineare" in filled


def test_briefing_covers_every_axis() -> None:
    """Level, math, Python and depth must all reach the prompt, not just level."""

    profile = LearnerProfile(
        level=Level.INTERMEDIO,
        math_comfort=Comfort.SOLIDA,
        python_comfort=Comfort.POCA,
        depth=Depth.SINTETICO,
    )
    briefing = profile.briefing()
    assert profile.level.briefing in briefing
    assert profile.depth.briefing in briefing
    assert "a suo agio con la matematica" in briefing
    assert "riga per riga" in briefing


def test_roundtrip_through_disk(tmp_path) -> None:
    profile = LearnerProfile(
        level=Level.AVANZATO,
        math_comfort=Comfort.MEDIA,
        python_comfort=Comfort.SOLIDA,
        depth=Depth.APPROFONDITO,
        background="ricercatore",
        goals="capire LoRA",
        known_topics=["transformer"],
    )
    save_profile(profile, tmp_path)
    assert load_profile(tmp_path) == profile


def test_missing_profile_returns_defaults(tmp_path) -> None:
    assert load_profile(tmp_path) == LearnerProfile()


def test_corrupt_or_partial_profile_degrades_to_defaults(tmp_path) -> None:
    """A hand-edited or older profile must not break the GUI on startup."""

    (tmp_path / "profile.json").write_text("{ not json", encoding="utf-8")
    assert load_profile(tmp_path) == LearnerProfile()

    (tmp_path / "profile.json").write_text(
        json.dumps({"level": "inventato", "known_topics": "non una lista"}),
        encoding="utf-8",
    )
    recovered = load_profile(tmp_path)
    assert recovered.level is Level.PRINCIPIANTE
    assert recovered.known_topics == []


def test_enums_serialise_as_plain_strings(tmp_path) -> None:
    """The JSON on disk should be readable/editable, not pickled enum reprs."""

    save_profile(LearnerProfile(level=Level.INTERMEDIO), tmp_path)
    data = json.loads((tmp_path / "profile.json").read_text(encoding="utf-8"))
    assert data["level"] == "intermedio"
