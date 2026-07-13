# APIs: pmle-01-architect-low-code-ai-solutions

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud nel corso - vedi `course.yaml`, nota del modulo). Le API
citate qui sono descrizioni concettuali per l'esame, non codice testato in
questo repository.

- `CREATE MODEL` (BigQuery ML): istruzione SQL che addestra un modello
  dentro BigQuery, specificando `model_type` (es. `LOGISTIC_REG`,
  `LINEAR_REG`, `KMEANS`, `ARIMA_PLUS`, `BOOSTED_TREE_CLASSIFIER`) e i dati
  di training via una query. **Stato: needs_reverification**, vedi
  evidence.yaml.
- `ML.PREDICT` (BigQuery ML): funzione SQL che applica un modello
  addestrato a nuove righe, restituendo predizioni come colonne aggiuntive.
  **Stato: needs_reverification**.
- `ML.EVALUATE` (BigQuery ML): funzione SQL che calcola le metriche di
  valutazione standard (accuratezza, precision/recall per classificazione;
  RMSE per regressione) su un modello addestrato. **Stato:
  needs_reverification**.
- AutoML (Vertex AI): interfaccia (console o SDK) per addestrare modelli
  tabulari/immagine/testo/video senza definire l'architettura; il servizio
  gestisce ricerca dell'architettura e tuning degli iperparametri.
  **Stato: needs_reverification**.

Prima di usare questi nomi in materiale da studio definitivo, verificarli
contro `docs.cloud.google.com` (bloccato in questa sessione di lavoro, vedi
`course/research_gaps.md`).
