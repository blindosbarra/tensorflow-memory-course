"""Starter: complete every TODO, then run the dedicated tests."""

import pandas as pd

CRITICAL_COLUMNS = ("reading_id", "station_id", "recorded_at")


def missing_rates(frame: pd.DataFrame) -> pd.Series:
    """Return the missing fraction for every column."""
    # TODO: calculate one rate per column.
    raise NotImplementedError


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing critical fields and impute the remaining fields."""
    # TODO: work on a copy; do not mutate frame.
    # TODO: drop rows missing a critical field.
    # TODO: add temperature_was_missing and humidity_was_missing before imputation.
    # TODO: fill both measurements with the survivors' column median.
    raise NotImplementedError
