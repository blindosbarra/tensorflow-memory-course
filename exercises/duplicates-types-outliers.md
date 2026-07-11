# Esercizio: audit di duplicati, tipi e outlier

Completa tutti i TODO in `exercises/duplicates-types-outliers_starter.py` usando
`datasets/synthetic/memory_events_quality_challenge.csv` (120 righe). Devi
scoprire i problemi dal dataset; non sono elencati qui.

Criteri: non mutare l'input; confrontare anche testo normalizzato; conservare la
prima occorrenza; creare flag di audit; imputare testo numerico invalido con la
mediana dei valori validi nel dominio; applicare il range di dominio `[0, 1]`.

```bash
uv run pytest -o norecursedirs= tests/exercises/test_duplicates_types_outliers.py
```

Lo starter incompleto deve fallire. Hint: (1) `str.strip().str.casefold()`;
(2) combina maschere `duplicated`; (3) `to_numeric(errors="coerce")`; (4)
calcola la mediana solo sui valori gia' nel dominio; (5) crea il flag prima di
`clip`.
