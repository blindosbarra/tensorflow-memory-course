from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd

PATH = Path("exercises/duplicates-types-outliers_starter.py")
SPEC = spec_from_file_location("quality_starter", PATH)
assert SPEC and SPEC.loader
STARTER = module_from_spec(SPEC)
SPEC.loader.exec_module(STARTER)


def test_quality_cleaning_contract() -> None:
    frame = pd.read_csv("datasets/synthetic/environmental_sensor_quality_challenge.csv")
    original = frame.copy(deep=True)
    mask = STARTER.duplicate_candidates(frame)
    cleaned = STARTER.clean_challenge(frame)
    pd.testing.assert_frame_equal(frame, original)
    assert mask.dtype == bool and mask.sum() >= 4
    assert len(cleaned) == len(frame) - int(mask.sum())
    assert cleaned["reading_id"].is_unique
    assert cleaned["temperature_c"].between(-50, 60).all()
    flags = {"temperature_was_invalid_type", "temperature_was_domain_outlier"}
    assert flags <= set(cleaned.columns)
    assert cleaned["temperature_was_invalid_type"].sum() > 0
    assert cleaned["temperature_was_domain_outlier"].sum() > 0
