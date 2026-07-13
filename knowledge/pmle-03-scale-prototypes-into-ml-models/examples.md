# Examples: pmle-03-scale-prototypes-into-ml-models

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). Gli scenari sotto sono di
ragionamento, non codice testato.

## Scenario 1: interpretabilità come vincolo, non solo accuratezza

Una banca deve motivare per legge ogni rifiuto di prestito con una
ragione comprensibile. Un modello più accurato ma opaco (es. un
ensemble complesso) potrebbe non essere la scelta giusta secondo la
sottosezione 3.1: i requisiti di interpretabilità sono un vincolo di
progettazione esplicito, non un dettaglio da sistemare dopo con tecniche
di spiegabilità a posteriori.

## Scenario 2: quando il fine-tuning non è la risposta giusta

Un team vuole che un modello fondazionale risponda in un tono aziendale
specifico su un compito che il modello già sa fare bene in generale. La
sottosezione 3.2 elenca esplicitamente "quando il tuning dovrebbe essere
considerato" come competenza a sé: spesso un prompt ben progettato basta,
e il fine-tuning (più costoso, più lento da iterare) va scelto solo
quando il comportamento desiderato non è raggiungibile in altro modo.

## Scenario 3: un modello che non entra su una singola GPU

Un modello linguistico di grandi dimensioni non entra nella memoria di
un singolo acceleratore. La sottosezione 3.3 distingue due strategie: il
parallelismo dei dati (utile quando il modello entra su un dispositivo
ma il dataset o il batch è grande) non risolve questo problema; serve
parallelismo del modello, che divide il modello stesso tra più
dispositivi.
