"""MemoryAILab, the pipeline that orchestrates lessons 54-56 (lesson 58/60).

Lesson 52 defines `MemoryRecord` and a stub pipeline; lessons 54-56 fill the
stubs one at a time (type classifier, entity/relation extraction, importance);
lesson 58 assembles the real components into `MemoryAILab.process`, and
lesson 60 adds an `archive` that only keeps what clears the storage
threshold, de-duplicated by `memory_id` so reprocessing the same memory is
idempotent.

Nothing here needs the entity/relation graph (lesson 55's adjacency-list
demo, itself dependency-free) or the hybrid retrieval score (lesson 28, a
core-curriculum lesson using a trained Keras embedding and `networkx`,
outside this item's file scope): neither is part of `MemoryAILab.process`
in the notebooks, so neither is a prerequisite for the pipeline to run.

`MemoryAILab` trains its own classifier on construction, mirroring the
notebooks' `lab = MemoryAILab()` exactly. That is still an explicit action
by the caller, not training at import time - the constraint decision D5 set
for `TypeClassifier.fit()`.
"""

from __future__ import annotations

from pathlib import Path

from memory_ai.classifier import DEFAULT_TRAIN_PATH, TypeClassifier
from memory_ai.embedding import DEFAULT_DIM
from memory_ai.importance import compute_importance
from memory_ai.schema import MemoryRecord
from memory_ai.text import extract_entities, extract_relations

DEFAULT_STORE_THRESHOLD = 0.4


class MemoryAILab:
    """Turns raw memory text into the full `MemoryRecord` and, maybe, archives it.

    `should_store` applies a threshold to importance - a product decision,
    not a statistical fact (lesson 58's own framing): 0.4 is not more
    "correct" than 0.5, it trades the cost of forgetting something important
    against the cost of archiving noise.
    """

    def __init__(
        self,
        store_threshold: float = DEFAULT_STORE_THRESHOLD,
        train_path: Path | str = DEFAULT_TRAIN_PATH,
    ) -> None:
        self.store_threshold = store_threshold
        self._classifier = TypeClassifier()
        self._classifier.fit(train_path)
        self.archive: list[MemoryRecord] = []

    @property
    def classifier(self) -> TypeClassifier:
        """The fitted classifier this lab uses, for inspection in tests and demos."""

        return self._classifier

    def process(self, memory_id: str, text: str, timestamp: str | None = None) -> MemoryRecord:
        """Classify, extract and score one memory, archiving it if it clears the bar.

        Archiving is idempotent in `memory_id`: processing the same memory
        twice does not duplicate it in `archive`, matching lesson 60's
        idempotent-processing property (the same guarantee RFC 7231 asks of
        idempotent HTTP methods).
        """

        importance = compute_importance(text)
        record = MemoryRecord(
            memory_id=memory_id,
            text=text,
            timestamp=timestamp,
            type=self._classifier.predict(text),
            entities=extract_entities(text),
            importance=importance,
            should_store=importance >= self.store_threshold,
            embedding_dim=DEFAULT_DIM,
            relations=extract_relations(text),
        )
        already_archived = any(existing.memory_id == memory_id for existing in self.archive)
        if record.should_store and not already_archived:
            self.archive.append(record)
        return record
