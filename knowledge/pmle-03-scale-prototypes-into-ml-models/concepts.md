# Concepts: pmle-03-scale-prototypes-into-ml-models

Decisione research: contenuto `VERIFIED` contro il testo verbatim della
exam guide ufficiale (vedi evidence.yaml). Un solo concetto generale
(data vs model parallelism) è spiegato con conoscenza ML generale, non
da documentazione di prodotto, ed è segnalato come tale.

## Concetti coperti

1. Il Dominio 3 ("Scaling prototypes into ML models", **~21% del peso, il
   dominio più grande dei sei**) copre il passaggio dal prototipo (Dominio
   2) a un modello addestrato in modo strutturato e ripetibile.
2. Sottosezione 3.1 — **scegliere l'approccio dato il compito**:
   scegliere il tipo di modello (es. ARIMA per serie storiche, DNN per
   pattern complessi, LLM per compiti generativi/linguistici) in base al
   problema; scegliere il prodotto giusto (Agent Platform AutoML,
   BigQuery ML, Agent Platform Pipelines — lo stesso ventaglio di
   strumenti del Dominio 1, qui applicato a un contesto di scala
   maggiore); scegliere la strategia di deployment; scegliere tecniche di
   modellazione compatibili con i requisiti di interpretabilità (un
   modello più semplice ma spiegabile può essere preferibile a uno più
   accurato ma opaco, a seconda del contesto).
3. Sottosezione 3.2 — **addestrare i modelli**: organizzare i dati di
   training (tabellari, testo, audio, immagini, video) su Cloud Storage o
   BigQuery; ingerire dati strutturati e non strutturati da fonti diverse
   nelle pipeline di training; addestrare con SDK diversi a seconda del
   caso (Agent Platform custom training per codice proprio, Kubeflow su
   GKE per orchestrazione containerizzata, Agent Platform AutoML per
   basso codice, Tabular Workflows per dati tabellari strutturati);
   risolvere errori di training; fare hyperparameter tuning; fare
   fine-tuning di modelli fondazionali da Agent Platform e Model Garden,
   **e capire quando il fine-tuning è la scelta giusta** (non sempre lo
   è: a volte un prompt ben progettato o un modello più piccolo bastano).
4. Sottosezione 3.3 — **scegliere l'hardware giusto**: valutare le
   opzioni di calcolo/acceleratore (CPU, GPU, TPU) in base al tipo di
   carico; capire le opzioni di training distribuito su GPU/TPU con
   strategie di **parallelismo dei dati** (ogni dispositivo ha una copia
   completa del modello e processa una porzione diversa del batch) e di
   **parallelismo del modello** (il modello stesso è diviso tra più
   dispositivi, quando non entra su uno solo).

## Il filo conduttore del dominio

Le tre sottosezioni rispondono in sequenza a: *che tipo di modello e
quale prodotto?* (3.1), *come lo addestro in modo ripetibile su dati
reali?* (3.2), *con quale hardware, e come lo scalo se non basta una
macchina sola?* (3.3). È il dominio più esplicitamente tecnico dei sei:
qui l'esame valuta scelte di progettazione, non solo conoscenza di
prodotto.

## Collegamento al resto del corso

Le Lezioni 6-13 del corso principale (NumPy, tensori, gradienti, loss,
prima rete Keras, training loop, overfitting, valutazione) sono
esattamente il "come" dietro la sottosezione 3.2: qui si impara a
costruire e addestrare un modello a mano, capendo cosa fa un ottimizzatore
e perché un modello overfitta; il Dominio 3 valuta la competenza
complementare, ovvero **quale strumento e quale scala** usare per lo
stesso problema in un contesto aziendale reale (un dataset che non entra
in RAM, un training che deve girare su più GPU, un modello che va
scelto tra dieci alternative diverse).

## Limiti

Questa lezione non tratta i dettagli implementativi di Kubeflow su GKE,
Tabular Workflows, o le API esatte di training distribuito: la exam guide
elenca queste come **strumenti da saper scegliere**, non fornisce
sintassi. Il concetto di parallelismo dati/modello è spiegato con
conoscenza ML generale (non specifica di Google Cloud), segnalato come
`needs_reverification` per eventuali dettagli implementativi specifici di
prodotto (vedi evidence.yaml).
