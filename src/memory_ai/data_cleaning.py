"""Small missing-value utilities used by the first data-cleaning lesson."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

CRITICAL_COLUMNS = ("memory_id", "text", "timestamp")


@dataclass(frozen=True)
class CleaningResult:
    """Cleaned memory records plus an auditable report."""

    data: pd.DataFrame
    report: dict[str, Any]


def missing_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Return count and ratio of missing values for each column."""

    row_count = len(frame)
    missing_count = frame.isna().sum()
    ratio = missing_count / row_count if row_count else missing_count
    return pd.DataFrame(
        {
            "missing_count": missing_count.astype("int64"),
            "missing_ratio": ratio.astype("float64"),
        }
    )


def clean_memory_records(frame: pd.DataFrame) -> CleaningResult:
    """Drop records without critical fields and impute low-risk fields.

    `memory_id`, `text`, and `timestamp` identify what happened and when. The
    lesson treats them as critical: if one is missing, the row is excluded.
    `type` and `importance` are useful features, so the function imputes them and
    records explicit flags.
    """

    required = set(CRITICAL_COLUMNS).union({"type", "importance"})
    missing_columns = sorted(required.difference(frame.columns))
    if missing_columns:
        joined = ", ".join(missing_columns)
        msg = f"Missing required columns: {joined}"
        raise ValueError(msg)

    working = frame.copy().convert_dtypes()
    before = missing_summary(working)
    rows_before = len(working)

    valid_mask = working.loc[:, list(CRITICAL_COLUMNS)].notna().all(axis="columns")
    invalid_mask = valid_mask.eq(False)
    dropped_memory_ids = (
        working.loc[invalid_mask, ["memory_id"]]["memory_id"].astype("string").fillna("<missing>")
    )
    cleaned = working.loc[valid_mask].reset_index(drop=True).copy()

    cleaned["type_was_missing"] = cleaned["type"].isna()
    cleaned["importance_was_missing"] = cleaned["importance"].isna()

    type_imputer = SimpleImputer(strategy="constant", fill_value="unknown")
    type_values = cleaned[["type"]].astype("object").where(cleaned[["type"]].notna(), np.nan)
    cleaned[["type"]] = type_imputer.fit_transform(type_values)

    importance_values = pd.to_numeric(cleaned["importance"], errors="coerce").astype("float64").to_frame()
    importance_imputer = SimpleImputer(strategy="median")
    cleaned[["importance"]] = importance_imputer.fit_transform(importance_values)
    cleaned["importance"] = cleaned["importance"].astype("float64")

    after = missing_summary(cleaned)
    report: dict[str, Any] = {
        "rows_before": rows_before,
        "rows_after": len(cleaned),
        "dropped_rows": rows_before - len(cleaned),
        "dropped_memory_ids": dropped_memory_ids.to_list(),
        "missing_before": before["missing_count"].to_dict(),
        "missing_after": after["missing_count"].to_dict(),
        "imputed": {
            "type": int(cleaned["type_was_missing"].sum()),
            "importance": int(cleaned["importance_was_missing"].sum()),
        },
    }
    return CleaningResult(data=cleaned, report=report)


def clean_memory_csv(input_path: Path, output_path: Path) -> CleaningResult:
    """Read, clean, and persist a small memory-record CSV."""

    frame = pd.read_csv(input_path)
    result = clean_memory_records(frame)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.data.to_csv(output_path, index=False)
    return result
