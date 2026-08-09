"""The composite importance score of lesson 25, as used by the capstone.

The score is a weighted sum of three readable signals rather than a learned
model, and that is the teaching point of lesson 25: every term can be
explained to the person whose memories are being scored, and a surprising
score can be traced back to the term that caused it.

The weights sum to 0.90 and a constant 0.10 floor is added, so a memory that
triggers nothing still scores 0.10 rather than 0. Nothing is worthless enough
to be exactly zero, and a zero would make the store threshold behave like a
special case.
"""

from __future__ import annotations

from dataclasses import dataclass

from memory_ai.text import extract_entities, tokenize

# Words that mark a stated preference or a strong claim.
STRONG_WORDS = frozenset(
    {"prefers", "likes", "dislikes", "hates", "loves", "always", "never", "important"}
)

LENGTH_WEIGHT = 0.30
STRONG_WEIGHT = 0.40
ENTITY_WEIGHT = 0.20
BASELINE = 0.10

LENGTH_SATURATION_WORDS = 15
ENTITY_SATURATION = 2


@dataclass(frozen=True)
class ImportanceBreakdown:
    """The score plus the three terms that produced it, for auditing."""

    score: float
    length_term: float
    strong_term: float
    entity_term: float
    strong_words_found: tuple[str, ...]
    entity_count: int


def importance_breakdown(text: str) -> ImportanceBreakdown:
    """Score a memory's importance and report which term contributed what.

    Each signal saturates: a very long memory is not endlessly more important
    than a long one, and a second entity helps while a fifth does not.
    """

    words = tokenize(text)
    strong_found = tuple(word for word in words if word in STRONG_WORDS)
    entity_count = len(extract_entities(text))

    length_term = LENGTH_WEIGHT * min(len(words) / LENGTH_SATURATION_WORDS, 1.0)
    strong_term = STRONG_WEIGHT * min(len(strong_found), 1)
    entity_term = ENTITY_WEIGHT * min(entity_count, ENTITY_SATURATION) / ENTITY_SATURATION

    total = min(length_term + strong_term + entity_term + BASELINE, 1.0)
    return ImportanceBreakdown(
        score=round(float(total), 2),
        length_term=length_term,
        strong_term=float(strong_term),
        entity_term=entity_term,
        strong_words_found=strong_found,
        entity_count=entity_count,
    )


def compute_importance(text: str) -> float:
    """Return the importance score in [0, 1], rounded to two decimals."""

    return importance_breakdown(text).score


def should_store(text: str, threshold: float = 0.4) -> bool:
    """Decide whether a memory clears the storage threshold."""

    return compute_importance(text) >= threshold
