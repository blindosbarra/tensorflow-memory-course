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
