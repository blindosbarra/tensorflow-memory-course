"""Tests for the composite importance score."""

from memory_ai.importance import (
    BASELINE,
    compute_importance,
    importance_breakdown,
    should_store,
)


def test_score_stays_in_the_unit_range() -> None:
    texts = [
        "",
        "ciao",
        "Marco visited Glasgow with his son on a long and detailed afternoon trip",
        "The user always prefers morning meetings with Marco and Elena in Torino",
    ]
    for text in texts:
        assert 0.0 <= compute_importance(text) <= 1.0


def test_empty_memory_scores_the_baseline_not_zero() -> None:
    assert compute_importance("") == BASELINE


def test_strong_word_raises_the_score() -> None:
    plain = compute_importance("the user had a meeting")
    strong = compute_importance("the user prefers a meeting")
    assert strong > plain


def test_strong_term_saturates_at_one_word() -> None:
    one = importance_breakdown("the user prefers meetings")
    many = importance_breakdown("the user prefers and likes and loves meetings")
    assert one.strong_term == many.strong_term


def test_entities_raise_the_score_and_saturate() -> None:
    two = importance_breakdown("Marco met Elena")
    four = importance_breakdown("Marco met Elena and Lucia and Giorgio")
    assert two.entity_term == four.entity_term
    assert four.entity_count > two.entity_count


def test_breakdown_terms_reconstruct_the_score() -> None:
    breakdown = importance_breakdown("Marco always prefers Glasgow in the morning")
    total = (
        breakdown.length_term
        + breakdown.strong_term
        + breakdown.entity_term
        + BASELINE
    )
    assert breakdown.score == round(min(total, 1.0), 2)


def test_breakdown_names_the_strong_words_found() -> None:
    breakdown = importance_breakdown("the user always prefers mornings")
    assert set(breakdown.strong_words_found) == {"always", "prefers"}


def test_should_store_follows_the_threshold() -> None:
    text = "The user always prefers morning meetings with Marco in Torino"
    score = compute_importance(text)
    assert should_store(text, threshold=score)
    assert not should_store(text, threshold=score + 0.01)


def test_score_is_deterministic() -> None:
    text = "Marco visited Glasgow with his son."
    assert compute_importance(text) == compute_importance(text)
