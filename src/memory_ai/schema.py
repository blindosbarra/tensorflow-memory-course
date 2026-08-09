"""The `MemoryRecord` contract and its validation.

Lesson 52 defines this dataclass and a stub pipeline; lessons 54-58 fill the
stubs in one at a time. The record is the contract every component agrees on,
so it is extracted here rather than redefined in each capstone notebook.

Two decisions carried over from the lesson, both deliberate:

- the record keeps `embedding_dim`, not the embedding vector. A record is
  meant to be readable and JSON-serialisable in the lesson; the vector lives
  in the index that `memory_ai.embedding` builds.
- `validate` returns the list of problems instead of raising. Lesson 52 shows
  a record being checked and printed, and a validator that raised would stop
  the notebook on the first bad example instead of showing the reader what
  was wrong with it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

VALID_TYPES = ("episodic", "semantic", "preference")


@dataclass(frozen=True)
class MemoryRecord:
    """One processed memory, as every capstone component agrees to see it."""

    memory_id: str
    text: str
    timestamp: str | None = None
    type: str | None = None
    entities: tuple[str, ...] = ()
    topics: tuple[str, ...] = ()
    importance: float | None = None
    should_store: bool | None = None
    embedding_dim: int | None = None
    relations: tuple[dict[str, str], ...] = field(default_factory=tuple)

    def validate(self) -> list[str]:
        """Return every contract violation found, empty when the record is valid."""

        problems: list[str] = []
        if not self.memory_id:
            problems.append("memory_id mancante")
        if not self.text:
            problems.append("text mancante")
        if self.type is not None and self.type not in VALID_TYPES:
            problems.append(f"type non valido: {self.type}")
        if self.importance is not None and not 0.0 <= self.importance <= 1.0:
            problems.append("importance fuori [0,1]")
        if self.embedding_dim is not None and self.embedding_dim <= 0:
            problems.append(f"embedding_dim non positivo: {self.embedding_dim}")
        for relation in self.relations:
            missing = sorted({"source", "type", "target"}.difference(relation))
            if missing:
                problems.append(f"relazione senza {', '.join(missing)}: {relation}")
        return problems

    def is_valid(self) -> bool:
        """True when the record violates nothing in the contract."""

        return not self.validate()

    def to_dict(self) -> dict[str, object]:
        """Render the record as plain JSON-serialisable data.

        Tuples become lists so the output matches what the capstone notebooks
        print with `json.dumps`.
        """

        return {
            "memory_id": self.memory_id,
            "text": self.text,
            "timestamp": self.timestamp,
            "type": self.type,
            "entities": list(self.entities),
            "topics": list(self.topics),
            "importance": self.importance,
            "should_store": self.should_store,
            "embedding_dim": self.embedding_dim,
            "relations": [dict(relation) for relation in self.relations],
        }
