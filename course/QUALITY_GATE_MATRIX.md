# Quality gate matrix

Scopo: rendere verificabile ogni fase senza interpretazioni implicite.

## Comandi standard

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
uv run python scripts/execute_notebooks.py
uv run mkdocs build --strict
```

Se la cache globale non e' scrivibile:

```bash
UV_CACHE_DIR=.uv-cache uv sync --extra dev
```

## Gate A: Research

Passa se:

- esiste `knowledge/<lesson-id>/evidence.yaml`;
- ogni claim importante della lezione ha un id evidenza;
- ogni fonte e' primaria oppure marcata come secondaria con motivazione;
- versione, data o data di accesso sono registrate;
- conflitti e deprecazioni sono espliciti;
- `course/research_gaps.md` contiene le domande non risolte.

Fallisce se:

- una fonte non e' raggiungibile e non esiste alternativa;
- il testo didattico contiene claim non presenti in `evidence.yaml`;
- viene citata una API non verificata.

## Gate B: Lesson

Passa se:

- la pagina e' in `docs/modules/<lesson-id>.md`;
- front matter contiene id, title, module, status, estimated_minutes,
  prerequisites, deliverables e sources;
- massimo 3 concetti principali;
- esiste collegamento esplicito al Memory AI Lab;
- quiz ed esercizio verificano gli obiettivi;
- il riepilogo ha massimo 8 punti;
- fonti presenti nella sezione finale.

Fallisce se:

- la lezione richiede prerequisiti non insegnati o non dichiarati;
- il testo supera lo scope microlearning;
- il quiz e' solo mnemonico.

## Gate C: Code

Passa se:

- `ruff check .` passa;
- `mypy src` passa;
- `pytest` passa;
- ogni esempio Python e' coperto da test;
- ogni notebook viene eseguito da `scripts/execute_notebooks.py`;
- output generati sono piccoli, riproducibili e versionabili quando utili;
- nessun path assoluto o segreto e' presente.

Fallisce se:

- un notebook e' solo illustrativo e non eseguibile;
- un esempio non ha test;
- un risultato numerico non ha seed o tolleranza quando serve.

## Gate D: Didactics

Passa se:

- una persona target puo' completare la lezione in 15-30 minuti;
- la lezione produce un risultato osservabile;
- l'esercizio ha hint progressivi;
- la soluzione resta separata;
- errori comuni e limiti sono dichiarati;
- la learner review non segnala blocker.
- esiste una learner review umana completa basata su
  `templates/learner-review.md` prima di avanzare a `done`.

Fallisce se:

- il contenuto salta passaggi operativi;
- l'esercizio richiede conoscenze non spiegate;
- il collegamento al progetto finale e' decorativo.

## Gate E: Publish

Passa se:

- `mkdocs build --strict` passa;
- navigazione aggiornata in `mkdocs.yml`;
- `docs/modules/index.md` punta alla lezione;
- glossario e riferimenti sono aggiornati;
- link esterni principali sono stati verificati durante research;
- `course/progress.yaml` e' coerente con gli artifact.

Fallisce se:

- una pagina non e' raggiungibile dal sito;
- una fonte citata non appare in `docs/references.md`;
- progress tracker dichiara stato piu' avanzato dei gate reali.

## Gate F: Security and cost

Obbligatorio per lezioni cloud, LLM e deploy.

Passa se:

- nessuna credenziale o token e' salvato nel repo;
- le variabili ambiente richieste sono documentate;
- esiste percorso locale equivalente;
- costi qualitativi e cleanup sono documentati;
- output cloud non e' necessario per passare i gate base.

Fallisce se:

- la lezione richiede account cloud per completare il corso base;
- cleanup mancante;
- servizi a costo non trascurabile senza warning.

## Report richiesto

Ogni review deve usare `templates/review.md` e includere:

- decisione PASS/FAIL;
- blocker, major, minor;
- comandi eseguiti;
- output sintetici;
- rischi residui;
- decisione su `course/progress.yaml`.
