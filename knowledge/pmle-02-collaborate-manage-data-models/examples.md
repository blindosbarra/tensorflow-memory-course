# Examples: pmle-02-collaborate-manage-data-models

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). Gli scenari sotto sono di
ragionamento, non codice testato.

## Scenario 1: scegliere lo strumento di preprocessing giusto

Un team ha 2 TB di log testuali da ripulire e trasformare in feature
prima del training, e i dati non stanno in memoria su una singola
macchina. La scelta secondo la sottosezione 2.1 è un servizio distribuito
(Dataflow o Apache Spark), non un framework Python in-memoria: la guida
lega esplicitamente la scelta dello strumento a scala e complessità dei
dati, non a preferenza personale.

## Scenario 2: prototipare prima di scalare

Un data scientist vuole verificare in mezza giornata se un modello
open-source da Model Garden ha una precisione ragionevole sul problema,
prima di investire settimane in una pipeline di training completa. La
sottosezione 2.2 descrive esattamente questo passo: prototipare in un
notebook condiviso (Workbench o Colab Enterprise) con un modello già
disponibile, prima di passare a un training strutturato.

## Scenario 3: confrontare due esperimenti fatti da persone diverse

Due membri del team hanno provato due configurazioni di iperparametri
diverse, in momenti diversi, senza parlarsi. Senza un sistema di tracking
(Experiments, ML Metadata), non si può dire con certezza quale modello
ha usato quali dati e quali parametri. La sottosezione 2.3 tratta proprio
questo: tracciare e confrontare artefatti, versioni e lineage non è un
dettaglio opzionale, è la condizione per poter confrontare due esperimenti
in modo affidabile.
