"""Complete solution for the missing-values learner starter."""

import pandas as pd

CRITICAL_COLUMNS = ("reading_id", "station_id", "recorded_at")


def missing_rates(frame: pd.DataFrame) -> pd.Series:
    return frame.isna().mean()


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy().dropna(subset=list(CRITICAL_COLUMNS)).reset_index(drop=True)
    cleaned["temperature_was_missing"] = cleaned["temperature_c"].isna()
    cleaned["humidity_was_missing"] = cleaned["humidity_pct"].isna()
    cleaned["temperature_c"] = cleaned["temperature_c"].fillna(
        cleaned["temperature_c"].median()
    )
    cleaned["humidity_pct"] = cleaned["humidity_pct"].fillna(cleaned["humidity_pct"].median())
    return cleaned
