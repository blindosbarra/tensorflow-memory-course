# Pitfalls: pmle-02-collaborate-manage-data-models

- Scegliere uno strumento di preprocessing per abitudine (es. sempre
  pandas) invece che in base a scala e complessità dei dati: la guida
  valuta esplicitamente questa scelta come una competenza a sé, non un
  dettaglio implementativo.
- Prototipare in notebook senza applicare pratiche di collaborazione e
  sicurezza (es. condividere credenziali nel codice, non isolare
  ambienti): la sottosezione 2.2 lo elenca come prima considerazione,
  prima ancora dei framework usati.
- Saltare il tracking degli esperimenti perché "si ricorda a mente" quale
  configurazione ha dato quale risultato: non scala oltre un singolo
  esperimento e non è riproducibile da un collega, il problema centrale
  che la sottosezione 2.3 indirizza.
- Ignorare la gestione delle informazioni sensibili (PII) durante
  l'esplorazione dei dati, trattandola come un passo successivo anziché
  parte della sottosezione 2.1 stessa.
