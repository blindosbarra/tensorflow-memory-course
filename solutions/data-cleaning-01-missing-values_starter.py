"""Complete solution for the missing-values learner starter."""

import pandas as pd

CRITICAL_COLUMNS = ("memory_id", "text", "timestamp")


def missing_rates(frame: pd.DataFrame) -> pd.Series:
    return frame.isna().mean()


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy().dropna(subset=list(CRITICAL_COLUMNS)).reset_index(drop=True)
    cleaned["type_was_missing"] = cleaned["type"].isna()
    cleaned["importance_was_missing"] = cleaned["importance"].isna()
    cleaned["type"] = cleaned["type"].fillna("unknown")
    cleaned["importance"] = cleaned["importance"].fillna(cleaned["importance"].median())
    return cleaned
