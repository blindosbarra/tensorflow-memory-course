"""Small data-quality utilities for duplicate, type, and outlier checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_QUALITY_COLUMNS = ("memory_id", "text", "timestamp", "type", "importance")


@dataclass(frozen=True)
class QualityResult:
    """Cleaned records plus a small data-quality report."""

    data: pd.DataFrame
    report: dict[str, Any]


def duplicate_memory_mask(frame: pd.DataFrame) -> pd.Series:
    """Mark repeated memories after the first occurrence."""

    required = {"memory_id", "text", "timestamp"}
    missing_columns = sorted(required.difference(frame.columns))
    if missing_columns:
        joined = ", ".join(missing_columns)
        msg = f"Missing required columns: {joined}"
        raise ValueError(msg)

    duplicated_id = frame.duplicated(subset=["memory_id"], keep="first")
    duplicated_event = frame.duplicated(subset=["text", "timestamp"], keep="first")
    return duplicated_id | duplicated_event


def coerce_importance(frame: pd.DataFrame, fallback: float = 0.0) -> pd.DataFrame:
    """Convert importance to float and flag values that were not numeric."""

    if "importance" not in frame.columns:
        raise ValueError("Missing required columns: importance")

    working = frame.copy()
    raw_importance = working["importance"]
    numeric_importance = pd.to_numeric(raw_importance, errors="coerce")
    invalid_mask = raw_importance.notna() & numeric_importance.isna()

    working["importance_was_invalid_type"] = invalid_mask
    working["importance"] = numeric_importance.fillna(fallback).astype("float64")
    return working


def flag_and_clip_importance_outliers(
    frame: pd.DataFrame,
    lower: float = 0.0,
    upper: float = 1.0,
) -> pd.DataFrame:
    """Flag importance values outside the local domain range and clip them."""

    if "importance" not in frame.columns:
        raise ValueError("Missing required columns: importance")

    working = frame.copy()
    outlier_mask = working["importance"].lt(lower) | working["importance"].gt(upper)
    working["importance_was_outlier"] = outlier_mask
    working["importance"] = working["importance"].clip(lower=lower, upper=upper)
    return working


def clean_memory_quality_issues(frame: pd.DataFrame) -> QualityResult:
    """Remove duplicate memory rows and normalize the importance column."""

    missing_columns = sorted(set(REQUIRED_QUALITY_COLUMNS).difference(frame.columns))
    if missing_columns:
        joined = ", ".join(missing_columns)
        msg = f"Missing required columns: {joined}"
        raise ValueError(msg)

    working = frame.copy().convert_dtypes()
    rows_before = len(working)
    duplicate_mask = duplicate_memory_mask(working)
    duplicate_memory_ids = working.loc[duplicate_mask, "memory_id"].astype("string").to_list()

    deduplicated = working.loc[duplicate_mask.eq(False)].reset_index(drop=True).copy()
    typed = coerce_importance(deduplicated)
    cleaned = flag_and_clip_importance_outliers(typed)

    report: dict[str, Any] = {
        "rows_before": rows_before,
        "rows_after": len(cleaned),
        "duplicates_removed": int(duplicate_mask.sum()),
        "duplicate_memory_ids": duplicate_memory_ids,
        "invalid_importance_values": int(cleaned["importance_was_invalid_type"].sum()),
        "importance_outliers": int(cleaned["importance_was_outlier"].sum()),
        "importance_min": float(cleaned["importance"].min()) if len(cleaned) else None,
        "importance_max": float(cleaned["importance"].max()) if len(cleaned) else None,
    }
    return QualityResult(data=cleaned, report=report)


def clean_memory_quality_csv(input_path: Path, output_path: Path) -> QualityResult:
    """Read, clean, and persist a memory-quality CSV."""

    frame = pd.read_csv(input_path)
    result = clean_memory_quality_issues(frame)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.data.to_csv(output_path, index=False)
    return result
