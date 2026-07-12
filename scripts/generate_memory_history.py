"""Generate the simulated 3-month memory history for project step 3."""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260712
OUTPUT = Path("datasets/synthetic/memory_events_history.csv")

NAMES = ["Marco", "Lucia", "Elena", "Paolo", "Sara", "Giorgio"]
CITIES = ["Milano", "Glasgow", "Torino", "Roma", "Bologna", "Napoli"]
TOPICS = ["il progetto TensorFlow", "la palestra", "il colloquio", "la newsletter",
          "il corso di cucina", "la riunione settimanale"]

EPISODIC = [
    "{name} visited {city} for the weekend.",
    "{name} booked a train to {city}.",
    "{name} had a long call about {topic}.",
    "{name} met a friend in {city}.",
    "{name} finished a milestone of {topic}.",
]
PREFERENCE = [
    "The user prefers short updates about {topic}.",
    "The user likes walking meetings.",
    "The user prefers morning sessions for {topic}.",
    "The user dislikes late notifications.",
]
SEMANTIC = [
    "{name} works on {topic}.",
    "{name} lives near {city}.",
    "The office in {city} closes at 18:00.",
    "{topic} happens every Tuesday.",
]


def main() -> None:
    rng = np.random.default_rng(SEED)
    size = 300
    start = pd.Timestamp("2026-04-01")
    offsets = np.sort(rng.integers(0, 100 * 24, size=size))
    timestamps = [start + pd.Timedelta(hours=int(h)) for h in offsets]

    rows = []
    for index in range(size):
        kind = rng.choice(["episodic", "preference", "semantic"], p=[0.5, 0.3, 0.2])
        template_pool = {"episodic": EPISODIC, "preference": PREFERENCE, "semantic": SEMANTIC}[kind]
        template = template_pool[int(rng.integers(0, len(template_pool)))]
        text = template.format(
            name=rng.choice(NAMES), city=rng.choice(CITIES), topic=rng.choice(TOPICS)
        )
        importance = float(np.clip(rng.normal(0.55, 0.2), 0.02, 0.98))
        rows.append(
            {
                "memory_id": f"hist_{index:04d}",
                "text": text,
                "timestamp": timestamps[index].strftime("%Y-%m-%d %H:%M"),
                "type": kind,
                "importance": round(importance, 2),
            }
        )

    frame = pd.DataFrame(rows)
    # difetti realistici e deterministici: qualche retry duplicato e buchi sparsi
    duplicate_rows = frame.iloc[[25, 90, 180]].copy()
    frame = pd.concat([frame, duplicate_rows], ignore_index=True)
    frame.loc[[40, 133, 210], "importance"] = np.nan
    frame.loc[[77, 250], "type"] = np.nan

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
