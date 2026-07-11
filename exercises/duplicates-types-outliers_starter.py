"""Starter: complete every TODO, then run the dedicated tests."""

import pandas as pd


def normalize_station(station: pd.Series) -> pd.Series:
    """Normalize station labels for a conservative near-duplicate comparison."""
    # TODO: remove surrounding whitespace and ignore letter case.
    raise NotImplementedError


def duplicate_candidates(frame: pd.DataFrame) -> pd.Series:
    """Mark repeated ids, exact readings and normalized near-duplicates."""
    # TODO: combine three boolean masks and keep the first occurrence.
    raise NotImplementedError


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove candidates, coerce temperature and flag invalid/domain outliers."""
    # TODO: do not mutate frame; preserve audit flags before correction.
    # TODO: invalid numeric text gets the median of valid in-domain values.
    # TODO: clip temperature to the station contract [-50, 60] degrees Celsius.
    raise NotImplementedError
