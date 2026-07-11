"""Complete solution for the duplicates/types/outliers learner starter."""

import pandas as pd


def normalize_text(text: pd.Series) -> pd.Series:
    return text.astype("string").str.strip().str.casefold()


def duplicate_candidates(frame: pd.DataFrame) -> pd.Series:
    by_id = frame.duplicated("memory_id", keep="first")
    by_event = frame.duplicated(["text", "timestamp"], keep="first")
    normalized = frame.assign(_normalized_text=normalize_text(frame["text"]))
    by_normalized_event = normalized.duplicated(["_normalized_text", "timestamp"], keep="first")
    return by_id | by_event | by_normalized_event


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.loc[~duplicate_candidates(frame)].copy().reset_index(drop=True)
    numeric = pd.to_numeric(cleaned["importance"], errors="coerce")
    cleaned["importance_was_invalid_type"] = cleaned["importance"].notna() & numeric.isna()
    in_domain = numeric[numeric.between(0, 1)]
    cleaned["importance"] = numeric.fillna(in_domain.median())
    cleaned["importance_was_outlier"] = ~cleaned["importance"].between(0, 1)
    cleaned["importance"] = cleaned["importance"].clip(0, 1)
    return cleaned
