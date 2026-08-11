"""Tests for MemoryAILab, the pipeline of lesson 58/60.

`test_matches_lesson_60_on_its_own_example_stream` is the parity check: it
runs lesson 60's exact four-memory demo through an independent
reimplementation of its cells and compares every field of every record
against `MemoryAILab`.
"""

from __future__ import annotations

from pathlib import Path

from memory_ai.classifier import TYPES
from memory_ai.embedding import DEFAULT_DIM
from memory_ai.pipeline import DEFAULT_STORE_THRESHOLD, MemoryAILab
from memory_ai.schema import MemoryRecord

TRAIN_CSV = Path(__file__).resolve().parents[1] / "datasets" / "processed" / "memory_train.csv"


def test_process_returns_a_valid_memory_record() -> None:
    lab = MemoryAILab()
    record = lab.process("mem_001", "Marco visited Glasgow with his son.", "2026-07-03")
    assert isinstance(record, MemoryRecord)
    assert record.validate() == []


def test_process_populates_every_component() -> None:
    lab = MemoryAILab()
    record = lab.process("mem_001", "Marco visited Glasgow with his son.", "2026-07-03")
    assert record.type in TYPES
    assert record.entities == ("Marco", "Glasgow")
    assert record.relations == ({"source": "Marco", "type": "visited", "target": "Glasgow"},)
    assert 0.0 <= record.importance <= 1.0  # type: ignore[operator]
    assert record.embedding_dim == DEFAULT_DIM
    assert isinstance(record.should_store, bool)


def test_should_store_follows_the_threshold() -> None:
    # "ok." carries no signal: length, strong words and entities all near
    # zero, so its importance sits well under the default 0.4 threshold.
    lab = MemoryAILab()
    record = lab.process("mem_low", "ok.")
    assert not record.should_store
    assert record.importance is not None and record.importance < DEFAULT_STORE_THRESHOLD


def test_only_stored_records_reach_the_archive() -> None:
    lab = MemoryAILab()
    stored = lab.process("mem_001", "Marco visited Glasgow with his son.")
    skipped = lab.process("mem_002", "ok.")
    assert stored in lab.archive
    assert skipped not in lab.archive


def test_processing_is_idempotent_in_memory_id() -> None:
    # lesson 60: reprocessing the same memory_id does not duplicate the archive.
    lab = MemoryAILab()
    lab.process("mem_001", "Marco visited Glasgow with his son.")
    lab.process("mem_001", "Marco visited Glasgow with his son.")
    assert len(lab.archive) == 1


def test_custom_store_threshold_is_respected() -> None:
    permissive = MemoryAILab(store_threshold=0.0)
    strict = MemoryAILab(store_threshold=1.01)
    assert permissive.process("mem_001", "ok.").should_store
    assert not strict.process("mem_001", "Marco always prefers Glasgow deeply").should_store


def test_classifier_is_fitted_and_reachable() -> None:
    lab = MemoryAILab()
    assert lab.classifier.is_fitted


def test_matches_lesson_60_on_its_own_example_stream() -> None:
    """Reimplements lesson 60's cells independently and compares every field."""

    import re

    import numpy as np
    import pandas as pd

    types = ["episodic", "semantic", "preference"]
    type_index = {t: i for i, t in enumerate(types)}
    train = pd.read_csv(TRAIN_CSV)
    train = train[train["type"].isin(types)].reset_index(drop=True)

    def tok(text: str) -> list[str]:
        return re.findall(r"[a-zA-Z]+", str(text).lower())

    vocab: dict[str, int] = {}
    for text in train["text"]:
        for word in tok(text):
            vocab.setdefault(word, len(vocab))

    def bow(text: str) -> np.ndarray:
        vector = np.zeros(len(vocab))
        for word in tok(text):
            if word in vocab:
                vector[vocab[word]] += 1.0
        return vector

    def softmax(z: np.ndarray) -> np.ndarray:
        shifted = z - z.max(axis=1, keepdims=True)
        exp = np.exp(shifted)
        return exp / exp.sum(axis=1, keepdims=True)

    x_train = np.vstack([bow(t) for t in train["text"]])
    y_train = np.array([type_index[t] for t in train["type"]])
    weights = np.zeros((len(vocab), len(types)))
    bias = np.zeros(len(types))
    y_onehot = np.eye(len(types))[y_train]
    for _ in range(300):
        probabilities = softmax(x_train @ weights + bias)
        weights -= 0.5 * (x_train.T @ (probabilities - y_onehot) / len(x_train) + 1e-3 * weights)
        bias -= 0.5 * (probabilities - y_onehot).mean(axis=0)

    def classifica_tipo(text: str) -> str:
        return types[int(softmax(bow(text)[None, :] @ weights + bias).argmax())]

    def estrai_entita(text: str) -> list[str]:
        return [w for w in re.findall(r"\b[A-Z][a-zA-Z]+\b", str(text)) if w not in {"The", "A", "User"}]

    verbs = {
        "visited": "visited", "met": "met", "likes": "likes",
        "prefers": "prefers", "works": "works_at", "lives": "lives_in",
    }

    def estrai_relazioni(text: str) -> list[dict[str, str]]:
        entities = estrai_entita(text)
        for surface, normalised in verbs.items():
            if surface in text.lower() and len(entities) >= 2:
                return [{"source": entities[0], "type": normalised, "target": entities[1]}]
        return []

    strong = {"prefers", "likes", "dislikes", "hates", "loves", "always", "never", "important"}

    def calcola_importanza(text: str) -> float:
        words = tok(text)
        strong_count = sum(1 for w in words if w in strong)
        length_term = min(len(words) / 15.0, 1.0)
        entity_count = len(estrai_entita(text))
        value = 0.30 * length_term + 0.40 * min(strong_count, 1) + 0.20 * min(entity_count, 2) / 2 + 0.10
        return round(float(min(value, 1.0)), 2)

    reference_archive: list[dict[str, object]] = []

    def reference_process(memory_id: str, text: str, timestamp: str | None) -> dict[str, object]:
        importance = calcola_importanza(text)
        record = {
            "memory_id": memory_id, "text": text, "timestamp": timestamp,
            "type": classifica_tipo(text), "entities": estrai_entita(text),
            "importance": importance, "should_store": importance >= 0.4,
            "embedding_dim": 48, "relations": estrai_relazioni(text),
        }
        already = any(r["memory_id"] == memory_id for r in reference_archive)
        if record["should_store"] and not already:
            reference_archive.append(record)
        return record

    memories = [
        ("mem_001", "Marco visited Glasgow with his son.", "2026-07-03"),
        ("mem_002", "The user prefers morning sessions.", "2026-07-04"),
        ("mem_003", "Water boils at 100 degrees.", "2026-07-05"),
        ("mem_004", "ok.", "2026-07-06"),
    ]

    lab = MemoryAILab()
    for memory_id, text, timestamp in memories:
        reference = reference_process(memory_id, text, timestamp)
        record = lab.process(memory_id, text, timestamp)
        assert record.type == reference["type"]
        assert list(record.entities) == reference["entities"]
        assert record.importance == reference["importance"]
        assert record.should_store == reference["should_store"]
        assert record.embedding_dim == reference["embedding_dim"]
        assert [dict(r) for r in record.relations] == reference["relations"]

    assert len(lab.archive) == len(reference_archive)
