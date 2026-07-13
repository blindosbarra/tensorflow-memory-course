---
id: pmle-03-scale-prototypes-into-ml-models
title: "Certificazione PMLE - Dominio 3: scalare i prototipi in modelli ML"
module: gcp-ml-certification
status: writing
estimated_minutes: 30
prerequisites: [pmle-02-collaborate-manage-data-models]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# Certificazione PMLE — Dominio 3: scalare i prototipi in modelli ML

!!! note "Stato: contenuto verificato su fonte primaria"
    Contenuto verificato parola per parola contro la exam guide ufficiale
    Google Cloud, fornita direttamente dallo studente. Un concetto (data
    vs model parallelism) è spiegato con conoscenza ML generale, non da
    documentazione di prodotto Google Cloud — segnalato dove compare.

## Cosa copre questo dominio

Il Dominio 3 ("Scaling prototypes into ML models", **~21% dell'esame — il
dominio più grande dei sei**) copre il passaggio dal prototipo (Dominio 2)
a un modello addestrato in modo strutturato e ripetibile. È il dominio
più esplicitamente tecnico: qui l'esame valuta scelte di progettazione,
non solo conoscenza di prodotto.

## Teoria essenziale

### 3.1 — Scegliere l'approccio dato il compito

Quattro considerazioni: scegliere il **tipo di modello** (es. ARIMA per
serie storiche, DNN per pattern complessi, LLM per compiti generativi) in
base al problema; scegliere il **prodotto** giusto (Agent Platform
AutoML, BigQuery ML, Agent Platform Pipelines — lo stesso ventaglio di
strumenti del Dominio 1, qui applicato a un contesto di scala maggiore);
scegliere la **strategia di deployment**; scegliere tecniche di
modellazione compatibili con i **requisiti di interpretabilità**.

Il punto sull'interpretabilità è spesso sottovalutato: un modello più
accurato ma opaco può non essere la scelta giusta quando servono
spiegazioni comprensibili (es. per obblighi normativi). L'esame tratta
l'interpretabilità come un vincolo di progettazione da subito, non un
problema da risolvere dopo con strumenti di spiegabilità a posteriori.

### 3.2 — Addestrare i modelli

Sei considerazioni: organizzare i dati di training (tabellari, testo,
audio, immagini, video) su Cloud Storage o BigQuery; ingerire dati
strutturati e non strutturati da fonti diverse nelle pipeline di
training; addestrare con SDK diversi a seconda del caso (Agent Platform
custom training per codice proprio, Kubeflow su GKE per orchestrazione
containerizzata, Agent Platform AutoML per basso codice, Tabular
Workflows per dati tabellari strutturati); risolvere errori di training;
fare hyperparameter tuning; fare fine-tuning di modelli fondazionali da
Agent Platform e Model Garden, **e capire quando il fine-tuning è la
scelta giusta**.

Quest'ultimo punto è esplicito nella guida: non sempre il fine-tuning è
la risposta. A volte un prompt ben progettato o un modello più piccolo
bastano, ed è più economico e veloce da iterare.

### 3.3 — Scegliere l'hardware giusto

Due considerazioni: valutare le opzioni di calcolo/acceleratore (CPU,
GPU, TPU) in base al tipo di carico; capire le opzioni di training
distribuito su GPU/TPU con strategie di **parallelismo dei dati** e di
**parallelismo del modello**.

La distinzione tra le due strategie (concetto generale di ML, non
specifico di un prodotto Google Cloud): nel parallelismo dei dati, ogni
dispositivo ha una copia completa del modello e processa una porzione
diversa del batch — utile quando il modello entra su un dispositivo ma
il dataset o il batch è grande. Nel parallelismo del modello, il modello
stesso è diviso tra più dispositivi — necessario quando il modello non
entra nella memoria di un singolo acceleratore.

### Collegamento al corso principale

Le Lezioni 6-13 del corso principale (NumPy, tensori, gradienti, loss,
prima rete Keras, training loop, overfitting, valutazione) sono
esattamente il "come" dietro la sottosezione 3.2: lì si impara a
costruire e addestrare un modello a mano; il Dominio 3 valuta la
competenza complementare — quale strumento e quale scala usare per lo
stesso problema in un contesto aziendale reale (un dataset che non entra
in RAM, un training che deve girare su più GPU).

## Scenari di ragionamento

(Dettagliati in `knowledge/pmle-03-scale-prototypes-into-ml-models/examples.md`.)

- Una banca deve motivare per legge ogni rifiuto di prestito → un modello
  più accurato ma opaco potrebbe non essere la scelta giusta:
  l'interpretabilità è un vincolo di progettazione esplicito.
- Un team vuole che un modello fondazionale risponda in un tono aziendale
  specifico su un compito che già sa fare → spesso un prompt ben
  progettato basta, il fine-tuning va scelto solo quando necessario.
- Un modello linguistico non entra sulla memoria di una singola GPU → il
  parallelismo dei dati non risolve il problema, serve parallelismo del
  modello.

## Errori comuni

- Scegliere il tipo di modello più potente disponibile invece di quello
  adatto al compito, ignorando costo, complessità, latenza e scalabilità.
- Trattare l'interpretabilità come un problema da risolvere dopo con
  strumenti di spiegabilità, invece che come vincolo nella scelta
  iniziale del modello.
- Fare sempre fine-tuning per abitudine, anche quando un prompt ben
  progettato basterebbe.
- Confondere parallelismo dei dati e parallelismo del modello: solo il
  secondo risolve il problema di un modello che non entra su un singolo
  dispositivo.

## Quiz

1. Una banca deve motivare legalmente ogni rifiuto di prestito con una
   spiegazione comprensibile. Quale considerazione della sottosezione 3.1
   entra in gioco, e come influenza la scelta del modello?
2. Perché la guida elenca esplicitamente "quando il tuning dovrebbe
   essere considerato" come competenza a sé, separata da "come fare il
   tuning"?
3. Un modello linguistico di grandi dimensioni non entra nella memoria di
   una singola GPU. Quale strategia di parallelismo risolve questo
   problema, e perché l'altra non basta?

<details>
<summary><b>Apri le risposte</b></summary>

1. L'interpretabilità, citata esplicitamente come "modeling techniques
   given interpretability requirements": un modello più accurato ma
   opaco può non essere la scelta giusta se serve una spiegazione
   comprensibile, quindi l'interpretabilità va considerata nella scelta
   del modello, non aggiunta dopo.
2. Perché il fine-tuning ha un costo (tempo, calcolo, iterazione più
   lenta) che non sempre è giustificato: a volte un prompt ben
   progettato o un modello più piccolo ottengono lo stesso risultato a
   costo minore. Saperlo riconoscere è una competenza distinta dal saper
   eseguire il fine-tuning.
3. Il parallelismo del modello, perché divide il modello stesso tra più
   dispositivi. Il parallelismo dei dati non basta perché ogni
   dispositivo dovrebbe comunque contenere una copia intera del modello,
   che non entra in memoria.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
