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
- Trattare "Gemini Enterprise Agent Platform" e "Vertex AI" come sinonimi
  certi senza verifica: la relazione esatta tra i due nomi non e'
  confermata in questo repository (vedi `course/research_gaps.md`) e va
  controllata sulla documentazione ufficiale corrente prima di un esame
  reale.
