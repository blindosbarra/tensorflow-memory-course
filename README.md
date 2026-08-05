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

Il corso e' strutturato in 60 lezioni principali in `notebooks/` (suddivise per fasi di apprendimento), un notebook consolidato e un modulo supplementare di certificazione GCP PMLE:

### Corso Principale: Memory AI Lab (Lezioni 1–60)
- **Fase 1 & 0 — Dati e Fondamenti (Lezioni 01–09, 14)**: da pulizia dati, train/val/test e leakage fino a NumPy, gradienti, loss e input pipeline `tf.data`.
- **Fase 2 — Keras e Reti Neurali Dense (Lezioni 10–13)**: prima rete neurale Keras, training loop custom con `GradientTape`, overfitting, dropout e metriche di calibrazione.
- **Fase 3 — Testo, Embedding e Retrieval (Lezioni 15–21)**: tokenizzazione, embedding layer, cosine similarity, PCA/UMAP, clustering K-Means e metriche di retrieval (Recall@K, MRR).
- **Fase 4 — Schema e Grafo delle Memorie (Lezioni 22–29)**: schema di memoria `@dataclass`, decadimento temporale, importanza composita, entita' e grafo relazionale `NetworkX`, retrieval ibrido e gestione contraddizioni.
- **Fase 5 — Transformer e Gemma (Lezioni 30–37)**: self-attention matematica da zero, blocco Transformer, tokenizer, `KerasHub`, inferenza Gemma, output strutturato e valutazione generativa.
- **Fase 6 — LoRA e QLoRA (Lezioni 38–44)**: transfer learning, matematica di LoRA, LoRA da zero e su Gemma, QLoRA e impacchettamento adapter.
- **Fase 7 — Preference Learning (Lezioni 45–51)**: feedback schema, coppie chosen/rejected, reward function, DPO, RLHF/RLAIF e rischi del learning online.
- **Fase 8 — Capstone Memory AI Lab (Lezioni 52–60)**: architettura end-to-end, dataset, classificatore, embedding graph, Gemma+LoRA, valutazione offline, pipeline, monitoring e demo finale.

### Notebook Consolidato
- `notebooks/consolidato-memoria-lezioni-01-15.ipynb` — riepilogo end-to-end eseguibile delle prime 15 lezioni sulla preparazione dati e baseline neurale.

### Certificazione GCP Professional ML Engineer (facoltativo)
- **Domini 1–6 e Sintesi Architetturale** (`pmle-01` .. `pmle-07`): teoria e scenari di architetture low-code, Feature Store, AutoSxS, serving, pipeline MLOps e monitoring. Disponibile in italiano (`docs/modules/pmle-*.md`) e in inglese (`docs/modules/en/pmle-*.md`).

I notebook vanno eseguiti in ordine: ogni lezione riparte dagli artifact
salvati dalla precedente. Le pagine in `docs/modules/` sono i riassunti di
riferimento pubblicati sul sito. I moduli `examples/` e `src/memory_ai/` sono
implementazione di riferimento della pipeline, non materiale di studio.
