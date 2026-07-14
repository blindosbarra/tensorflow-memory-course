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

## Meccaniche supplementari (non nella exam guide, conoscenza generale)

La exam guide elenca **attivita'** ("generating predictions using
BigQuery ML"), non il "come". Le sezioni sotto spiegano il meccanismo
reale, non solo il nome dello strumento — aggiunte su richiesta esplicita
dello studente dopo che la prima versione di questa lezione si fermava a
elencare i nomi. Conoscenza generale pre-addestramento, non riverificata
su `docs.cloud.google.com` in questa sessione (bloccato, vedi
`course/research_gaps.md`); marcata `needs_reverification` in
evidence.yaml.

### BigQuery ML: come si addestra e si valuta un modello

- `CREATE MODEL nome_dataset.nome_modello OPTIONS(model_type='...',
  input_label_cols=['colonna_target']) AS SELECT ...`: un'unica
  istruzione SQL che addestra il modello sui risultati della query. Il
  `model_type` sceglie l'algoritmo — elenco con cosa fa davvero ciascuno,
  non solo il nome:
    - `LINEAR_REG`: retta/iperpiano tra le feature e un target numerico
      continuo (regressione). Semplice e interpretabile, cattura solo
      relazioni lineari.
    - `LOGISTIC_REG`: come sopra ma per un target categorico (tipicamente
      binario); nonostante il nome è classificazione, non regressione.
    - `KMEANS`: clustering non supervisionato — raggruppa righe simili
      senza un target da prevedere, a differenza di tutti gli altri
      model_type di questa lista.
    - `ARIMA_PLUS`: serie storiche — prevede un valore futuro dal proprio
      andamento passato nel tempo (trend, stagionalità), non da feature
      indipendenti.
    - `BOOSTED_TREE_CLASSIFIER`/`_REGRESSOR`: alberi decisionali costruiti
      in sequenza (stessa famiglia di XGBoost), ognuno che corregge gli
      errori del precedente; cattura relazioni non lineari, spesso la
      scelta più performante su dati tabellari strutturati.
    - `DNN_CLASSIFIER`/`_REGRESSOR`: rete neurale densa (stessa famiglia
      delle Lezioni 5-7 del corso principale); utile per relazioni
      complesse tra le feature, richiede più dati/tempo delle opzioni
      sopra per dare un vantaggio reale.
    - `AUTOML_CLASSIFIER`/`_REGRESSOR`: delega la scelta dell'algoritmo e
      degli iperparametri alla ricerca di AutoML (vedi sotto) invece di
      fissarne uno esplicitamente.

  **Stato: needs_reverification** (elenco indicativo, non necessariamente
  completo o aggiornato).
- Clausola `TRANSFORM(...)`: dentro `CREATE MODEL` si possono dichiarare
  le trasformazioni di feature (es. `ML.STANDARD_SCALER`,
  `ML.BUCKETIZE`, `ML.ONE_HOT_ENCODER`) una sola volta; BigQuery ML le
  riapplica automaticamente e in modo identico a ogni chiamata di
  `ML.PREDICT`, senza che chi chiama la predizione debba ripetere la
  logica di preprocessing. Questo è il motivo tecnico per cui BigQuery
  ML evita per costruzione il training-serving skew descritto nel
  Dominio 4/5 di questo corso: la trasformazione vive in un solo posto.
  **Stato: needs_reverification**.
- `ML.PREDICT(MODEL nome_modello, (SELECT ...))`: applica il modello
  addestrato a nuove righe, restituendo una colonna di predizione (e, per
  la classificazione, le probabilità per classe). **Stato:
  needs_reverification**.
- `ML.EVALUATE(MODEL nome_modello)`: restituisce le metriche appropriate
  al tipo di modello — precision, recall, accuracy, F1, log loss e ROC
  AUC per la classificazione; errore assoluto medio, errore quadratico
  medio e R² per la regressione. `ML.CONFUSION_MATRIX` restituisce la
  matrice di confusione separatamente. **Stato: needs_reverification**
  (per il significato di ciascuna metrica, vedi Lezione 13 del corso
  principale, che le tratta con codice eseguito).

### AutoML: cosa fa davvero durante il training

AutoML non prova "un" modello: cerca, all'interno di un budget di
calcolo/tempo che l'utente imposta, molte combinazioni candidate di
architettura e iperparametri in parallelo (per immagini e testo, spesso
partendo da backbone pre-addestrati con transfer learning invece che da
zero), e seleziona la combinazione con la performance migliore su uno
split di validazione tenuto da parte. È automazione della ricerca che un
data scientist farebbe a mano per tentativi — non una tecnica diversa,
ma la stessa ricerca fatta più in fretta e su più candidati
contemporaneamente. **Stato: needs_reverification** (meccanismo generale
della famiglia di prodotti; budget e soglie esatte non affermati qui).

### Tuning di un modello fondazionale: quando conviene

Tre livelli di intervento, in ordine di costo crescente: **prompting** (o
RAG, recupero di contesto pertinente prima della generazione) non
aggiorna nessun peso del modello ed è il modo più veloce ed economico di
iterare; il **tuning efficiente in parametri** (es. LoRA) allena piccole
matrici di adattamento aggiuntive invece di tutti i pesi del modello,
adattando il comportamento oltre ciò che il solo prompting raggiunge, a
una frazione del costo del fine-tuning completo; il **fine-tuning
completo** aggiorna tutti i pesi su un dataset etichettato specifico per
il compito ed è l'opzione più costosa. Questo è il ragionamento dietro il
bullet della sottosezione 1.1 "fine-tuning Gemini models using BigQuery":
si sceglie il fine-tuning quando prompting e tuning efficiente non
bastano a ottenere il comportamento richiesto, non come prima opzione.
**Stato: needs_reverification** (conoscenza ML generale, non specifica
di un prodotto Google Cloud).
