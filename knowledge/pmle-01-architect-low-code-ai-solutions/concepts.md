# Concepts: pmle-01-architect-low-code-ai-solutions

Decisione research: contenuto principale (pesi, sottosezioni 1.1/1.2,
terminologia) `VERIFIED` contro il testo verbatim della exam guide
ufficiale (vedi evidence.yaml). Cinque claim supplementari sui meccanismi
reali (sintassi/TRANSFORM/ML.EVALUATE di BigQuery ML, ricerca
architetturale di AutoML, framework prompting-vs-tuning) restano
`needs_reverification` e sono segnalati esplicitamente dove usati — vedi
apis.md per il dettaglio.

## Concetti coperti

1. Il Dominio 1 dell'esame ("Architecting low-code AI solutions", **~13%
   del peso, dato ufficiale dalla exam guide**) valuta la capacita' di
   **scegliere lo strumento con il minimo codice necessario** per un
   problema di ML dato, non di scrivere quel codice a mano.
2. La sottosezione 1.1 (sviluppo modelli con BigQuery ML o AutoML su
   Gemini Enterprise Agent Platform) copre cinque attivita' verificate
   testualmente sulla guida: costruire modelli in BigQuery ML o Agent
   Platform AutoML per classificazione/regressione/forecasting/clustering
   in base al problema di business; feature engineering/selezione con
   BigQuery ML; generare predizioni con BigQuery ML; addestrare modelli
   con Agent Platform AutoML; fare fine-tuning di modelli Gemini con
   BigQuery.
3. La sottosezione 1.2 (soluzioni AI con API Google Cloud o modelli
   fondazionali) copre quattro attivita': valutare e scegliere il modello
   giusto da Gemini Enterprise Agent Platform Model Garden; costruire
   applicazioni con API di settore (Document AI, Vision, Translate);
   costruire soluzioni e fare tuning di modelli per casi d'uso specifici
   (Gemini, Imagen, Veo, modelli come servizio in Model Garden);
   ottimizzare applicazioni basate su Gemini per costo, latenza e
   disponibilita'.
4. Due famiglie di strumenti low-code con casi d'uso distinti:
   - **BigQuery ML**: addestri e servi modelli con SQL, dentro il
     data warehouse dove i dati gia' vivono. Adatto quando i dati sono
     gia' in BigQuery e il problema e' tabellare/serie storiche.
   - **AutoML (su Agent Platform)**: addestri modelli su dati
     tabellari, immagini, testo, video, senza scrivere l'architettura del
     modello. Adatto quando serve un modello di produzione senza
     competenze di deep learning specializzate.
5. Una terza via: usare **API o modelli fondazionali gia' pronti** (non
   addestrare nulla, solo integrare) quando il compito rientra in
   capacita' generiche (visione, linguaggio, generazione), valutando
   costo/latenza/disponibilita' come vincoli di progettazione, non solo
   come dettagli implementativi.

## Collegamento al resto del corso

Le lezioni 1-15 del corso principale insegnano a costruire un
classificatore **da zero** (NumPy, poi Keras) per capire *cosa* fa un
modello. Questo modulo insegna la decisione opposta e complementare:
*quando NON serve costruirlo da zero* perche' uno strumento gestito
risolve lo stesso problema piu' in fretta. Sono competenze diverse:
capire il modello (corso principale) vs scegliere lo strumento giusto per
il contesto aziendale (questo modulo).

## Come funzionano davvero gli strumenti (meccaniche, non solo nomi)

Aggiunto dopo un primo giro in cui la lezione elencava le attivita' della
exam guide senza spiegare il meccanismo sottostante — feedback diretto
dello studente ("non e' un corso, e' un syllabus"). Vedi apis.md per il
dettaglio completo, marcato `needs_reverification` come conoscenza
generale non riverificata su documentazione live:

- BigQuery ML: `CREATE MODEL` con un `model_type` che sceglie
  l'algoritmo, una clausola `TRANSFORM` opzionale che rende il
  preprocessing riproducibile automaticamente tra training e predizione,
  `ML.PREDICT`/`ML.EVALUATE`/`ML.CONFUSION_MATRIX` per predire e valutare.
- Normalizzazione delle feature (z-score via `ML.STANDARD_SCALER` dentro
  `TRANSFORM`): necessaria per model_type che si addestrano per discesa
  del gradiente (`LOGISTIC_REG`, `DNN_CLASSIFIER`), inutile per model_type
  ad albero (`BOOSTED_TREE_*`). Spiegata con un esempio numerico
  costruito (media/deviazione standard/valori cliente), non dati reali.
- Lettura di `ML.EVALUATE` con una matrice di confusione calcolata a
  mano su un esempio costruito: precision/recall/F1/accuracy/ROC AUC,
  perché l'accuracy da sola è fuorviante su classi sbilanciate, e come il
  costo relativo di falsi positivi/negativi guida la scelta della soglia
  di decisione su `ML.PREDICT`.
- AutoML: ricerca automatica di architettura e iperparametri dentro un
  budget di calcolo, spesso con transfer learning da backbone
  pre-addestrati per immagini/testo.
- Loss function per tipo di problema (regressione, binaria, multi-classe
  esclusiva, multi-etichetta), con un esempio numerico verificato di
  softmax + categorical cross-entropy; optimizer (SGD, momentum,
  RMSprop, Adam) e sensibilità del learning rate; differenza tra loss
  (derivabile, ottimizzata) e metrica (riportata a un umano); le tre
  modalità di aggregazione precision/recall/F1 in multi-classe (macro/
  micro/weighted) e perché solo il macro-average fa emergere un problema
  su una classe rara. Aggiunto su richiesta esplicita dello studente
  ("explain optimization function, loss function and metrics... binary
  classification vs probabilities for multi class").
- Tuning di modelli fondazionali: prompting/RAG (nessun peso aggiornato)
  < tuning efficiente come LoRA (poche matrici aggiuntive) < fine-tuning
  completo (tutti i pesi) — in ordine di costo crescente, e il
  fine-tuning si sceglie solo quando i primi due non bastano.

## Limiti

Il nome "Gemini Enterprise Agent Platform" e' verificato testualmente
come terminologia della guida stessa; il suo rapporto storico esatto con
il nome precedente "Vertex AI" non e' affermato dalla guida e non viene
quindi affermato qui.
