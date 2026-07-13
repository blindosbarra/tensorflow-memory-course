# APIs: pmle-04-serve-and-scale-models

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud). I nomi sotto sono quelli usati testualmente dalla exam
guide ufficiale (fonte primaria, vedi evidence.yaml).

## Servizi di serving (4.1)

- **Agent Platform, Model Garden, Cloud Run, GKE**: citati come servizi
  appropriati per deployare inferenza batch e online. **Stato: verified**
  (nomi testuali, nessuna guida su quando scegliere quale oltre
  all'elenco stesso).
- **PyTorch, XGBoost**: citati come framework di provenienza dei modelli
  da servire, con container predefiniti o personalizzati. **Stato:
  verified** (nomi testuali).
- **Gemini Enterprise Agent Platform Model Registry**: sistema per
  organizzare e versionare modelli. **Stato: verified** (nome testuale).
- **A/B testing, canary deployment**: strategie di rollout citate dalla
  guida per confrontare versioni di modello. **Stato: verified** che la
  guida nomina questi due termini; la spiegazione concettuale in
  concepts.md è conoscenza generale di deployment, non specifica di
  prodotto — **needs_reverification** per dettagli implementativi Google
  Cloud specifici (vedi evidence.yaml).

## Scaling e hardware (4.2)

- **Agent Platform Feature Store**: stesso Feature Store del Dominio 2,
  qui usato per servire feature in modo coerente col training. **Stato:
  verified** (nome testuale).
- **Endpoint pubblici e privati**: due modalità di distribuzione citate.
  **Stato: verified** (nomi testuali, nessun dettaglio di configurazione
  affermato).
- **CPU, GPU, TPU, edge**: opzioni di hardware per il serving, incluso
  "edge" (dispositivi periferici fuori dal cloud). **Stato: verified**
  (nomi testuali).
- **Gemini Enterprise Agent Platform Inference**: componente citato per
  scalare il backend di serving in base al throughput. **Stato:
  verified** che il nome compare nella guida; nessun dettaglio
  implementativo affermato oltre al nome, prodotto troppo recente per
  conoscenza pre-addestramento affidabile (vedi
  `course/research_gaps.md`).
- **Containerized serving**: citato come alternativa/complemento per
  scalare il serving. **Stato: verified** (termine testuale).
