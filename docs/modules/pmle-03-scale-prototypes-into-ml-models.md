---
id: pmle-03-scale-prototypes-into-ml-models
title: "Certificazione PMLE - Dominio 3: scalare i prototipi in modelli ML"
module: gcp-ml-certification
status: writing
estimated_minutes: 45
prerequisites: [pmle-02-collaborate-manage-data-models]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# Certificazione PMLE — Dominio 3: scalare i prototipi in modelli ML

!!! note "Stato: contenuto verificato su fonte primaria"
    Contenuto verificato parola per parola contro la exam guide ufficiale
    Google Cloud, fornita direttamente dallo studente. Alcuni concetti —
    data vs model parallelism, il dettaglio di cosa sono CNN/RNN/
    Transformer dietro il termine "DNN" della guida, e i dettagli
    implementativi di come si sottomette davvero un training job/
    hyperparameter tuning su Google Cloud — sono spiegati con conoscenza
    ML/MLOps generale, non da documentazione di prodotto Google Cloud,
    segnalati dove compaiono.

## Cosa copre questo dominio

Il Dominio 3 ("Scaling prototypes into ML models", **~21% dell'esame — il
dominio più grande dei sei**) copre il passaggio dal prototipo (Dominio 2)
a un modello addestrato in modo strutturato e ripetibile. È il dominio
più esplicitamente tecnico: qui l'esame valuta scelte di progettazione,
non solo conoscenza di prodotto.

## Teoria essenziale

Riprendiamo ancora "Nordica Commerce": il modello di rinnovo contratti B2B
del Dominio 2 ha superato il prototipo in notebook ed è pronto per essere
addestrato in modo strutturato. Le tre sottosezioni del Dominio 3 sono le
decisioni che Nordica deve prendere per portarlo lì.

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

**Nordica, concretamente.** Il modello di rinnovo contratti non serve
solo a prevedere: quando un cliente business scopre che le sue condizioni
non sono state rinnovate automaticamente, l'ufficio commerciale deve
potergli spiegare *perché* — è una relazione contrattuale, non una
raccomandazione anonima su un sito consumer. Un modello a scatola nera
(es. una rete profonda complessa) potrebbe essere leggermente più
accurato di un `BOOSTED_TREE_CLASSIFIER` o di una `LOGISTIC_REG`, ma se
nessuno riesce a spiegare al cliente quali fattori hanno pesato nella
decisione, quella maggiore accuratezza non vale il costo: qui
l'interpretabilità (in questo caso, dei modelli visti nel Dominio 1,
`LOGISTIC_REG` e gli alberi restano più facili da ispezionare di una
`DNN_CLASSIFIER`) è un vincolo che entra nella scelta del modello fin
dall'inizio, non un report da produrre a posteriori.

