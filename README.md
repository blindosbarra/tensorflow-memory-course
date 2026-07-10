# TensorFlow Memory AI Course Factory

Repository per costruire un corso tecnico eseguibile su TensorFlow, data
engineering e Memory AI Lab.

## Avvio locale

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
uv run python scripts/execute_notebooks.py
uv run mkdocs build --strict
```

Se l'ambiente blocca la cache globale di `uv`, usa una cache locale:

```bash
UV_CACHE_DIR=.uv-cache uv sync --extra dev
```

Su PowerShell:

```powershell
$env:UV_CACHE_DIR='.uv-cache'; uv sync --extra dev
```

## Documento principale

Leggi [`COURSE_FACTORY_SPEC.md`](COURSE_FACTORY_SPEC.md).

## Vertical slice disponibile

- Lezione: `data-cleaning-01-missing-values`
- Pagina: `docs/modules/data-cleaning-01-missing-values.md`
- Notebook: `notebooks/data-cleaning-01-missing-values.ipynb`
- Esempio: `examples/data_cleaning_missing_values.py`
- Test: `tests/test_data_cleaning.py`
- Review: `reports/reviews/bootstrap-review.md`

Non generare altri moduli prima della learner review umana della vertical slice.
