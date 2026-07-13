# Pitfalls: pmle-04-serve-and-scale-models

- Usare inferenza online per un carico che è in realtà batch (es.
  processare un milione di righe una volta al mese chiamando un endpoint
  riga per riga): più costoso e più lento di un job batch dedicato.
- Rilasciare una nuova versione di modello a tutto il traffico in un
  colpo solo, senza una strategia di rollout progressiva (A/B testing o
  canary): un problema nella nuova versione impatta subito tutti gli
  utenti.
- Ricalcolare le feature in modo diverso tra training e serving (anche
  solo un dettaglio come un arrotondamento) invece di usare la stessa
  fonte (Feature Store) in entrambe le fasi: causa training-serving skew,
  un problema difficile da diagnosticare perché il modello sembra
  corretto ma performa peggio in produzione.
- Scegliere l'hardware di serving in base a cosa è stato usato in
  training, invece che in base al throughput e alla latenza richiesti in
  produzione: sono vincoli diversi (la sottosezione 4.2 li tratta
  separatamente).
