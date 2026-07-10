# Examples: missing values

Esempio eseguibile:

```bash
uv run python examples/data_cleaning_missing_values.py
```

Input:

- `datasets/synthetic/memory_events_raw.csv`

Output generati:

- `datasets/processed/memory_events_clean.csv`
- `reports/evaluation/data-cleaning-01-missing-values.json`

Comportamento atteso:

- righe senza `text` o `timestamp` escluse;
- `type` mancante imputato con `unknown`;
- `importance` mancante imputata con la mediana;
- flag booleani creati per indicare quali valori sono stati imputati.
