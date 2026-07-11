from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd

PATH = Path("exercises/data-cleaning-01-missing-values_starter.py")
SPEC = spec_from_file_location("missing_starter", PATH)
assert SPEC and SPEC.loader
STARTER = module_from_spec(SPEC)
SPEC.loader.exec_module(STARTER)


def test_missing_rates_and_cleaning_contract() -> None:
    frame = pd.read_csv("datasets/synthetic/environmental_sensor_missing_challenge.csv")
    original = frame.copy(deep=True)
    rates = STARTER.missing_rates(frame)
    cleaned = STARTER.clean_challenge(frame)
    pd.testing.assert_frame_equal(frame, original)
    assert rates.index.equals(frame.columns)
    assert rates.between(0, 1).all()
    assert cleaned[list(STARTER.CRITICAL_COLUMNS)].notna().all().all()
    assert cleaned[["temperature_c", "humidity_pct"]].notna().all().all()
    assert {"temperature_was_missing", "humidity_was_missing"} <= set(cleaned.columns)
    assert cleaned["temperature_was_missing"].sum() > 0
    assert cleaned["humidity_was_missing"].sum() > 0
