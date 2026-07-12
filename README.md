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

1. `notebooks/lezione-01-dati-mancanti.ipynb` — dati mancanti:
   teoria (meccanismi, strategie, effetti) + progetto passo 1 (ingestion).
2. `notebooks/lezione-02-duplicati-tipi-outlier.ipynb` — duplicati, tipi errati
   e outlier + progetto passo 2 (controllo qualita' del nuovo batch).
3. `notebooks/lezione-03-train-validation-test.ipynb` — valutare senza barare:
   i tre insiemi e i tre tipi di divisione + progetto passo 3 (lo storico
   viene diviso temporalmente).
4. `notebooks/lezione-04-data-leakage.ipynb` — le tre forme di leakage, con
   dimostrazioni numeriche + progetto passo 4 (audit anti-leakage degli split).
5. `notebooks/lezione-05-encoding-scaling.ipynb` — encoding e scaling + progetto
   passo 5 (la prima matrice di feature, pronta per la Fase 2).
6. `notebooks/lezione-06-numpy.ipynb` — pensare per array: vettorizzazione,
   riduzioni, maschere + progetto passo 6 (le firme delle classi).
7. `notebooks/lezione-07-tensori.ipynb` — forme, prodotto scalare come somma
   pesata, `X @ W` + progetto passo 7 (i punteggi di classe, pesi casuali).
8. `notebooks/lezione-08-gradienti.ipynb` — derivate come sensibilita',
   discesa del gradiente + progetto passo 8 (i primi parametri imparati).
9. `notebooks/lezione-09-loss.ipynb` — MSE, softmax e cross-entropy +
   progetto passo 9 (softmax regression a mano: la baseline della Fase 2).
10. `notebooks/lezione-10-prima-rete-neurale.ipynb` — Keras: non-linearita'
    e confini curvi (mezzelune) + progetto passo 10 (la rete sfida la
    baseline). Da qui serve `uv sync --extra ml`.
11. `notebooks/lezione-11-dentro-il-training.ipynb` — batch, epoche,
    autodiff e il training loop scritto a mano + progetto passo 11.
12. `notebooks/lezione-12-overfitting.ipynb` — curve di apprendimento,
    early stopping, dropout + progetto passo 12 (valutazione finale sul
    test e primo modello salvato).
13. `notebooks/lezione-13-valutare-un-classificatore.ipynb` — precision,
    recall, F1, confusion matrix, calibrazione + progetto passo 13 (la
    pagella del classificatore).
14. `notebooks/lezione-14-tf-data.ipynb` — pipeline di input: shuffle (e la
    trappola del buffer), batch, prefetch + progetto passo 14.
15. `notebooks/lezione-15-tokenizzazione.ipynb` — il modello legge il
    testo: vocabolario, OOV, bag of words + progetto passo 15 (il salto:
    ~60% -> ~95% su validation).

I notebook vanno eseguiti in ordine: ogni lezione riparte dagli artifact
salvati dalla precedente. Le pagine in `docs/modules/` sono i riassunti di
riferimento pubblicati sul sito. I moduli `examples/` e `src/memory_ai/` sono
implementazione di riferimento della pipeline, non materiale di studio.
