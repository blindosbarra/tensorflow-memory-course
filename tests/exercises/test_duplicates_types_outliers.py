from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd

PATH = Path("exercises/duplicates-types-outliers_starter.py")
SPEC = spec_from_file_location("quality_starter", PATH)
assert SPEC and SPEC.loader
STARTER = module_from_spec(SPEC)
SPEC.loader.exec_module(STARTER)


def test_quality_cleaning_contract() -> None:
    frame = pd.read_csv("datasets/synthetic/memory_events_quality_challenge.csv")
    original = frame.copy(deep=True)
    mask = STARTER.duplicate_candidates(frame)
    cleaned = STARTER.clean_challenge(frame)
    pd.testing.assert_frame_equal(frame, original)
    assert mask.dtype == bool and mask.sum() >= 4
    assert len(cleaned) == len(frame) - int(mask.sum())
    assert cleaned["memory_id"].is_unique
    assert cleaned["importance"].between(0, 1).all()
    assert {"importance_was_invalid_type", "importance_was_outlier"} <= set(cleaned.columns)
    assert cleaned["importance_was_invalid_type"].sum() > 0
    assert cleaned["importance_was_outlier"].sum() > 0
