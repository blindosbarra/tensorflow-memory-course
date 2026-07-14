# Pitfalls: pmle-07-architetture-end-to-end

- Copiare la scelta di modello/strumento di un problema su un altro solo
  perché "ha funzionato l'ultima volta": ogni architettura di questa
  lezione ha vincoli diversi (interpretabilità, driver esterni, dati
  sbilanciati) che cambiano la scelta giusta.
- Diagnosticare overfitting o underfitting guardando una sola metrica in
  un solo momento, invece di confrontare esplicitamente training e
  validation e osservare come il divario evolve nel tempo/nelle
  iterazioni.
- Guardare solo l'accuratezza aggregata su un problema multi-classe o
  con classi sbilanciate: nasconde sistematicamente le classi minoritarie,
  spesso quelle che contano di più per il business.
- Reagire a un calo di performance in produzione riaddestrando subito,
  senza prima distinguere un drift atteso/stagionale da un vero
  cambiamento nella distribuzione dei dati o nella relazione
  input-target.
- Trattare "aggiungere AI generativa" come un dettaglio implementativo
  del solito ciclo MLOps: cambiano la valutazione (nessuna singola
  risposta corretta), cosa si versiona (anche prompt/contesto RAG) e
  cosa si monitora (rischi specifici come prompt injection), non solo il
  tipo di modello usato.
- Scegliere inferenza online per un problema che è strutturalmente
  batch (nessuno aspetta una risposta immediata), pagando costo e
  complessità di un endpoint in tempo reale senza bisogno.
- In un sistema RAG, aggiornare i documenti sorgente senza
  re-indicizzarli per il retrieval: il sintomo (risposte scadute) sembra
  un problema del modello ma è un problema di freschezza dei dati
  recuperati — l'equivalente RAG del training-serving skew.
