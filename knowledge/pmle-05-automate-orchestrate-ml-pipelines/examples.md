# Examples: pmle-05-automate-orchestrate-ml-pipelines

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). Gli scenari sotto sono di
ragionamento, non codice testato.

## Scenario 1: validare prima di procedere, non dopo

Una pipeline automatica riceve ogni notte nuovi dati e riaddestra un
modello. Un giorno una fonte a monte invia dati corrotti (molte righe
vuote). Senza un passo di validazione dei dati (sottosezione 5.1) prima
del training, la pipeline addestrerebbe comunque un modello — su dati
rotti — e lo distribuirebbe automaticamente, propagando l'errore invece
di fermarlo.

## Scenario 2: quando riaddestrare, non solo come

Un modello di raccomandazione perde progressivamente accuratezza man mano
che le preferenze degli utenti cambiano nel tempo. Riaddestrare ogni
notte a prescindere è costoso e spesso inutile; non riaddestrare mai
lascia il modello obsoleto. La sottosezione 5.2 tratta esplicitamente la
scelta di una policy di retraining (es. basata su una soglia di calo
delle metriche di produzione, non solo su un intervallo fisso) come
competenza distinta dal meccanismo di retraining stesso.

## Scenario 3: preprocessing incoerente tra pipeline di training e serving

Una pipeline di training normalizza una feature numerica sottraendo la
media calcolata sul training set; il servizio di serving in produzione,
scritto separatamente, usa una media diversa calcolata su un altro
campione. Il modello riceve input sistematicamente diversi da quelli su
cui è stato addestrato. La sottosezione 5.1 tratta esplicitamente la
coerenza del preprocessing tra training e serving come un requisito della
pipeline stessa, non un dettaglio da controllare a mano dopo.
