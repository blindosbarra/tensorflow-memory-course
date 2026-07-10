---
id: data-cleaning-01-missing-values
title: Missing values nei dati di memoria
module: data-engineering
status: done
estimated_minutes: 25
prerequisites:
  - Python base
  - Tabelle CSV
deliverables:
  - datasets/processed/memory_events_clean.csv
  - reports/evaluation/data-cleaning-01-missing-values.json
sources:
  - https://pandas.pydata.org/docs/user_guide/missing_data.html
  - https://scikit-learn.org/stable/modules/impute.html
  - https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
---

# Missing values nei dati di memoria

## Cosa saprai fare

Al termine saprai:

- misurare quanti valori mancano in ogni colonna;
- decidere quali righe scartare perche' mancano campi critici;
- imputare feature non critiche e registrare cosa e' stato modificato.

## Perche' serve nel Memory AI Lab

Il progetto finale usera' record di memoria con testo, timestamp, tipo e
importanza. Una memoria senza testo o senza tempo non puo' essere recuperata in
modo affidabile. Un tipo mancante o un punteggio di importanza mancante, invece,
possono essere imputati se il report conserva l'informazione che il valore era
assente.

## Intuizione

Non pulire i dati "per far sparire i buchi". Puliscili per rendere esplicite le
decisioni. Prima misuri, poi decidi quali campi sono critici, poi applichi una
regola semplice e verificabile.

## Teoria essenziale

pandas rappresenta i valori mancanti con sentinelle diverse in base al tipo di
dato, per esempio `NaN`, `NaT` e `NA`. Per questo si usa `isna()` o `notna()`
invece di confronti di uguaglianza.

scikit-learn documenta due strategie di base per dataset incompleti: scartare
righe o colonne, oppure imputare i valori mancanti. `SimpleImputer` copre
strategie semplici come costante, media, mediana e valore piu' frequente.

In questa lezione applichiamo una regola conservativa:

- `memory_id`, `text` e `timestamp` sono campi critici: se mancano, la riga esce;
- `type` viene imputato con `unknown`;
- `importance` viene imputato con la mediana dei record rimasti;
- ogni imputazione lascia un flag booleano.

## Dentro TensorFlow/Keras

Il tutorial TensorFlow sui dati strutturati mostra che le feature tabellari
arrivano al modello come tensori. Questa lezione prepara una tabella coerente
prima di arrivare a quel punto: niente credenziali, niente cloud, niente training
prematuro.

## Esempio guidato

Esegui:

```bash
uv run python examples/data_cleaning_missing_values.py
```

Il comando legge `datasets/synthetic/memory_events_raw.csv`, produce
`datasets/processed/memory_events_clean.csv` e scrive il report JSON in
`reports/evaluation/data-cleaning-01-missing-values.json`.

Il comportamento importante e' testato in `tests/test_data_cleaning.py`.

## Prova tu

Apri `notebooks/data-cleaning-01-missing-values.ipynb` ed eseguilo dall'inizio
alla fine, oppure usa il gate automatico:

```bash
uv run python scripts/execute_notebooks.py
```

## Errori comuni

- usare `== NaN` per cercare missing value;
- imputare tutto senza distinguere campi critici e feature ausiliarie;
- non salvare un report delle righe scartate;
- calcolare statistiche di imputazione su dati che in futuro saranno test set.

## Riepilogo

- I missing value vanno misurati prima di essere corretti.
- `isna()` e `notna()` sono le API pandas da usare per rilevarli.
- Scartare righe puo' essere corretto quando manca un campo critico.
- Imputare e' utile per feature non critiche.
- `SimpleImputer` rende esplicita la strategia di imputazione.
- I flag di imputazione conservano informazione utile per audit e modelli.
- La pulizia deve produrre output riproducibili.

## Quiz

1. Perche' `isna()` e' piu' adatto di `== pd.NA`?
2. Quale rischio introduci se imputi `importance` usando anche il test set?
3. Perche' una memoria senza `timestamp` viene scartata in questa lezione?

## Esercizio

Vedi `exercises/data-cleaning-01-missing-values.md`.

## Fonti

- pandas, "Working with missing data":
  https://pandas.pydata.org/docs/user_guide/missing_data.html
- scikit-learn, "Imputation of missing values":
  https://scikit-learn.org/stable/modules/impute.html
- TensorFlow Core, "Classify structured data using Keras preprocessing layers":
  https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
