"""Generate the reproducible learner dataset for the missing-values exercise."""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260711
OUTPUT = Path("datasets/synthetic/environmental_sensor_missing_challenge.csv")


def main() -> None:
    rng = np.random.default_rng(SEED)
    size = 120
    frame = pd.DataFrame(
        {
            "reading_id": [f"reading_{index:03d}" for index in range(size)],
            "station_id": rng.choice(["north", "central", "south"], size=size),
            "recorded_at": pd.date_range("2026-01-01", periods=size, freq="h").astype(str),
            "temperature_c": np.round(rng.normal(18.0, 5.5, size=size), 1),
            "humidity_pct": np.round(rng.normal(61.0, 12.0, size=size), 1),
        }
    )
    for column, count in (
        ("station_id", 5),
        ("recorded_at", 4),
        ("temperature_c", 13),
        ("humidity_pct", 17),
    ):
        indices = rng.choice(size, size=count, replace=False)
        frame.loc[indices, column] = np.nan
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
