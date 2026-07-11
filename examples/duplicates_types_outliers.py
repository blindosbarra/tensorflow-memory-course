"""Run the duplicates, types, and outliers example from the repository root."""

from __future__ import annotations

import json
from pathlib import Path

from memory_ai.data_quality import clean_memory_quality_csv


def main() -> None:
    input_path = Path("datasets/synthetic/memory_events_quality_issues.csv")
    output_path = Path("datasets/processed/memory_events_quality_clean.csv")
    report_path = Path("reports/evaluation/duplicates-types-outliers.json")

    result = clean_memory_quality_csv(input_path, output_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result.report, indent=2), encoding="utf-8")

    print(f"Wrote {output_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
