# Esercizio: missing values su dati non anticipati

Completa tutti i TODO in
`exercises/data-cleaning-01-missing-values_starter.py` usando
`datasets/synthetic/memory_events_missing_challenge.csv` (120 righe). La lezione
non rivela quali celle siano problematiche: la diagnosi fa parte dell'esercizio.

Criteri: non mutare l'input; calcolare tassi per colonna; scartare soltanto i
record senza campi critici; creare i flag prima di imputare; usare `unknown` e
la mediana dei record sopravvissuti.

Esegui soltanto i test learner con:

```bash
uv run pytest -o norecursedirs= tests/exercises/test_data_cleaning_01_missing_values.py
```

Lo starter incompleto deve fallire. `uv run pytest` lo esclude intenzionalmente.

Hint: (1) parti da `frame.isna().mean()`; (2) usa `dropna(subset=...)` su una
copia; (3) crea i flag prima di `fillna`; (4) calcola la mediana dopo i drop.
