"""Tests for `lesson_agent.runner` — the session seeding, without calling an LLM.

The valuable test here is `test_every_agent_placeholder_is_seeded`. ADK
resolves `{placeholder}` in an agent's `instruction` against session state
**at call time**, so a placeholder nobody seeded fails in the middle of a
paid, minutes-long run rather than at import. Adding a `{learner_profile}`
to one more agent and forgetting to seed it is exactly the mistake this
catches for free.
"""

from __future__ import annotations

import re

import pytest

from lesson_agent import agents
from lesson_agent.profile import LearnerProfile, Level
from lesson_agent.read_notebook import NOTEBOOKS_DIR, read_lesson_context
from lesson_agent.runner import NO_FOCUS, build_initial_state
from lesson_agent.tutor import TUTOR_INSTRUCTION

# Placeholders written into state by an *upstream* agent's `output_key`
# rather than seeded before the run.
AGENT_OUTPUT_KEYS = {"info_brief", "math", "code", "writer", "validator"}

# What `TutorSession.create` seeds. Kept as a literal rather than imported so
# that dropping a key there fails this test instead of silently agreeing.
TUTOR_SEEDED = {"lesson_context", "learner_profile"}

_PLACEHOLDER_RE = re.compile(r"\{([a-z_]+)\}")


@pytest.fixture(scope="module")
def context():
    return read_lesson_context(NOTEBOOKS_DIR / "lezione-58-capstone-pipeline.ipynb")


def test_every_agent_placeholder_is_seeded_or_produced_upstream(context) -> None:
    seeded = set(build_initial_state(context, LearnerProfile()))
    known = seeded | AGENT_OUTPUT_KEYS

    workflow_agents = [
        agents.gather_info_agent,
        agents.math_agent,
        agents.code_agent,
        agents.writer_agent,
        agents.validator_agent,
    ]
    for agent in workflow_agents:
        placeholders = set(_PLACEHOLDER_RE.findall(str(agent.instruction)))
        unresolved = placeholders - known
        assert not unresolved, (
            f"{agent.name} usa {sorted(unresolved)}, che nessuno mette in "
            "session state: la run fallirebbe a metà pipeline."
        )


def test_tutor_placeholders_are_seeded_by_its_session() -> None:
    placeholders = set(_PLACEHOLDER_RE.findall(TUTOR_INSTRUCTION))
    assert placeholders <= TUTOR_SEEDED, (
        f"il tutor usa {sorted(placeholders - TUTOR_SEEDED)}, che "
        "`TutorSession.create` non mette in session state."
    )


def test_initial_state_carries_the_learner_into_the_prompt(context) -> None:
    state = build_initial_state(context, LearnerProfile(level=Level.AVANZATO))
    assert "Salta le basi" in state["learner_profile"]
    assert state["lesson_context"].startswith("# Lezione: capstone-pipeline")


def test_absent_focus_becomes_an_instruction_not_an_empty_string(context) -> None:
    """An empty placeholder reads as a truncated prompt; a sentence doesn't."""

    assert build_initial_state(context, LearnerProfile(), focus="")["learner_focus"] == NO_FOCUS
    assert build_initial_state(context, LearnerProfile(), focus="   ")["learner_focus"] == NO_FOCUS


def test_focus_is_passed_through_verbatim(context) -> None:
    focus = "perche' il decadimento e' esponenziale e non lineare?"
    assert build_initial_state(context, LearnerProfile(), focus=focus)["learner_focus"] == focus


def test_two_profiles_produce_different_state(context) -> None:
    """If this ever stops holding, personalisation has silently stopped working."""

    beginner = build_initial_state(context, LearnerProfile(level=Level.PRINCIPIANTE))
    expert = build_initial_state(context, LearnerProfile(level=Level.AVANZATO))
    assert beginner["learner_profile"] != expert["learner_profile"]
    assert beginner["lesson_context"] == expert["lesson_context"]
