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

### Normalizzazione delle feature: perché serve per alcuni model_type e non per altri

`LOGISTIC_REG` e `DNN_CLASSIFIER` si addestrano per discesa del
gradiente: il peso di ciascuna feature si aggiorna in proporzione al
valore della feature. Feature su scale molto diverse (es. spesa mensile
in euro nell'ordine delle migliaia contro un conteggio di ticket
nell'ordine delle decine) fanno sì che il gradiente della feature a
scala maggiore domini l'aggiornamento, rallentando o degradando la
convergenza sulle altre. La correzione standard è la standardizzazione
z-score: `z = (x - media) / deviazione_standard`, calcolata sui dati di
training. In BigQuery ML si applica con `ML.STANDARD_SCALER(...)`
dentro la clausola `TRANSFORM`; media e deviazione standard usate sono
salvate con il modello e riapplicate identiche a ogni `ML.PREDICT`, così
il train/serve non diverge anche sulla normalizzazione stessa. I
model_type ad albero (`BOOSTED_TREE_CLASSIFIER`/`_REGRESSOR`) non ne
hanno bisogno: un albero decide i tagli confrontando l'ordine dei valori
di una feature, non la loro grandezza assoluta, quindi la scala non
influisce sull'addestramento. **Stato: needs_reverification** (meccanismo
di discesa del gradiente e formula z-score sono conoscenza ML generale;
`ML.STANDARD_SCALER` come nome di funzione specifico non riverificato su
documentazione live in questa sessione).

### Valutare un classificatore con numeri veri: dalla matrice di confusione alle metriche

`ML.CONFUSION_MATRIX` restituisce conteggi di veri/falsi positivi/
negativi; `ML.EVALUATE` li trasforma in metriche leggibili. Su un esempio
costruito (200 casi, 40 positivi reali, matrice 28 TP / 12 FN / 18 FP /
142 TN): `precision = TP/(TP+FP) = 28/46 ≈ 0.61`, `recall = TP/(TP+FN) =
28/40 = 0.70`, `F1 = 2·precision·recall/(precision+recall) ≈ 0.65`,
`accuracy = (TP+TN)/totale = 170/200 = 0.85`. L'accuracy da sola è
fuorviante quando le classi sono sbilanciate: un modello che predicesse
sempre la classe maggioritaria otterrebbe comunque l'80% di accuracy in
questo esempio (160/200), senza intercettare un solo caso positivo — è
il motivo per cui `ML.EVALUATE` restituisce anche precision/recall/F1.
Quale metrica pesa di più dipende dal costo relativo di falsi positivi e
falsi negativi nel problema di business: se un falso negativo (mancare
un caso positivo) costa più di un falso positivo (un falso allarme), si
preferisce un modello con recall più alto, ottenibile abbassando la
soglia di decisione sulla probabilità restituita da `ML.PREDICT`. **ROC
AUC** misura la capacità del modello di ordinare correttamente i casi
positivi sopra i negativi, indipendentemente dalla soglia scelta (0.5 =
casuale, 1.0 = separazione perfetta) — utile per confrontare modelli
prima di scegliere dove mettere la soglia. **Stato: needs_reverification**
(formule standard di conoscenza ML generale, stesse della Lezione 13 del
corso principale; la matrice di confusione e i numeri sono un esempio
didattico costruito, non un output reale).

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

### Loss function, optimizer, metrica: come scegliere

- **Loss per tipo di problema**: regressione → `MSE` (penalizza gli
  errori grandi, sensibile agli outlier), `MAE` (penalità lineare, più
  robusta agli outlier), `Huber loss` (compromesso). Classificazione
  binaria → `binary cross-entropy` con un neurone di output e
  attivazione `sigmoid`. Classificazione multi-classe mutuamente
  esclusiva → `categorical`/`sparse categorical cross-entropy` con N
  neuroni di output e attivazione `softmax` (probabilità che sommano a
  1). Classificazione multi-etichetta (classi non esclusive) →
  `binary cross-entropy` per etichetta, con `sigmoid` indipendente su
  ciascun neurone, non `softmax`. **Stato: needs_reverification**
  (definizioni matematiche standard, stesse della Lezione 9 del corso
  principale).
- **Softmax, esempio numerico verificato**: logit `[2,0; 1,0; 0,1]` →
  `e^2,0≈7,39`, `e^1,0≈2,72`, `e^0,1≈1,10`, somma≈11,21 →
  `P=[0,66; 0,24; 0,10]` (somma 1,00). Categorical cross-entropy per la
  classe corretta (prima) = `-log(0,66)≈0,42`. **Stato:
  needs_reverification** (formule standard; numeri usati come esempio
  didattico verificato aritmeticamente, non output reale).
- **Optimizer**: `SGD` (aggiornamento base scalato dal learning rate),
  `SGD+momentum` (media mobile degli aggiornamenti passati, accelera la
  convergenza), `RMSprop` (learning rate adattivo per singolo peso),
  `Adam` (momentum + adattamento per-peso, scelta di default comune,
  richiede poco tuning). Il learning rate è l'iperparametro più
  sensibile: troppo alto → la loss di training oscilla o diverge; troppo
  basso → progresso quasi impercettibile. **Stato: needs_reverification**
  (meccaniche generali di ottimizzazione, stesse della Lezione 11 del
  corso principale con `GradientTape`).
- **Loss vs metrica**: la loss deve essere derivabile (l'optimizer ne usa
  il gradiente); la metrica no — l'accuracy è una pessima loss diretta
  (gradiente quasi ovunque zero) ma una metrica ragionevole da riportare.
  In multi-classe, precision/recall/F1 per classe vanno aggregati con
  **macro-average** (media semplice, fa emergere un problema su una
  classe rara), **micro-average** (aggrega TP/FP/FN su tutte le classi
  prima di calcolare, le classi comuni dominano — stesso limite
  dell'accuracy aggregata), o **weighted average** (macro pesato per il
  supporto di ciascuna classe). **Stato: needs_reverification**
  (conoscenza ML generale standard, stessa della Lezione 13 del corso
  principale).
