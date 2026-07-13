# Examples: pmle-04-serve-and-scale-models

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). Gli scenari sotto sono di
ragionamento, non codice testato.

## Scenario 1: batch vs online inference

Un'azienda deve classificare un milione di documenti archiviati una volta
al mese (non serve una risposta immediata) e, separatamente, deve
classificare un documento appena caricato da un utente in tempo reale
(serve una risposta in millisecondi). La sottosezione 4.1 distingue
esplicitamente inferenza batch (adatta al primo caso, più economica per
grandi volumi non urgenti) da inferenza online (adatta al secondo,
ottimizzata per bassa latenza su singole richieste).

## Scenario 2: rilasciare una nuova versione senza rischiare tutto il traffico

Un team ha addestrato una nuova versione di un modello di raccomandazione
e vuole verificarla su traffico reale senza sostituire subito la versione
in produzione. Un canary deployment (una piccola percentuale di traffico
alla nuova versione) limita il danno potenziale se la nuova versione ha
un problema, mentre un A/B testing più esteso permette di confrontare
statisticamente le due versioni prima di decidere quale tenere.

## Scenario 3: training-serving skew nel preprocessing

Un modello è stato addestrato con feature calcolate da uno script batch,
ma in produzione le stesse feature vengono ricalcolate da un servizio
online con una logica leggermente diversa (es. un arrotondamento
diverso). Il modello riceve in produzione input sistematicamente diversi
da quelli visti in training. Usare lo stesso Feature Store sia in
training sia in serving (sottosezione 4.2) è pensato esattamente per
evitare questo tipo di incoerenza.
