# Pitfalls: pmle-03-scale-prototypes-into-ml-models

- Scegliere il tipo di modello più potente disponibile (es. un LLM per un
  problema di forecasting tabellare semplice) invece di quello adatto al
  compito: la sottosezione 3.1 valuta la scelta motivata da costo,
  complessità, latenza e scalabilità, non la potenza massima.
- Ignorare i requisiti di interpretabilità come vincolo di progettazione,
  trattandoli come un problema da risolvere dopo con strumenti di
  spiegabilità a posteriori invece che nella scelta iniziale del modello.
- Fare sempre fine-tuning di un modello fondazionale per abitudine, anche
  quando un prompt ben progettato basterebbe: la guida elenca
  esplicitamente "quando il tuning dovrebbe essere considerato" come
  competenza separata dal "come farlo".
- Confondere parallelismo dei dati e parallelismo del modello: il primo
  non risolve il problema di un modello che non entra su un singolo
  dispositivo, il secondo sì (vedi concepts.md).