!!! info "DNN per pattern complessi, in dettaglio: CNN, RNN, e perché i modelli fondazionali oggi usano Transformer"
    La guida dice solo "DNN per pattern complessi", senza specificare
    che "DNN" copre famiglie di architetture molto diverse tra loro a
    seconda del tipo di dato. Tre di queste tornano più volte in questo
    modulo (foto difettose e fiori nel Dominio 1, riassunto ticket nel
    Dominio 1, previsione domanda/pioggia nei Domini 1 e nella lezione di
    sintesi) senza mai essere spiegate.

    **CNN (rete neurale convoluzionale) — per immagini.** Un `DNN`
    "denso" tratta ogni pixel come un input indipendente: per
    un'immagine 100×100 in scala di grigi (10.000 pixel) collegata a
    soli 100 neuroni del livello successivo servirebbero già 10.000 ×
    100 = **1.000.000 di pesi**, e la rete non saprebbe che due pixel
    vicini sono correlati. Una **CNN** usa invece piccoli filtri (es. 3×3
    pixel) che scorrono su tutta l'immagine, riusando **sempre gli
    stessi pesi** in ogni posizione: 32 filtri 3×3 costano solo 3×3×32 =
    **288 pesi**, indipendentemente da quanto è grande l'immagine — un
    filtro che ha imparato a riconoscere un bordo lo riconosce ovunque
    compaia nella foto, non solo in una posizione fissa.

    Un esempio numerico di cosa calcola davvero un filtro. Un filtro
    tipo "rileva contrasto locale":

    ```
    Filtro:        Patch di immagine (valori pixel):
     0  -1   0       10  10  10
    -1   4  -1       10  50  10
     0  -1   0       10  10  10
    ```

    Il filtro scorre sulla patch e calcola la somma dei prodotti
    elemento per elemento: `0×10 + (-1)×10 + 0×10 + (-1)×10 + 4×50 +
    (-1)×10 + 0×10 + (-1)×10 + 0×10 = -40 + 200 = 160`. Un valore alto
    (160) segnala che il pixel centrale (50) contrasta fortemente con i
    vicini (tutti 10) — il filtro ha "acceso" un segnale forte in
    corrispondenza di un bordo o di un punto isolato. Dopo alcuni strati
    convoluzionali, un livello di **pooling** (es. max pooling: da un
    blocco 2×2 di valori `[[9,2],[4,7]]` tiene solo il massimo, `9`)
    riduce la dimensione mantenendo il segnale più forte, prima di
    passare tutto a strati densi finali per la decisione di
    classificazione. Questo è ciò che AutoML cerca automaticamente
    (Dominio 1) quando lavora su immagini — spesso partendo da un
    backbone convoluzionale già pre-addestrato invece che inventare
    l'architettura da zero.

    **RNN (rete neurale ricorrente) — per sequenze.** Una RNN elabora una
    sequenza (una serie storica, una frase) un elemento alla volta,
    mantenendo uno **stato nascosto** che riassume ciò che ha visto
    finora e si aggiorna a ogni passo: `stato_t = f(pesi_x · input_t +
    pesi_h · stato_(t-1))`. Gli stessi pesi sono riusati a ogni passo
    temporale, il che permette a una RNN di gestire sequenze di
    lunghezza qualunque con un numero fisso di parametri. Il problema
    pratico: durante l'addestramento, il gradiente della loss deve
    propagarsi all'indietro attraverso *tutti* i passi temporali
    (backpropagation through time), e moltiplicandosi ripetutamente
    tende a **svanire** (diventare quasi zero, la rete smette di
    imparare dipendenze tra elementi lontani nella sequenza) o a
    **esplodere** (crescere senza controllo). Varianti come **LSTM** e
    **GRU** aggiungono meccanismi di "cancello" (gate) che permettono
    alla rete di decidere esplicitamente cosa tenere e cosa scartare
    dallo stato nascosto nel tempo, attenuando (non eliminando) questo
    problema.

    **Dove RNN è un'opzione reale in questo modulo, e dove non lo è
    più.** Per la previsione domanda/pioggia (Domini 1 e la lezione di
    sintesi), una RNN/LSTM è un'alternativa tecnicamente valida ad
    `ARIMA_PLUS` o a un `BOOSTED_TREE_REGRESSOR` con feature di lag — ma
    richiede più codice, più dati e più tuning, quindi il criterio del
    Dominio 1 (minimo sforzo che basta) la rende la scelta di **ultima
    istanza**, non la prima, a meno che il pattern temporale sia troppo
    complesso per feature di lag scritte a mano. Per il testo (riassunto
    ticket, Dominio 1 Problema 3), invece, le RNN sono in gran parte
    **superate**: i modelli fondazionali moderni come quelli di Gemini
    Enterprise Agent Platform Model Garden si basano sull'architettura
    **Transformer**, che elabora tutti gli elementi della sequenza **in
    parallelo** invece che uno alla volta, usando un meccanismo di
    attenzione per pesare direttamente le relazioni tra elementi
    lontani nella sequenza senza passare per uno stato nascosto
    propagato passo-passo — più veloce da addestrare su hardware
    parallelo e meno soggetto al problema del gradiente che svanisce. Il
    corso principale tratta l'attenzione e i Transformer in dettaglio,
    con codice, nel modulo "Transformer e modello open" più avanti nel
    percorso.

    **Stato: needs_reverification** — meccaniche generali di CNN
    (convoluzione, pooling, condivisione dei pesi), RNN (stato nascosto,
    vanishing/exploding gradient, LSTM/GRU) e Transformer/attenzione sono
    conoscenza ML generale, non specifica di un prodotto Google Cloud,
    non riverificate su documentazione live in questa sessione. L'esempio
    numerico del filtro convoluzionale è un calcolo aritmetico verificato
    su valori costruiti a scopo didattico, non un output di un modello
    reale.

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

**Nordica, concretamente.** Torniamo al modello di riassunto ticket del
Dominio 1: il primo tentativo con solo prompting produce riassunti
generici ma corretti. Se il team scopre (tramite AutoSxS, Dominio 2) che
il formato non è ancora abbastanza costante per l'operatore umano,
la sequenza da seguire è quella del Dominio 1: prima un tuning efficiente
in parametri (es. LoRA) sul formato desiderato, e solo se anche questo
non basta si considera il fine-tuning completo. La sottosezione 3.2
tratta il "come" tecnico di quell'ultima opzione (SDK, hyperparameter
tuning, debug di un training che fallisce) — ma la decisione *se* farlo
resta quella vista nel Dominio 1.

