"""Tests for the MemoryRecord contract."""

from memory_ai.schema import MemoryRecord


def test_minimal_record_is_valid() -> None:
    record = MemoryRecord(memory_id="mem_001", text="Marco visited Glasgow.")
    assert record.validate() == []
    assert record.is_valid()


def test_missing_identity_fields_are_reported() -> None:
    record = MemoryRecord(memory_id="", text="")
    assert record.validate() == ["memory_id mancante", "text mancante"]


def test_invalid_type_is_reported() -> None:
    record = MemoryRecord(memory_id="mem_001", text="ciao", type="procedural")
    assert record.validate() == ["type non valido: procedural"]


def test_importance_outside_unit_range_is_reported() -> None:
    for bad in (-0.1, 1.5):
        record = MemoryRecord(memory_id="mem_001", text="ciao", importance=bad)
        assert record.validate() == ["importance fuori [0,1]"]


def test_importance_at_the_boundaries_is_accepted() -> None:
    for good in (0.0, 1.0):
        record = MemoryRecord(memory_id="mem_001", text="ciao", importance=good)
        assert record.validate() == []


def test_non_positive_embedding_dim_is_reported() -> None:
    record = MemoryRecord(memory_id="mem_001", text="ciao", embedding_dim=0)
    assert record.validate() == ["embedding_dim non positivo: 0"]


def test_relation_missing_fields_is_reported() -> None:
    record = MemoryRecord(
        memory_id="mem_001",
        text="ciao",
        relations=({"source": "Marco"},),
    )
    problems = record.validate()
    assert len(problems) == 1
    assert problems[0].startswith("relazione senza target, type")


def test_problems_accumulate() -> None:
    record = MemoryRecord(memory_id="", text="ciao", type="nope", importance=9.0)
    assert len(record.validate()) == 3


def test_to_dict_carries_the_whole_contract() -> None:
    record = MemoryRecord(
        memory_id="mem_001",
        text="Marco visited Glasgow.",
        timestamp="2026-07-03",
        type="episodic",
        entities=("Marco", "Glasgow"),
        importance=0.62,
        should_store=True,
        embedding_dim=48,
        relations=({"source": "Marco", "type": "visited", "target": "Glasgow"},),
    )
    payload = record.to_dict()
    assert set(payload) == {
        "memory_id", "text", "timestamp", "type", "entities",
        "topics", "importance", "should_store", "embedding_dim", "relations",
    }
    # tuples become lists so json.dumps produces what the notebooks print
    assert payload["entities"] == ["Marco", "Glasgow"]
    assert payload["relations"] == [
        {"source": "Marco", "type": "visited", "target": "Glasgow"}
    ]
