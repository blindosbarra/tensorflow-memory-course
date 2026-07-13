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

## Hardware (3.3)

- **CPU, GPU, TPU**: opzioni di calcolo/acceleratore da valutare. **Stato:
  verified** (nomi testuali).
- **Parallelismo dei dati e del modello**: strategie di training
  distribuito su GPU/TPU citate dalla guida. **Stato: verified** che la
  guida nomina questi due termini; la spiegazione concettuale dei due
  termini in concepts.md è conoscenza ML generale, non specifica di
  prodotto — vedi evidence.yaml, **needs_reverification** per dettagli
  implementativi specifici Google Cloud.
