"""Generate the reproducible learner dataset for the quality exercise."""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260711
OUTPUT = Path("datasets/synthetic/memory_events_quality_challenge.csv")


def main() -> None:
    rng = np.random.default_rng(SEED)
    size = 120
    topics = rng.choice(["travel", "food", "work", "family"], size=size)
    frame = pd.DataFrame(
        {
            "memory_id": [f"quality_{index:03d}" for index in range(size)],
            "text": [f"The user mentioned {topic} item {index}." for index, topic in enumerate(topics)],
            "timestamp": pd.date_range("2026-02-01", periods=size).astype(str),
            "type": rng.choice(["episodic", "semantic", "preference"], size=size),
            "importance": np.round(rng.normal(0.55, 0.18, size=size), 3).astype(object),
        }
    )
    frame.loc[[7, 49], "memory_id"] = frame.loc[[6, 48], "memory_id"].to_numpy()
    frame.loc[80, ["text", "timestamp"]] = frame.loc[79, ["text", "timestamp"]].to_numpy()
    frame.loc[95, "text"] = "  " + str(frame.loc[94, "text"]).upper() + "  "
    frame.loc[[14, 67], "importance"] = ["urgent", "unknown"]
    frame.loc[[20, 88], "importance"] = [-0.4, 1.6]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
