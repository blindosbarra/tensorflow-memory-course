from __future__ import annotations

import pandas as pd
import pytest

from memory_ai.data_quality import (
    clean_memory_quality_issues,
    coerce_importance,
    duplicate_memory_mask,
    flag_and_clip_importance_outliers,
)


def test_duplicate_memory_mask_marks_repeated_id_or_event() -> None:
    frame = pd.DataFrame(
        {
            "memory_id": ["mem_001", "mem_001", "mem_003", "mem_004"],
            "text": ["alpha", "alpha", "beta", "beta"],
            "timestamp": ["2026-07-01", "2026-07-01", "2026-07-02", "2026-07-02"],
        }
    )

    mask = duplicate_memory_mask(frame)

    assert mask.to_list() == [False, True, False, True]


def test_coerce_importance_flags_invalid_text_values() -> None:
    frame = pd.DataFrame({"importance": ["0.4", "high", None]})

    result = coerce_importance(frame)

    assert result["importance"].to_list() == [0.4, 0.0, 0.0]
    assert result["importance_was_invalid_type"].to_list() == [False, True, False]


def test_flag_and_clip_importance_outliers_uses_domain_range() -> None:
    frame = pd.DataFrame({"importance": [-0.2, 0.5, 1.7]})

    result = flag_and_clip_importance_outliers(frame)

    assert result["importance"].to_list() == [0.0, 0.5, 1.0]
    assert result["importance_was_outlier"].to_list() == [True, False, True]


def test_clean_memory_quality_issues_reports_all_decisions() -> None:
    frame = pd.DataFrame(
        {
            "memory_id": ["mem_001", "mem_001", "mem_002", "mem_003", "mem_004"],
            "text": ["alpha", "alpha", "beta", "gamma", "delta"],
            "timestamp": [
                "2026-07-01",
                "2026-07-01",
                "2026-07-02",
                "2026-07-03",
                "2026-07-04",
            ],
            "type": ["episodic", "episodic", "semantic", "preference", "episodic"],
            "importance": ["0.5", "0.5", "high", "1.4", "-0.1"],
        }
    )

    result = clean_memory_quality_issues(frame)

    assert result.report["rows_before"] == 5
    assert result.report["rows_after"] == 4
    assert result.report["duplicates_removed"] == 1
    assert result.report["duplicate_memory_ids"] == ["mem_001"]
    assert result.report["invalid_importance_values"] == 1
    assert result.report["importance_outliers"] == 2
    assert result.data["importance"].to_list() == [0.5, 0.0, 1.0, 0.0]


def test_clean_memory_quality_issues_rejects_missing_columns() -> None:
    frame = pd.DataFrame({"memory_id": ["mem_001"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        clean_memory_quality_issues(frame)
