# Review: bootstrap and data-cleaning-01-missing-values

## Decisione

PASS per bootstrap tecnico, CI locale, build MkDocs e vertical slice tecnica.

La lezione resta in `learner_review` perche' la specifica richiede validazione
umana prima di scalare il corso.

## Blocker

- Nessuno per i gate locali.

## Major

- Nessuno.

## Minor

- `uv` non era installato globalmente nella macchina. E' stato installato nella
  venv di gate per generare `uv.lock` e validare `uv sync --extra dev`.
- `mkdocs build --strict` mostra un warning informativo di Material for MkDocs
  su MkDocs 2.0; non blocca la build.
- L'esecuzione notebook su Windows mostra warning runtime di ZMQ/IPKernel; il
  notebook passa e non usa credenziali o rete.

## Verifiche eseguite

- [x] Fonti
- [x] Teoria
- [x] API
- [x] Codice
- [x] Notebook
- [x] Test
- [x] Didattica
- [x] Link
- [x] Build sito

## Comandi

```powershell
$env:UV_CACHE_DIR='.uv-cache'; .\.venv-gates\Scripts\uv.exe sync --extra dev
$env:UV_CACHE_DIR='.uv-cache'; .\.venv-gates\Scripts\uv.exe run ruff check .
$env:UV_CACHE_DIR='.uv-cache'; .\.venv-gates\Scripts\uv.exe run mypy src
$env:UV_CACHE_DIR='.uv-cache'; .\.venv-gates\Scripts\uv.exe run pytest
$env:UV_CACHE_DIR='.uv-cache'; .\.venv-gates\Scripts\uv.exe run python scripts\execute_notebooks.py
$env:UV_CACHE_DIR='.uv-cache'; .\.venv-gates\Scripts\uv.exe run mkdocs build --strict
```

Risultati sintetici:

- `ruff`: all checks passed.
- `mypy`: success, 2 source files checked.
- `pytest`: 3 passed.
- notebook: `notebooks/data-cleaning-01-missing-values.ipynb` executed.
- MkDocs: documentation built successfully.

## Artifact prodotti

- `uv.lock`
- `.github/workflows/ci.yml`
- `src/memory_ai/data_cleaning.py`
- `datasets/synthetic/memory_events_raw.csv`
- `datasets/processed/memory_events_clean.csv`
- `examples/data_cleaning_missing_values.py`
- `tests/test_data_cleaning.py`
- `notebooks/data-cleaning-01-missing-values.ipynb`
- `knowledge/data-cleaning-01-missing-values/evidence.yaml`
- `docs/modules/data-cleaning-01-missing-values.md`
- `exercises/data-cleaning-01-missing-values.md`
- `solutions/data-cleaning-01-missing-values.md`
- `reports/evaluation/data-cleaning-01-missing-values.json`

## Fonti primarie

- pandas documentation, "Working with missing data":
  https://pandas.pydata.org/docs/user_guide/missing_data.html
- scikit-learn documentation, "Imputation of missing values":
  https://scikit-learn.org/stable/modules/impute.html
- TensorFlow Core tutorial, "Classify structured data using Keras preprocessing
  layers": https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers

## Decisioni

- TensorFlow, Keras e KerasHub sono stati spostati nell'extra `ml`: la prima
  slice non addestra modelli e deve restare leggera.
- Python 3.12 e' usato in CI e mypy per allinearsi all'ambiente locale e alle
  stubs NumPy installate.
- La pulizia dati scarta campi critici mancanti e imputa solo feature non
  critiche con flag di audit.

## Rischi residui

- La learner review umana e' ancora necessaria.
- I meccanismi statistici MCAR/MAR/MNAR sono esclusi dalla slice e rimandati a
  una lezione successiva.
- La CI GitHub non e' stata eseguita su runner remoto da questa macchina; e'
  stata validata localmente con gli stessi comandi.
