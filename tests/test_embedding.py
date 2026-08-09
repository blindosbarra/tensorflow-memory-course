"""Tests for hashing embeddings and cosine similarity search."""

import numpy as np
import pytest

from memory_ai.embedding import (
    DEFAULT_DIM,
    MemorySearchIndex,
    cosine_similarity,
    embed,
)


def test_embedding_has_the_requested_dimension() -> None:
    assert embed("Marco visited Glasgow").shape == (DEFAULT_DIM,)
    assert embed("Marco visited Glasgow", dim=16).shape == (16,)


def test_embedding_is_unit_length() -> None:
    vector = embed("Marco visited Glasgow with his son")
    assert np.isclose(np.linalg.norm(vector), 1.0)


def test_text_without_words_maps_to_the_zero_vector() -> None:
    vector = embed("12345 !!!")
    assert np.allclose(vector, 0.0)


def test_embedding_is_deterministic() -> None:
    assert np.array_equal(embed("Marco visited Glasgow"), embed("Marco visited Glasgow"))


def test_non_positive_dim_is_rejected() -> None:
    with pytest.raises(ValueError, match="dim must be positive"):
        embed("ciao", dim=0)


def test_cosine_similarity_of_identical_texts_is_one() -> None:
    vector = embed("Marco visited Glasgow")
    assert np.isclose(cosine_similarity(vector, vector), 1.0)


def test_cosine_similarity_with_a_zero_vector_is_zero() -> None:
    assert cosine_similarity(embed("Marco"), np.zeros(DEFAULT_DIM)) == 0.0


def test_empty_index_returns_no_hits() -> None:
    assert MemorySearchIndex().search("Marco") == []
    assert len(MemorySearchIndex()) == 0


def test_index_retrieves_the_matching_memory_first() -> None:
    index = MemorySearchIndex()
    index.add_many(
        [
            ("mem_001", "Marco visited Glasgow with his son"),
            ("mem_002", "the user prefers morning meetings"),
            ("mem_003", "Elena works in Torino"),
        ]
    )
    assert len(index) == 3
    hits = index.search("Marco visited Glasgow with his son", top_k=1)
    assert hits[0].memory_id == "mem_001"
    assert np.isclose(hits[0].score, 1.0)


def test_search_returns_at_most_top_k_sorted_descending() -> None:
    index = MemorySearchIndex()
    index.add_many([(f"mem_{i:03d}", f"memory number {i} about Glasgow") for i in range(5)])
    hits = index.search("Glasgow", top_k=3)
    assert len(hits) == 3
    assert [h.score for h in hits] == sorted((h.score for h in hits), reverse=True)


def test_search_is_deterministic_across_calls() -> None:
    index = MemorySearchIndex()
    index.add_many([("a", "Marco visited Glasgow"), ("b", "Elena works in Torino")])
    assert index.search("Glasgow") == index.search("Glasgow")


def test_empty_memory_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="memory_id mancante"):
        MemorySearchIndex().add("", "ciao")


def test_non_positive_top_k_is_rejected() -> None:
    index = MemorySearchIndex()
    index.add("mem_001", "ciao")
    with pytest.raises(ValueError, match="top_k must be positive"):
        index.search("ciao", top_k=0)
