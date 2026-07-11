# Examples: duplicates-types-outliers

## Mini tabella

| memory_id | text | timestamp | type | importance |
|---|---|---|---|---|
| mem_001 | Marco visited Glasgow with his son. | 2026-07-03 | episodic | 0.72 |
| mem_001 | Marco visited Glasgow with his son. | 2026-07-03 | episodic | 0.72 |
| mem_002 | The user prefers concise summaries. | 2026-07-04 | preference | 0.40 |
| mem_003 | The user likes walking meetings. | 2026-07-05 | preference | high |
| mem_004 | A trip lasted 400 days. | 2026-07-06 | episodic | 1.70 |

## Output atteso

- la seconda riga `mem_001` viene rimossa;
- `0.40` diventa numero;
- `high` viene segnalato come tipo non valido;
- `1.70` viene segnalato come outlier e portato a `1.0`.

## Comando

```bash
uv run python examples/duplicates_types_outliers.py
```

Output:

- `datasets/processed/memory_events_quality_clean.csv`
- `reports/evaluation/duplicates-types-outliers.json`
