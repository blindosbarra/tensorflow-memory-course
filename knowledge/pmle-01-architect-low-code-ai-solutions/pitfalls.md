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
