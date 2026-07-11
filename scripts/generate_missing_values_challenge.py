"""Generate the reproducible learner dataset for the missing-values exercise."""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260711
OUTPUT = Path("datasets/synthetic/memory_events_missing_challenge.csv")


def main() -> None:
    rng = np.random.default_rng(SEED)
    size = 120
    frame = pd.DataFrame(
        {
            "memory_id": [f"challenge_{index:03d}" for index in range(size)],
            "text": [f"Synthetic memory number {index}." for index in range(size)],
            "timestamp": pd.date_range("2026-01-01", periods=size).astype(str),
            "type": rng.choice(["episodic", "semantic", "preference"], size=size),
            "importance": np.round(rng.beta(2.5, 4.0, size=size), 3),
        }
    )
    for column, count in (("text", 5), ("timestamp", 4), ("type", 13), ("importance", 17)):
        indices = rng.choice(size, size=count, replace=False)
        frame.loc[indices, column] = np.nan
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
