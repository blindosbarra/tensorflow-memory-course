# APIs: pmle-07-architetture-end-to-end

Nessun notebook eseguibile (teoria pura, nessuna credenziale cloud). A
differenza delle lezioni pmle-01..06, qui non c'è un elenco di nomi
verificati contro la exam guide: ogni prodotto citato in questa lezione
è già stato verificato/marcato needs_reverification nella lezione di
dominio corrispondente (vedi tabella sotto), e questa lezione lo
riutilizza senza riverificarlo una seconda volta.

## Prodotti riutilizzati, e dove sono già documentati

- **BigQuery ML** (`CREATE MODEL`, `TRANSFORM`, `ML.ONE_HOT_ENCODER`,
  `ML.STANDARD_SCALER`, `ML.TRAINING_INFO`, `ML.EVALUATE`): vedi
  `knowledge/pmle-01-architect-low-code-ai-solutions/apis.md`.
  `ML.TRAINING_INFO` (metriche per iterazione durante il training di un
  modello ad albero) è un dettaglio aggiuntivo non descritto nella
  lezione pmle-01: **Stato: needs_reverification** (nome di funzione
  plausibile per il caso d'uso descritto — seguire l'andamento
  dell'addestramento per iterazione — ma non verificato su
  documentazione live in questa sessione).
- **AutoML** (ricerca architetturale, transfer learning): vedi
  `knowledge/pmle-01-architect-low-code-ai-solutions/apis.md`.
- **Feature Store** (entity type, lettura online/offline, correttezza
  point-in-time): vedi
  `knowledge/pmle-02-collaborate-manage-data-models/apis.md`.
- **AutoSxS / LLM-as-a-judge**: citato solo nella tabella di confronto
  MLOps, non riusato in dettaglio qui — vedi
  `knowledge/pmle-02-collaborate-manage-data-models/apis.md`.
- **Model Monitoring, tipi di drift**: vedi
  `knowledge/pmle-06-monitor-ai-solutions/concepts.md`.
- **Model Armor**: citato solo per nome nella tabella MLOps, coerente con
  come è trattato in `knowledge/pmle-06-monitor-ai-solutions/apis.md`
  (nome troppo recente per dettaglio implementativo affidabile).

## Dettaglio supplementare specifico di questa lezione

- **`ML.TRAINING_INFO`**: funzione ipotizzata per illustrare come si
  osserverebbe un andamento di overfitting per iterazione su un modello
  ad albero in BigQuery ML (training AUC che continua a salire, validation
  AUC che ristagna). **Stato: needs_reverification** — non verificato che
  questo sia il nome esatto o il comportamento esatto della funzione reale
  in BigQuery ML.
- **Opzioni di regolarizzazione per `BOOSTED_TREE_CLASSIFIER`/`_REGRESSOR`
  citate** (`max_tree_depth`, `l2_reg`, `subsample`, `early_stop`):
  nomi di opzioni plausibili per un modello ad albero con boosting del
  gradiente (la stessa famiglia di iperparametri di XGBoost/LightGBM),
  non verificati uno per uno contro la sintassi esatta di BigQuery ML in
  questa sessione. **Stato: needs_reverification**.
