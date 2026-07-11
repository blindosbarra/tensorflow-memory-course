# Lesson plan: duplicates-types-outliers

## Scope

- Modulo: data-engineering
- Lezione: duplicates-types-outliers
- Stato iniziale: planned
- Stato target: learner_review

## Gap analysis

- File presenti:
  - `course/course.yaml` contiene la lezione.
  - `course/progress.yaml` contiene solo la vertical slice precedente.
  - `docs/syllabus.md` cita gia' "Duplicati, tipi e outlier".
  - `docs/modules/data-cleaning-01-missing-values.md` definisce lo stile locale.
- File mancanti:
  - research pack in `knowledge/duplicates-types-outliers/`.
  - lezione in `docs/modules/duplicates-types-outliers.md`.
  - dataset sintetico dedicato.
  - funzioni Python, esempio, notebook, esercizio, soluzione e test.
  - voce MkDocs e indice moduli.
  - report review finale.
- Fonti necessarie:
  - pandas per duplicati, conversione tipi e outlier via quantili.
  - pandas `to_numeric` per coercizione controllata dei tipi.
  - scikit-learn o documentazione statistica primaria per l'idea di robustezza
    rispetto agli outlier. Se il claim non e' coperto da fonte primaria, va
    marcato come gap o mantenuto come regola operativa locale.
- API da verificare:
  - `DataFrame.duplicated`.
  - `DataFrame.drop_duplicates`.
  - `pandas.to_numeric`.
  - `Series.quantile`.
- Dataset necessari:
  - CSV sintetico piccolo con record memoria duplicati, `importance` come testo,
    valori non convertibili e un valore fuori range.
- Decisioni aperte:
  - trattare `importance` fuori da `[0, 1]` come outlier di dominio, non come
    outlier statistico generico.
  - lasciare la deduplicazione conservativa: stesso `memory_id` o stessa coppia
    `text`/`timestamp`.

## Obiettivo pratico

Pulire un piccolo dataset di memorie rimuovendo duplicati, convertendo tipi
numericamente controllati e segnalando outlier senza nascondere le decisioni.

## Prerequisiti

- Lezione `data-cleaning-01-missing-values`.
- Python base.
- pandas DataFrame e CSV.

## Artifact da produrre

- Research pack: `knowledge/duplicates-types-outliers/`
- Lezione: `docs/modules/duplicates-types-outliers.md`
- Notebook: `notebooks/duplicates-types-outliers.ipynb`
- Esempio: `examples/duplicates_types_outliers.py`
- Dataset: `datasets/synthetic/memory_events_quality_issues.csv`
- Output esempio: `datasets/processed/memory_events_quality_clean.csv`
- Test: `tests/test_data_quality.py`
- Esercizio: `exercises/duplicates-types-outliers.md`
- Soluzione: `solutions/duplicates-types-outliers.md`
- Report: `reports/reviews/duplicates-types-outliers.md`

## Patch sequence

1. Research pack con evidenze e fonti primarie.
2. Funzioni piccole in `src/memory_ai/data_quality.py`.
3. Dataset sintetico, esempio eseguibile e report JSON.
4. Test unitari per duplicati, tipi e outlier.
5. Notebook con gli stessi passaggi dell'esempio.
6. Lezione, esercizio e soluzione.
7. Navigazione MkDocs, indice moduli, riferimenti e progress tracker.
8. Quality gates e review finale.

## Quality gates

- [x] Research
- [x] Lesson
- [x] Code
- [x] Didactics
- [x] Publish
- [x] Security/cost non applicabile: nessun cloud, nessuna credenziale.

## Rischi

- Confondere outlier statistici con valori impossibili per dominio. La lezione
  deve dichiarare che qui si usa una regola locale su `importance`.
- Rendere l'esempio troppo ampio. Limitare a tre problemi: duplicati, tipi,
  outlier.
- Marcare la lezione `done` senza review umana. Lo stato target resta
  `learner_review`.
