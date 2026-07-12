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

## Lezioni disponibili (in learner review)

Due lezioni della fase dati, riscritte dopo la learner review del 2026-07-11
(report: `reports/reviews/course-content-review.md`; rework:
`reports/reviews/content-rework.md`):

- `data-cleaning-01-missing-values` e `duplicates-types-outliers`
- Pagine: `docs/modules/<lesson-id>.md`
- Esercizi da completare: `exercises/<lesson-id>_starter.py`
- Test dell'esercizio (rossi finche' non scrivi il codice):
  `uv run pytest -o norecursedirs= tests/exercises/`
- Soluzioni e risposte al quiz: `solutions/<lesson-id>.md`

I moduli `examples/` e `src/memory_ai/` sono l'implementazione di riferimento
della pipeline memoria, usata dalle lezioni solo nel trasferimento finale.

Non generare nuove lezioni prima della learner review umana
(`templates/learner-review.md`) delle due lezioni riscritte.
