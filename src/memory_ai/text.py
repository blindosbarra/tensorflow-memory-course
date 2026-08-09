"""Tokenisation, entity extraction and rule-based relation extraction.

Extracted from the capstone notebooks (lessons 55 and 56), where the same
three helpers were redefined cell by cell. They are deliberately small and
rule-based: the point of those lessons is that a readable rule you can debug
beats an opaque model you cannot, at the scale this course works at.

The limits are real and stated rather than hidden. `extract_entities` finds
capitalised words, so it also finds a capitalised common noun at the start of
a sentence — hence `STOPWORD_ENTITIES`. `extract_relations` returns at most
one relation per text, because the corpus sentences carry one.
"""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[a-zA-Z]+")
CAPITALISED_RE = re.compile(r"\b[A-Z][a-zA-Z]+\b")

# Capitalised words that are not entities: sentence openers, mostly.
STOPWORD_ENTITIES = frozenset({"The", "A", "User"})

# Surface verb -> normalised relation type.
RELATION_VERBS: dict[str, str] = {
    "visited": "visited",
    "met": "met",
    "likes": "likes",
    "prefers": "prefers",
    "works": "works_at",
    "lives": "lives_in",
}


def tokenize(text: str) -> list[str]:
    """Split text into lowercase alphabetic words, dropping everything else."""

    return WORD_RE.findall(str(text).lower())


def extract_entities(text: str) -> tuple[str, ...]:
    """Return capitalised words that are plausibly entities, in order of appearance.

    Repeats are kept. This mirrors the capstone notebooks exactly, and the
    extraction deliberately did not change it: `memory_ai.importance` counts
    the result, so de-duplicating here would silently move importance scores
    the lessons print. Whether a name mentioned twice should count once is a
    question for the course author, not for a refactor.
    """

    return tuple(
        word
        for word in CAPITALISED_RE.findall(str(text))
        if word not in STOPWORD_ENTITIES
    )


def extract_relations(text: str) -> tuple[dict[str, str], ...]:
    """Return the subject-verb-object relations found, by surface verb match.

    Needs at least two entities: a relation with nothing to point at is not a
    relation. Returns an empty tuple when no rule fires, which is the honest
    answer for a sentence this small ruleset does not cover.
    """

    entities = extract_entities(text)
    if len(entities) < 2:
        return ()

    lowered = str(text).lower()
    for surface, normalised in RELATION_VERBS.items():
        if surface in lowered:
            return ({"source": entities[0], "type": normalised, "target": entities[1]},)
    return ()
