"""Tests for tokenisation, entity extraction and relation extraction."""

from memory_ai.text import extract_entities, extract_relations, tokenize


def test_tokenize_lowercases_and_drops_punctuation() -> None:
    assert tokenize("Marco visited Glasgow, twice!") == [
        "marco", "visited", "glasgow", "twice",
    ]


def test_tokenize_drops_digits() -> None:
    # the corpus carries dates and ids; the bag of words is alphabetic only
    assert tokenize("meeting on 2026-07-03") == ["meeting", "on"]


def test_tokenize_accepts_non_string_input() -> None:
    assert tokenize(None) == ["none"]


def test_extract_entities_finds_capitalised_words() -> None:
    assert extract_entities("Marco visited Glasgow with his son.") == ("Marco", "Glasgow")


def test_extract_entities_drops_sentence_openers() -> None:
    # "The" opens the sentence and is capitalised, but is not an entity
    assert extract_entities("The user met Elena.") == ("Elena",)


def test_extract_entities_keeps_repeats() -> None:
    # deliberate: the capstone counts this result, so de-duplicating here
    # would move the importance scores the lessons print
    assert extract_entities("Marco met Elena. Marco likes Elena.") == (
        "Marco", "Elena", "Marco", "Elena",
    )


def test_extract_relations_reads_subject_verb_object() -> None:
    assert extract_relations("Marco visited Glasgow with his son.") == (
        {"source": "Marco", "type": "visited", "target": "Glasgow"},
    )


def test_relation_verbs_are_normalised() -> None:
    assert extract_relations("Elena works in Torino.")[0]["type"] == "works_at"
    assert extract_relations("Lucia lives in Bologna.")[0]["type"] == "lives_in"


def test_no_relation_without_two_entities() -> None:
    assert extract_relations("Marco visited the shop.") == ()


def test_no_relation_when_no_rule_fires() -> None:
    assert extract_relations("Marco forgot Glasgow entirely.") == ()
