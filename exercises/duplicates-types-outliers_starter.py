"""Starter: complete every TODO, then run the dedicated tests."""

import pandas as pd


def normalize_text(text: pd.Series) -> pd.Series:
    """Normalize text for a conservative near-duplicate comparison."""
    # TODO: remove surrounding whitespace and ignore letter case.
    raise NotImplementedError


def duplicate_candidates(frame: pd.DataFrame) -> pd.Series:
    """Mark repeated ids, exact events and normalized near-duplicates."""
    # TODO: combine three boolean masks and keep the first occurrence.
    raise NotImplementedError


def clean_challenge(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove candidates, coerce importance, flag invalid/out-of-domain values."""
    # TODO: do not mutate frame; preserve audit flags before correction.
    # TODO: invalid numeric text gets the median of valid in-domain values.
    # TODO: clip importance to the declared [0, 1] domain.
    raise NotImplementedError
