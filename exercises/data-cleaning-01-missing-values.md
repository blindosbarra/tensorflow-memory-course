# Esercizio: missing values in una rete di sensori

Completa tutti i TODO in
`exercises/data-cleaning-01-missing-values_starter.py` usando
`datasets/synthetic/environmental_sensor_missing_challenge.csv` (120 righe).
Devi diagnosticare il dataset: problemi, quantita' e posizioni non sono
anticipati.

Criteri: non mutare l'input; calcolare tassi per colonna; scartare soltanto le
righe senza campi critici; creare i flag prima di imputare; usare la mediana dei
record sopravvissuti per temperatura e umidita'.

```bash
uv run pytest -o norecursedirs= tests/exercises/test_data_cleaning_01_missing_values.py
```

Lo starter incompleto deve fallire; `uv run pytest` lo esclude intenzionalmente.
Hint: (1) `frame.isna().mean()`; (2) lavora su una copia; (3) crea i flag prima
di `fillna`; (4) calcola ogni mediana dopo i drop.
