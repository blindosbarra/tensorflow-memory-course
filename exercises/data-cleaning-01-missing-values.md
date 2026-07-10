# Esercizio: missing values

Parti da `datasets/synthetic/memory_events_raw.csv`.

Obiettivo: usa `memory_ai.data_cleaning.clean_memory_records` per ottenere una
tabella senza missing value e un report con le decisioni applicate.

## Criteri di successo

- Le righe senza `text` o `timestamp` non sono presenti nel risultato.
- `type` mancante diventa `unknown`.
- `importance` mancante viene imputata con la mediana.
- Il report contiene `rows_before`, `rows_after`, `dropped_rows` e `imputed`.
- I test passano con `uv run pytest`.

## Hint

1. Carica il CSV con pandas.
2. Prima guarda `missing_summary`.
3. Poi chiama `clean_memory_records`.
4. Controlla i flag `type_was_missing` e `importance_was_missing`.
