"""Complete solution for the duplicates/types/outliers learner starter."""

import pandas as pd


def normalize_station(station: pd.Series) -> pd.Series:
    return station.astype("string").str.strip().str.casefold()


def duplicate_candidates(frame: pd.DataFrame) -> pd.Series:
    by_id = frame.duplicated("reading_id", keep="first")
    by_event = frame.duplicated(["station_id", "recorded_at"], keep="first")
    normalized = frame.assign(_normalized_station=normalize_station(frame["station_id"]))
    by_normalized_event = normalized.duplicated(
        ["_normalized_station", "recorded_at"], keep="first"
    )
    return by_id | by_event | by_normalized_event


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.loc[~duplicate_candidates(frame)].copy().reset_index(drop=True)
    numeric = pd.to_numeric(cleaned["temperature_c"], errors="coerce")
    cleaned["temperature_was_invalid_type"] = cleaned["temperature_c"].notna() & numeric.isna()
    in_domain = numeric[numeric.between(-50, 60)]
    cleaned["temperature_c"] = numeric.fillna(in_domain.median())
    cleaned["temperature_was_domain_outlier"] = ~cleaned["temperature_c"].between(-50, 60)
    cleaned["temperature_c"] = cleaned["temperature_c"].clip(-50, 60)
    return cleaned
