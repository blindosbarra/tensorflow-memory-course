# AGENTS.md

## Scope

Queste istruzioni si applicano all’intero repository.

## Mission

Costruire un corso tecnico eseguibile e verificabile, non una raccolta di testo generato.

## Required reading

Prima di qualsiasi modifica leggere:

1. `COURSE_FACTORY_SPEC.md`
2. `course/course.yaml`
3. `course/progress.yaml`
4. i template e gli schemi pertinenti.

## Working rules

- Lavorare su una milestone o un modulo chiaramente delimitato.
- Scrivere un piano in `reports/` prima di patch estese.
- Preferire fonti primarie.
- Registrare le evidenze prima di scrivere una lezione.
- Non inventare informazioni per colmare lacune.
- Eseguire codice e notebook.
- Aggiungere test per ogni comportamento importante.
- Mantenere gli esempi piccoli e leggibili.
- Non inserire segreti o credenziali.
- Non utilizzare path assoluti.
- Aggiornare `course/progress.yaml`.
- Non marcare `done` se un quality gate fallisce.
- Evitare modifiche non correlate.
- Conservare soluzioni separate dagli esercizi.
- Documentare decisioni non ovvie.

## Verification commands

Quando disponibili, eseguire:

```bash
uv sync
uv run ruff check .
uv run mypy src
uv run pytest
uv run python scripts/execute_notebooks.py
uv run mkdocs build --strict
```

## Content style

- Italiano chiaro.
- Terminologia tecnica inglese mantenuta quando standard.
- Frasi brevi.
- Spiegazione intuitiva prima della matematica.
- Nessun prerequisito implicito.
- Ogni lezione collega teoria, codice e progetto Memory AI.
- Citazioni in fondo alla sezione pertinente.
- Nessuna lunga citazione verbatim.

## Pull requests

Ogni PR deve indicare:

- modulo;
- stato iniziale e finale;
- fonti aggiunte;
- test eseguiti;
- notebook eseguiti;
- limiti noti;
- screenshot o artifact quando utili.
