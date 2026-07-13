# Pitfalls: pmle-06-monitor-ai-solutions

- Monitorare solo l'accuratezza aggregata di un modello in produzione,
  senza controllare la distribuzione dei dati in ingresso o l'importanza
  delle feature: un problema di data drift o feature attribution drift
  può essere invisibile finché non è già serio.
- Trattare la sicurezza di un'applicazione con LLM come un problema
  risolto una volta, in fase di sviluppo, invece che come monitoraggio
  continuo: nuovi tentativi di prompt malevolo o di esfiltrazione dati
  possono emergere dopo il rilascio.
- Confondere data drift e concept drift, applicando la correzione
  sbagliata (es. raccogliere più dati simili quando in realtà è la
  relazione input-target che è cambiata, non la distribuzione dei dati).
- Ignorare pratiche di AI responsabile (monitoraggio del bias) come
  separate dal monitoraggio "tecnico": la sottosezione 6.1 le tratta come
  parte della stessa competenza di identificazione dei rischi.
