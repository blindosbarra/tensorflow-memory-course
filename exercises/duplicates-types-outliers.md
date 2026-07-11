# Esercizio: audit di una rete di sensori

Completa tutti i TODO in `exercises/duplicates-types-outliers_starter.py` usando
`datasets/synthetic/environmental_sensor_quality_challenge.csv` (120 righe).
Devi scoprire i problemi dal dataset; non sono elencati qui.

Criteri: non mutare l'input; confrontare anche etichette di stazione
normalizzate; conservare la prima occorrenza; creare flag di audit; imputare
testo numerico invalido con la mediana dei valori validi nel dominio; applicare
il contratto di stazione `[-50, 60]` gradi Celsius.

```bash
uv run pytest -o norecursedirs= tests/exercises/test_duplicates_types_outliers.py
```

Lo starter incompleto deve fallire. Hint: (1) `str.strip().str.casefold()`;
(2) combina maschere `duplicated`; (3) `to_numeric(errors="coerce")`;
(4) calcola la mediana solo sui valori nel dominio; (5) crea il flag prima di
`clip`.
