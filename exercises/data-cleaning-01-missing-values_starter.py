"""Starter: complete every TODO, then run the dedicated tests."""

import pandas as pd

CRITICAL_COLUMNS = ("memory_id", "text", "timestamp")


def missing_rates(frame: pd.DataFrame) -> pd.Series:
    """Return the missing fraction for every column."""
    # TODO: calculate one rate per column.
    raise NotImplementedError


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing critical fields and impute the remaining fields."""
    # TODO: work on a copy; do not mutate frame.
    # TODO: drop rows missing a critical field.
    # TODO: add type_was_missing and importance_was_missing before imputation.
    # TODO: fill type with "unknown" and importance with the survivors' median.
    raise NotImplementedError
