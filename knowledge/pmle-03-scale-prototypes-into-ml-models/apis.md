# APIs: pmle-03-scale-prototypes-into-ml-models

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud). I nomi sotto sono quelli usati testualmente dalla exam
guide ufficiale (fonte primaria, vedi evidence.yaml).

## Tipi di modello e prodotti (3.1)

- **ARIMA, DNN, LLM**: citati come esempi di tipo di modello tra cui
  scegliere in base al compito. **Stato: verified** (nomi testuali,
  nessun dettaglio implementativo affermato).
- **Agent Platform AutoML, BigQuery ML, Agent Platform Pipelines**: citati
  come esempi di prodotto tra cui scegliere. **Stato: verified** (stessi
  nomi già visti nel Dominio 1, qui riusati in un contesto di scelta più
  ampio).

## SDK e strumenti di training (3.2)

- **Agent Platform custom training**: training con codice proprio su
  Agent Platform. **Stato: verified** (nome testuale).
- **Kubeflow su Google Kubernetes Engine (GKE)**: orchestrazione di
  training containerizzato. **Stato: verified** (nome testuale).
- **Agent Platform AutoML**: stesso strumento del Dominio 1, qui citato
  come una delle opzioni di training. **Stato: verified**.
- **Tabular Workflows**: SDK specifico per dati tabellari. **Stato:
  verified** (nome testuale, nessun dettaglio d'uso affermato).
- **Cloud Storage, BigQuery**: citati come luoghi dove organizzare i dati
  di training. **Stato: verified** (nomi testuali).

## Dettaglio supplementare: cosa nasconde "DNN per pattern complessi"

- **CNN (rete convoluzionale)**: filtri piccoli (es. 3×3) riusati
  (parametri condivisi) in ogni posizione dell'immagine, invece di un
  peso dedicato per ogni pixel; molti meno parametri di una rete densa
  a parità di immagine (esempio verificato: 288 pesi per 32 filtri 3×3,
  contro 1.000.000 di pesi per una rete densa 10.000→100 su
  un'immagine 100×100). Un livello di pooling (es. max pooling) riduce
  la dimensione mantenendo il segnale più forte. **Stato:
  needs_reverification** (meccanica generale, non specifica di prodotto
  Google Cloud).
- **RNN (rete ricorrente), LSTM, GRU**: stato nascosto aggiornato passo
  per passo con pesi condivisi nel tempo; soggetta a gradiente che
  svanisce/esplode su sequenze lunghe (backpropagation through time);
  LSTM/GRU aggiungono gate per attenuare il problema. **Stato:
  needs_reverification**.
- **Transformer**: architettura usata dai moderni modelli fondazionali
  di testo (Model Garden, Dominio 1), elabora la sequenza in parallelo
  con un meccanismo di attenzione invece che passo-passo come una RNN.
  **Stato: needs_reverification** (non afferma quale architettura
  esatta usi internamente un modello Gemini specifico, solo che la
  famiglia Transformer ha sostituito le RNN per il testo nei modelli
  fondazionali moderni in generale).

## Dettaglio supplementare: come si sottomette davvero un training job

- **Worker pool spec**: container image, machine type, tipo/numero di
  acceleratori, numero di repliche; per training distribuito, un pool
  chief/master + uno o più worker pool. **Stato: needs_reverification**.
- **Hyperparameter tuning**: spazio di ricerca (es. learning rate
  continuo su scala log, batch size discreto) + metrica obiettivo,
  ottimizzazione bayesiana su più trial in parallelo, non grid search
  esaustiva. **Stato: needs_reverification**.
- **Troubleshooting comune**: VM preemptible/spot senza checkpoint →
  progresso perso a ogni interruzione; errore di memoria esaurita
  sull'acceleratore → ridurre `batch_size` prima di sospettare
  l'architettura; quote regionali GPU/TPU come blocco pratico distinto
  da un problema ML. **Stato: needs_reverification**.

## Hardware (3.3)

- **CPU, GPU, TPU**: opzioni di calcolo/acceleratore da valutare. **Stato:
  verified** (nomi testuali).
- **Parallelismo dei dati e del modello**: strategie di training
  distribuito su GPU/TPU citate dalla guida. **Stato: verified** che la
  guida nomina questi due termini; la spiegazione concettuale dei due
  termini in concepts.md è conoscenza ML generale, non specifica di
  prodotto — vedi evidence.yaml, **needs_reverification** per dettagli
  implementativi specifici Google Cloud.