!!! info "Come si sottomette davvero un training job custom, concretamente"
    La guida nomina "Agent Platform custom training" come opzione SDK,
    senza spiegare cosa significhi in pratica avviarne uno.

    **Il job.** Il codice di training (uno script Python, o un container
    Docker che lo incapsula) viene sottomesso specificando una
    **worker pool spec**: quale immagine container eseguire, che
    `machine-type` usare (es. `n1-standard-8`), quanti e quali
    acceleratori (`accelerator-type=NVIDIA_TESLA_T4`,
    `accelerator-count=2`), e quante repliche. Per training distribuito
    (Dominio 3.3) si definiscono più worker pool: un pool "chief/master"
    (una replica che coordina) e uno o più pool "worker" aggiuntivi — la
    stessa distinzione tra parallelismo dati/modello vista sopra
    determina quanti worker servono e come sono configurati.

    **Hyperparameter tuning, come funziona davvero.** Non è una ricerca
    a griglia esaustiva: si definisce uno spazio di ricerca (es.
    `learning_rate`: continuo tra 1e-5 e 1e-1 su scala logaritmica,
    `batch_size`: discreto tra 16/32/64) e una metrica obiettivo da
    massimizzare o minimizzare (es. il recall visto nel Dominio 1); il
    servizio esegue più prove (trial) in parallelo fino a un budget
    massimo di prove, usando i risultati delle prove già fatte per
    scegliere quali combinazioni provare dopo (ottimizzazione
    bayesiana) — concettualmente la stessa logica di ricerca guidata
    vista per AutoML nel Dominio 1, qui applicata agli iperparametri di
    un'architettura fissata invece che all'architettura stessa.

    **Risolvere errori di training, in pratica.** Due problemi ricorrenti
    e le loro cause tipiche, distinti da un problema di
    overfitting/underfitting (che è un problema del *modello*, non del
    *job*): un job interrotto a metà su una VM **preemptible/spot**
    (più economica ma può essere ripresa dal provider in qualsiasi
    momento) perde tutto il progresso se non si salvano periodicamente
    checkpoint (pesi + stato dell'optimizer) su Cloud Storage, da cui il
    job può ripartire invece di ricominciare da zero; un job che fallisce
    con un errore di memoria esaurita sull'acceleratore va quasi sempre
    risolto riducendo il `batch_size` prima di sospettare l'architettura
    del modello. Le quote regionali di GPU/TPU disponibili sono un altro
    blocco pratico comune, non un problema di machine learning in sé.

    **Stato: needs_reverification** — struttura generale di un job di
    training gestito (worker pool, hyperparameter tuning bayesiano,
    checkpointing su VM preemptibili) è conoscenza ML/MLOps generale;
    nomi esatti di flag, parametri e opzioni non riverificati su
    documentazione live in questa sessione (bloccato, vedi
    `course/research_gaps.md`).

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

**Nordica, concretamente.** Se in futuro Nordica decidesse di addestrare
da zero (non solo fare fine-tuning) un modello linguistico proprio sui
tre anni di ticket accumulati — uno scenario più estremo di quelli visti
finora, ma comunque nel perimetro dell'esame — due problemi diversi
possono presentarsi. Se il *dataset* è enorme ma il modello entra sulla
memoria di una singola GPU, la soluzione è il parallelismo dei dati: ogni
GPU tiene una copia intera del modello e processa un pezzo diverso del
batch, poi i gradienti calcolati vengono mediati tra le GPU. Se invece è
il *modello stesso* a non entrare nella memoria di una singola GPU (comune
per i modelli linguistici più grandi), il parallelismo dei dati non basta
— ogni dispositivo dovrebbe comunque contenere una copia intera del
modello — e serve il parallelismo del modello, che divide gli strati o i
parametri del modello stesso su più dispositivi.

### Collegamento al corso principale

Le Lezioni 6-13 del corso principale (NumPy, tensori, gradienti, loss,
prima rete Keras, training loop, overfitting, valutazione) sono
esattamente il "come" dietro la sottosezione 3.2: lì si impara a
costruire e addestrare un modello a mano; il Dominio 3 valuta la
competenza complementare — quale strumento e quale scala usare per lo
stesso problema in un contesto aziendale reale (un dataset che non entra
in RAM, un training che deve girare su più GPU).

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
- Usare una RNN per un problema di testo oggi, per abitudine o perché
  "sono reti per sequenze": i modelli fondazionali moderni per il testo
  usano Transformer, non RNN — le RNN restano un'opzione valida
  soprattutto per serie storiche, non la scelta di default per il testo.
- Applicare una rete densa "semplice" a immagini invece di una CNN,
  ignorando che il numero di pesi esplode senza sfruttare la
  correlazione spaziale tra pixel vicini.
- Usare VM preemptible/spot per un training lungo senza salvare
  checkpoint periodici: un'interruzione a metà fa perdere tutto il
  progresso invece di poter riprendere da dove si era arrivati.
- Sospettare subito l'architettura del modello quando un training fallisce
  per memoria esaurita sull'acceleratore: la prima cosa da controllare è
  il `batch_size`, un problema del job, non del modello.

## Quiz

1. Nordica deve poter spiegare a un cliente business perché il suo
   contratto non è stato rinnovato automaticamente. Quale considerazione
   della sottosezione 3.1 entra in gioco, e come influenza la scelta del
   modello?
2. Perché la guida elenca esplicitamente "quando il tuning dovrebbe
   essere considerato" come competenza a sé, separata da "come fare il
   tuning"?
3. Un modello linguistico di grandi dimensioni non entra nella memoria di
   una singola GPU. Quale strategia di parallelismo risolve questo
   problema, e perché l'altra non basta?
4. Perché una CNN ha bisogno di molti meno pesi di una rete densa per
   elaborare la stessa immagine, e cosa perderebbe una rete densa che
   una CNN invece cattura?
5. Perché una RNN semplice fatica a imparare dipendenze tra elementi
   lontani in una sequenza lunga, e quali due varianti attenuano il
   problema?
6. Un training job che dura 10 ore su una VM preemptible/spot viene
   interrotto dopo 7 ore. Cosa determina se Nordica deve ricominciare da
   zero o può ripartire da dove si era fermato?

<details>
<summary><b>Apri le risposte</b></summary>

1. L'interpretabilità, citata esplicitamente come "modeling techniques
   given interpretability requirements": un modello più accurato ma
   opaco (es. una DNN complessa) può non essere la scelta giusta se serve
   spiegare al cliente quali fattori hanno pesato sulla decisione, quindi
   l'interpretabilità va considerata nella scelta del modello (es.
   preferire `LOGISTIC_REG` o un albero a una rete profonda), non
   aggiunta dopo con strumenti di spiegabilità a posteriori.
