# Pitfalls: pmle-01-architect-low-code-ai-solutions

- Scegliere sempre la soluzione custom (rete scritta a mano) per abitudine,
  anche quando un problema tabellare standard risolvibile in BigQuery ML o
  AutoML costerebbe meno tempo e produrrebbe un risultato comparabile:
  l'esame valuta la scelta dello strumento minimo sufficiente, non la
  padronanza tecnica massima.
- Confondere "basso codice" con "nessuna competenza richiesta": scegliere
  bene tra BigQuery ML, AutoML e un modello fondazionale richiede comunque
  capire il tipo di problema (classificazione vs forecasting vs
  generazione) e i vincoli di costo/latenza.
- Dare per scontata la sintassi esatta di BigQuery ML (`CREATE MODEL`,
  `ML.PREDICT`) come materiale d'esame: la guida valuta la scelta dello
  strumento e l'attivita' svolta, non la sintassi SQL precisa, che qui
  resta comunque `needs_reverification` (vedi apis.md).
- Assumere che "Gemini Enterprise Agent Platform" sia sinonimo
  intercambiabile del vecchio nome "Vertex AI" usato in materiale piu'
  datato: il nome attuale e' verificato sulla exam guide primaria, ma la
  guida stessa non definisce il rapporto storico tra i due nomi — non va
  quindi assunto senza controllo sulla documentazione prodotto corrente.
- Dimenticare la clausola `TRANSFORM` in BigQuery ML e riscrivere a mano
  la stessa logica di preprocessing sia prima del training sia prima di
  ogni chiamata a `ML.PREDICT`: è esattamente il tipo di duplicazione che
  causa training-serving skew (vedi Domini 4-5), e `TRANSFORM` esiste per
  evitarla.
- Scegliere il fine-tuning completo di un modello fondazionale come prima
  opzione, senza prima provare prompting/RAG o un tuning efficiente in
  parametri: è l'opzione più costosa delle tre, da riservare ai casi in
  cui le altre due non bastano.
- Non normalizzare le feature prima di addestrare un `LOGISTIC_REG` o un
  `DNN_CLASSIFIER` (es. lasciare `spesa_mensile_eur` e
  `ticket_aperti_90gg` sulle scale numeriche originali): il gradiente
  della feature a scala maggiore domina l'aggiornamento e il modello
  fatica a imparare dalle feature a scala più piccola. Applicare la
  stessa normalizzazione a un `BOOSTED_TREE_CLASSIFIER` invece non serve
  a nulla (gli alberi sono invarianti alla scala): sapere quale model_type
  ne ha bisogno evita lavoro inutile o, peggio, la sua omissione dove
  serve davvero.
- Guardare solo l'accuracy di `ML.EVALUATE` su un problema con classi
  sbilanciate (es. 20% di clienti che non rinnovano): un modello che
  predicesse sempre la classe maggioritaria avrebbe comunque un'accuracy
  alta senza essere utile — precision, recall e F1 vanno guardati insieme
  all'accuracy, non al suo posto.
- Usare `softmax` su un problema multi-etichetta (classi non mutuamente
  esclusive): forza le probabilità a sommare a 1 e sopprime
  artificialmente etichette corrette che dovrebbero poter essere vere
  insieme. Serve `sigmoid` indipendente su ciascun neurone di output.
- Guardare l'accuracy aggregata o il micro-average su un problema
  multi-classe sbilanciato: entrambi pesano di fatto ogni singolo
  esempio, quindi le classi comuni nascondono un recall pessimo su una
  classe rara. Solo il macro-average tratta ogni classe allo stesso
  modo indipendentemente da quanti esempi ha.
- Usare una metrica non derivabile (es. accuracy) come loss da
  minimizzare direttamente: il suo gradiente è quasi ovunque zero,
  quindi non dà all'optimizer nessuna informazione utile su come
  aggiustare i pesi — loss e metrica hanno scopi diversi e non sono
  intercambiabili.
