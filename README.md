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

## Come si studia

Ogni lezione e' **un notebook autosufficiente** in `notebooks/`: teoria,
esempi eseguibili, esercizio guidato con soluzione spiegata, quiz con
risposte, e un passo del **progetto del corso** (Memory AI Lab), che cresce
di lezione in lezione fino a diventare il sistema completo. Non servono
terminale, pytest o altri strumenti: si apre il notebook e si esegue.

Per aprire un notebook in locale:

```bash
uv sync --extra dev
uv run jupyter lab notebooks/
```

(oppure aprilo con VS Code o caricalo su Google Colab).

## Lezioni disponibili (in learner review)

1. `notebooks/data-cleaning-01-missing-values.ipynb` — dati mancanti:
   teoria (meccanismi, strategie, effetti) + progetto passo 1 (ingestion).
2. `notebooks/duplicates-types-outliers.ipynb` — duplicati, tipi errati e
   outlier + progetto passo 2 (controllo qualita' del nuovo batch).

Le pagine in `docs/modules/` sono i riassunti di riferimento pubblicati sul
sito. I moduli `examples/` e `src/memory_ai/` sono implementazione di
riferimento della pipeline, non materiale di studio.

Non generare nuove lezioni prima della learner review umana
(`templates/learner-review.md`) delle due lezioni esistenti.
