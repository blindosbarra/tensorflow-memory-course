from __future__ import annotations

import pandas as pd
import pytest

from memory_ai.data_cleaning import clean_memory_records, missing_summary


def test_missing_summary_counts_and_ratios() -> None:
    frame = pd.DataFrame({"a": [1, None, 3], "b": [None, "x", None]})

    summary = missing_summary(frame)

    assert summary.loc["a", "missing_count"] == 1
    assert summary.loc["a", "missing_ratio"] == pytest.approx(1 / 3)
    assert summary.loc["b", "missing_count"] == 2
    assert summary.loc["b", "missing_ratio"] == pytest.approx(2 / 3)


def test_clean_memory_records_drops_critical_missing_and_imputes_features() -> None:
    frame = pd.DataFrame(
        {
            "memory_id": ["mem_001", "mem_002", "mem_003"],
            "text": ["alpha", None, "gamma"],
            "timestamp": ["2026-07-01", "2026-07-02", "2026-07-03"],
            "type": ["episodic", "semantic", None],
            "importance": [0.2, 0.8, None],
        }
    )

    result = clean_memory_records(frame)

    assert result.report["rows_before"] == 3
    assert result.report["rows_after"] == 2
    assert result.report["dropped_rows"] == 1
    assert result.report["dropped_memory_ids"] == ["mem_002"]
    assert result.report["imputed"] == {"type": 1, "importance": 1}
    assert result.data["type"].to_list() == ["episodic", "unknown"]
    assert result.data["importance"].to_list() == [0.2, 0.2]
    assert result.data.isna().sum().sum() == 0


def test_clean_memory_records_rejects_missing_required_columns() -> None:
    frame = pd.DataFrame({"memory_id": ["mem_001"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        clean_memory_records(frame)
