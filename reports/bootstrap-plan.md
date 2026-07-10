# Bootstrap plan

Data: 2026-07-10

## Scope

Bootstrap tecnico del repository e una sola vertical slice completa per la lezione
`data-cleaning-01-missing-values`.

Non verranno generati altri moduli del corso.

## Gap analysis iniziale

- Il repository di lavoro contiene solo `.git`; non esistono ancora `AGENTS.md`,
  `COURSE_FACTORY_SPEC.md`, `course/`, `prompts/`, `templates/`, `schemas/`,
  `docs/`, `src/`, `tests/`, `notebooks/` o configurazioni CI.
- Lo starter zip allegato contiene la struttura base richiesta dalla specifica:
  istruzioni agenti, specifica factory, `course/course.yaml`,
  `course/progress.yaml`, template, prompt, schema evidenze, script notebook,
  scheletro MkDocs e directory di lavoro.
- Mancano dipendenze riproducibili installabili localmente, lockfile e workflow CI.
- Mancano package Python importabile, esempi eseguibili, test, notebook validati,
  research pack, pagina lezione, esercizio e soluzione per la vertical slice.
- Mancano registrazione evidenze, decisioni tecniche e report review.

## Fonti primarie selezionate per la slice

- pandas documentation: working with missing data.
- scikit-learn documentation: imputation of missing values and `SimpleImputer`.
- TensorFlow tutorial: structured data preprocessing layers.

Queste fonti coprono solo i claim della lezione pilota. Qualsiasi claim non coperto
deve restare fuori dalla lezione o finire in `course/research_gaps.md`.

## Sequenza di patch proposta

1. Importare lo starter zip nella root del repository senza path assoluti.
2. Aggiornare il bootstrap tecnico: `pyproject.toml`, CI GitHub Actions, package
   Python minimo, script notebook robusto e configurazione MkDocs.
3. Costruire il research pack per `data-cleaning-01-missing-values` in
   `knowledge/data-cleaning-01-missing-values/`, includendo `evidence.yaml`.
4. Implementare la vertical slice: dataset sintetico, funzioni Python, esempio,
   test, notebook, esercizio e soluzione.
5. Scrivere la pagina MkDocs della lezione e aggiornare navigazione, glossario,
   riferimenti e progress tracker.
6. Eseguire quality gate locali: lint, type check, test, notebook execution e
   `mkdocs build --strict`.
7. Scrivere `reports/reviews/bootstrap-review.md` con esito, comandi, limiti e
   rischi residui.
8. Creare piccoli commit logici dopo blocchi coerenti.

## Decisioni iniziali

- La prima slice usera' pandas e scikit-learn per il trattamento dei missing
  values; TensorFlow resta collegato al contesto strutturato del corso, senza
  forzare un training model nella prima lezione.
- Il dataset sara' sintetico e piccolo, versionato in `datasets/synthetic/`, per
  evitare download e credenziali.
- L'esempio produrra' un CSV pulito e un report JSON locale, entrambi generabili
  con comando Python.
- Il notebook verra' eseguito con `nbclient` tramite `scripts/execute_notebooks.py`.
- Lo stato della lezione potra' diventare `done` solo se tutti i gate locali
  passano.

## Lacune note

- Il lockfile dipende dalla disponibilita' di `uv` e dalla rete del runner locale.
- La CI non puo' essere eseguita su GitHub da questa macchina; viene validata
  localmente eseguendo gli stessi comandi.
- La comprensibilita' reale per principianti richiede revisione umana dopo la
  vertical slice, come indicato dalla specifica.