2. Perché il fine-tuning ha un costo (tempo, calcolo, iterazione più
   lenta) che non sempre è giustificato: a volte un prompt ben
   progettato o un modello più piccolo ottengono lo stesso risultato a
   costo minore. Saperlo riconoscere è una competenza distinta dal saper
   eseguire il fine-tuning.
3. Il parallelismo del modello, perché divide il modello stesso tra più
   dispositivi. Il parallelismo dei dati non basta perché ogni
   dispositivo dovrebbe comunque contenere una copia intera del modello,
   che non entra in memoria.
4. Perché una CNN riusa lo stesso piccolo filtro (es. 3×3 pixel) in ogni
   posizione dell'immagine invece di collegare ogni pixel a un peso
   dedicato: pochi pesi (es. 288 per 32 filtri 3×3) bastano
   indipendentemente da quanto è grande l'immagine. Una rete densa
   tratterebbe ogni pixel come indipendente, perdendo l'informazione che
   pixel vicini sono correlati (un bordo o una texture) e richiedendo
   milioni di pesi anche per immagini piccole.
5. Perché il gradiente della loss deve propagarsi all'indietro
   attraverso ogni passo temporale (backpropagation through time), e
   moltiplicandosi ripetutamente tende a svanire (quasi zero) o esplodere
   — rendendo difficile imparare relazioni tra elementi molto distanti
   nella sequenza. LSTM e GRU attenuano il problema con meccanismi di
   gate che permettono alla rete di decidere esplicitamente cosa
   mantenere e cosa scartare dallo stato nascosto nel tempo.
6. Se il job salvava checkpoint periodici (pesi + stato dell'optimizer)
   su Cloud Storage, può ripartire dall'ultimo checkpoint salvato invece
   di ricominciare da zero. Senza checkpoint, tutto il progresso delle 7
   ore è perso — il rischio esplicito da accettare quando si sceglie una
   VM più economica ma interrompibile.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
