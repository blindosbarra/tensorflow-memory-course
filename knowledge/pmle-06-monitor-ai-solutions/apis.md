# APIs: pmle-06-monitor-ai-solutions

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud). I nomi sotto sono quelli usati testualmente dalla exam
guide ufficiale (fonte primaria, vedi evidence.yaml).

## Sicurezza e rischi (6.1)

- **Regex (espressioni regolari), filtri di sicurezza (safety filters)**:
  citati come strumenti per proteggere contro fughe di dati/modelli.
  **Stato: verified** (nomi testuali).
- **Model Armor**: citato come strumento di sicurezza. **Stato:
  verified** che il nome compare nella guida; nessun dettaglio
  implementativo affermato oltre al nome, prodotto troppo recente per
  conoscenza pre-addestramento affidabile (vedi
  `course/research_gaps.md`).
- **Agent Platform Inference**: citato come contesto per la spiegabilità
  del modello. **Stato: verified** che il nome compare nella guida
  (stesso nome citato nel Dominio 4 per lo scaling del serving);
  nessun dettaglio implementativo affermato.

## Monitoraggio (6.2)

- **Model Monitoring su Gemini Enterprise Agent Platform**: servizio per
  metriche di valutazione continua su modelli in produzione. **Stato:
  verified** (nome testuale).
- **Training-serving skew, data drift, concept drift, feature attribution
  drift**: quattro problemi di monitoraggio citati dalla guida. **Stato:
  verified** che la guida nomina questi quattro termini; le definizioni
  concettuali in concepts.md sono conoscenza ML generale, non specifica
  di prodotto — **needs_reverification** per dettagli implementativi
  Google Cloud specifici su come vengono misurati in pratica (vedi
  evidence.yaml).
