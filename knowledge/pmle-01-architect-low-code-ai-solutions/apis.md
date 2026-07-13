# APIs: pmle-01-architect-low-code-ai-solutions

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud nel corso - vedi `course.yaml`, nota del modulo). I nomi
di prodotto/servizio sotto sono **quelli usati testualmente dalla exam
guide ufficiale** (fonte primaria, vedi evidence.yaml); i dettagli di
sintassi supplementari sono segnalati come tali.

## Nomi verificati sulla exam guide (Sezione 1)

- **BigQuery ML**: strumento per costruire modelli (classificazione,
  regressione, forecasting, clustering), fare feature engineering/
  selezione, generare predizioni, fare fine-tuning di modelli Gemini —
  tutto con BigQuery. **Stato: verified** (nome e attivita' elencati
  testualmente in 1.1).
- **Agent Platform AutoML**: strumento per addestrare modelli senza
  definire l'architettura. **Stato: verified** (nome testuale in 1.1).
- **Gemini Enterprise Agent Platform Model Garden**: catalogo per
  valutare e scegliere modelli fondazionali o open-source per un compito
  dato. **Stato: verified** (nome testuale in 1.2).
- **API di settore**: Document AI API, Vision API, Translate API, citate
  come esempi di API industry-specific. **Stato: verified** (nomi
  testuali in 1.2).
- **Modelli citati per uso/tuning specifico**: Gemini, Imagen, Veo, e
  "modelli come servizio" in Model Garden. **Stato: verified** (nomi
  testuali in 1.2).

## Dettagli di sintassi supplementari (non nella exam guide)

La exam guide elenca **attivita'** ("generating predictions using
BigQuery ML"), non sintassi SQL. I nomi di istruzione sotto sono
meccaniche di prodotto stabili e note, ma non riverificate su
`docs.cloud.google.com` in questa sessione (bloccato, vedi
`course/research_gaps.md`):

- `CREATE MODEL` (BigQuery ML): istruzione SQL che addestrerebbe un
  modello dentro BigQuery. **Stato: needs_reverification**.
- `ML.PREDICT` (BigQuery ML): funzione SQL che applicherebbe un modello
  addestrato a nuove righe. **Stato: needs_reverification**.
- `ML.EVALUATE` (BigQuery ML): funzione SQL per metriche di valutazione.
  **Stato: needs_reverification**.

Prima di usare questi tre nomi in uno studio d'esame definitivo,
verificarli contro `docs.cloud.google.com` (bloccato in questa sessione di
lavoro).
