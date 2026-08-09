# Template di lezione

Questo file descrive come e' fatta una lezione **oggi**. Non e' una pagina da
copiare intera: la lezione vive nel notebook, e la pagina in `docs/modules/`
ne e' il riassunto di riferimento.

> Nota storica: fino al commit `3fa5799` il corso aveva un modello diverso —
> file `exercises/<lesson-id>_starter.py` con TODO e test dedicati in
> `tests/exercises/`. Quel modello e' stato rimosso, e con esso le cartelle
> `exercises/` e `solutions/` (WI-8). Non ricostruirlo.

---

## I due tipi di lezione

La decisione **D2** (`course/research_gaps.md`) ha fissato due tipi, e il
corso li dichiara apertamente invece di promettere un esercizio ovunque:

| Tipo | Lezioni | Esercizio guidato |
|---|---|---|
| Con esercizio | 1-30 | si', dentro il notebook |
| Di sola lettura | 31-60 | no |

Una lezione di sola lettura e' legittima. Non e' legittima una lezione a un
terzo della profondita' teorica delle altre: la densita' e' un requisito
separato dall'esercizio (WI-6).

---

## Artefatti di una lezione

Due file, piu' il pack di evidenze:

1. `notebooks/lezione-<NN>-<slug>.ipynb` — **la lezione**. Autosufficiente:
   teoria, codice eseguito, esercizio (se 1-30), passo del Memory AI Lab.
2. `docs/modules/<lesson-id>.md` — il **riassunto di riferimento** pubblicato
   sul sito. Non duplica il notebook: lo riassume e ci rimanda.
3. `knowledge/<lesson-id>/evidence.yaml` — le evidenze. Si scrivono **prima**
   di scrivere la lezione, e ogni affermazione tecnica nuova va registrata
   qui nello stesso commit del testo che la introduce.

Non creare altri file di esercizio, soluzione o test per lezione.

---

## Struttura del notebook

```text
# Lezione <NN> — <titolo>

> **Modulo:** <modulo> · **Tempo stimato:** <NN> minuti
> **Prerequisiti:** <lezioni>
>
> Obiettivo pratico unico: <un solo risultato osservabile>

## Parte 1 — Il problema
## Parte 2 — Teoria essenziale
## Parte 3 — <teoria o esempio guidato, quante parti servono>
## Parte N — Esercizio guidato          <- solo lezioni 1-30
### Soluzione spiegata                  <- solo lezioni 1-30
## Parte N+1 — Il progetto: Memory AI Lab, passo <NN>
## Cosa hai imparato   (oppure "## Riepilogo (max 8 punti)")
## Quiz
## Fonti
```

Regole per le sezioni che sbagliano piu' spesso:

- **Il problema.** Parti da un dominio generico e realistico (sensori, log,
  form). Il Memory AI Lab non si introduce qui.
- **Teoria essenziale.** Il *perche'* prima del *come*: concetti, assunzioni,
  trade-off. Ogni affermazione tecnica rilevante ha una citazione primaria
  vicina, e la stessa fonte sta in `evidence.yaml`. Non descrivere qui le API.
- **Esercizio guidato** (1-30). Una cella dove lo studente scrive, con i passi
  richiesti come commenti, poi `### Soluzione spiegata` in una cella separata.
  Nessun file esterno, nessun test dedicato.
- **Memory AI Lab.** Un solo passo per lezione, chiuso da un `assert` che
  verifica un invariante strutturale. Spiega il meccanismo reale che produce
  il difetto (timeout di ingestion, estrazione parziale, retry), non darlo per
  scontato.
- **Quiz.** Domande basate solo su concetti gia' insegnati, e le risposte
  stanno **nel notebook**: un blocco `<details><summary>Apri le
  risposte</summary>` per le risposte lunghe, oppure una riga
  `*(Risposte: 1. ...; 2. ...)*` per quelle brevi. Non rimandare a file fuori
  da `docs/` o `notebooks/`: non sarebbero raggiungibili dal sito.
- **Fonti.** In fondo, una riga per fonte. Le lezioni 2 e 30-60 storicamente
  ne erano prive: aggiungerle man mano che si introducono citazioni.

Il notebook deve girare nell'ambiente base (`uv sync`) salvo quando la lezione
richiede davvero l'extra `ml`. Deve essere deterministico: seed fissi, e
`git status --porcelain` vuoto dopo un run completo di
`scripts/execute_notebooks.py`.

---

## Struttura della pagina in `docs/modules/`

```markdown
---
id: <lesson-id>
title: <titolo>
module: <module-id>
status: draft
estimated_minutes: 25
prerequisites: []
deliverables: [notebooks/lezione-<NN>-<slug>.ipynb]
sources: []
---

# <Titolo>

> **La lezione si segue nel notebook** `notebooks/lezione-<NN>-<slug>.ipynb`.
> Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare
## Il problema nel suo dominio naturale
## Teoria essenziale
## Dentro TensorFlow/Keras
## Esempio guidato
## Prova tu
## Errori comuni
## Riepilogo
## Quiz
## Esercizio
## Trasferimento al Memory AI Lab
## Fonti
```

- **Dentro TensorFlow/Keras** non si omette: se la lezione non usa
  TensorFlow/Keras, dichiara cosa prepara e in quale lezione arriva.
- **Esercizio** rimanda al notebook (`Parte <N>`) e non anticipa quantita' e
  posizioni dei problemi. Nelle lezioni di sola lettura, dillo.
- **Riepilogo**: massimo 8 punti, senza risposte copiabili al quiz.
- **Fonti**: `docs/references.md` e' generata da queste sezioni con
  `scripts/build_references.py`. Una fonte citata solo nel notebook non
  raggiunge la pagina aggregata.

---

## Prima di dire che la lezione e' finita

```bash
uv run ruff check .
uv run mypy src
uv run pytest
uv run python scripts/execute_notebooks.py     # 61/61, albero pulito dopo
uv run python scripts/build_references.py --check
uv run mkdocs build --strict
```

E aggiorna `course/progress.yaml`: stato, state machine e una nota che dica
cosa e' stato eseguito davvero. Se riscrivi una lezione gia' rivista, riporta
la state machine alla fase che il contenuto nuovo non ha ancora attraversato —
non lasciare `technical_review: done` su testo scritto dopo quella revisione.
