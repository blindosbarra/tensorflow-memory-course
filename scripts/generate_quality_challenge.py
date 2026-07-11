"""Generate the reproducible learner dataset for the quality exercise."""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260711
OUTPUT = Path("datasets/synthetic/environmental_sensor_quality_challenge.csv")


def main() -> None:
    rng = np.random.default_rng(SEED)
    size = 120
    stations = rng.choice(["north", "central", "south"], size=size)
    frame = pd.DataFrame(
        {
            "reading_id": [f"reading_{index:03d}" for index in range(size)],
            "station_id": stations,
            "recorded_at": pd.date_range("2026-02-01", periods=size, freq="h").astype(str),
            "temperature_c": np.round(rng.normal(18.0, 5.0, size=size), 1).astype(object),
        }
    )
    frame.loc[[7, 49], "reading_id"] = frame.loc[[6, 48], "reading_id"].to_numpy()
    frame.loc[80, ["station_id", "recorded_at"]] = frame.loc[
        79, ["station_id", "recorded_at"]
    ].to_numpy()
    frame.loc[95, "station_id"] = "  " + str(frame.loc[94, "station_id"]).upper() + "  "
    frame.loc[95, "recorded_at"] = frame.loc[94, "recorded_at"]
    frame.loc[[14, 67], "temperature_c"] = ["sensor_error", "offline"]
    frame.loc[[20, 88], "temperature_c"] = [-62.0, 79.0]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
