"""Hashing embeddings and cosine similarity search for the capstone.

Lesson 55 embeds a memory by hashing each word into one of `DEFAULT_DIM`
buckets and counting, then normalising to unit length. It is not a learned
embedding and the lesson says so: it exists because it needs no model, no
download and no training, so the retrieval mechanics stay visible.

Because the vectors are unit length, cosine similarity is a dot product, and
searching is one matrix multiply. That is the property lesson 18 establishes
and lesson 55 relies on, so `MemorySearchIndex` normalises on insert and
never again.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from memory_ai.text import tokenize

DEFAULT_DIM = 48


def embed(text: str, dim: int = DEFAULT_DIM) -> np.ndarray:
    """Embed text as a unit-length hashing bag of words.

    A text with no alphabetic words has no direction to point in, so it maps
    to the zero vector rather than to an arbitrary one. Its similarity to
    everything is then 0, which is the honest answer.
    """

    if dim <= 0:
        raise ValueError(f"dim must be positive, got {dim}")

    vector = np.zeros(dim, dtype="float64")
    for word in tokenize(text):
        vector[int.from_bytes(word.encode(), "little") % dim] += 1.0

    norm = float(np.linalg.norm(vector))
    return vector / norm if norm > 0 else vector


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    """Cosine similarity of two vectors, 0.0 when either has no direction."""

    left_norm = float(np.linalg.norm(left))
    right_norm = float(np.linalg.norm(right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return float(np.dot(left, right) / (left_norm * right_norm))


@dataclass(frozen=True)
class SearchHit:
    """One retrieved memory and how close it was to the query."""

    memory_id: str
    text: str
    score: float


class MemorySearchIndex:
    """A dense index over memory texts, searched by cosine similarity.

    Small on purpose: the capstone works at a scale where a full scan is
    instant, and an approximate index would hide the mechanism the lessons
    are there to show.
    """

    def __init__(self, dim: int = DEFAULT_DIM) -> None:
        if dim <= 0:
            raise ValueError(f"dim must be positive, got {dim}")
        self.dim = dim
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._vectors: list[np.ndarray] = []

    def __len__(self) -> int:
        return len(self._ids)

    def add(self, memory_id: str, text: str) -> None:
        """Add one memory, embedding it on the way in."""

        if not memory_id:
            raise ValueError("memory_id mancante")
        self._ids.append(memory_id)
        self._texts.append(text)
        self._vectors.append(embed(text, self.dim))

    def add_many(self, records: list[tuple[str, str]]) -> None:
        """Add several (memory_id, text) pairs in order."""

        for memory_id, text in records:
            self.add(memory_id, text)

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        """Return the closest memories to the query, best first.

        Ties keep insertion order, so a repeated run gives the same answer:
        the sort is stable and the scores are computed the same way every time.
        """

        if top_k <= 0:
            raise ValueError(f"top_k must be positive, got {top_k}")
        if not self._ids:
            return []

        matrix = np.vstack(self._vectors)
        scores = matrix @ embed(query, self.dim)
        order = sorted(range(len(scores)), key=lambda i: -float(scores[i]))
        return [
            SearchHit(self._ids[i], self._texts[i], round(float(scores[i]), 4))
            for i in order[:top_k]
        ]
