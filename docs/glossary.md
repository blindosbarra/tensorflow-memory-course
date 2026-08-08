# Glossario

## Adapter

Piccolo insieme di parametri addestrabili aggiunto a un modello pre-addestrato,
che permette di adattarlo senza modificare tutti i suoi pesi. Vedi
[Impacchettare e distribuire un adapter](modules/adapter-packaging.md).

## Backpropagation

Procedura che propaga il segnale di errore dalla loss verso i parametri della
rete applicando la regola della catena. Vedi
[Dentro `fit`](modules/model-fit-under-the-hood.md).

## Blocco Transformer

Struttura che combina self-attention, rete feed-forward, connessioni residue e
normalizzazione. Vedi [Il blocco Transformer](modules/transformer-block.md).

## Calibrazione

Coerenza tra una probabilità predetta e la frequenza osservata dell'evento: tra
le predizioni vicine a `0.8`, circa l'80% dovrebbe essere positivo. Vedi
[Valutazione e calibrazione](modules/evaluation-calibration.md).

## Clustering

Raggruppamento non supervisionato di esempi simili, senza etichette note in
partenza. Vedi [Clustering delle memorie](modules/clustering-memories.md).

## Contraddizione

Conflitto tra due memorie riferite alla stessa entità e allo stesso attributo,
ma con valori incompatibili. Vedi
[Contraddizione e aggiornamento](modules/contradiction-and-update.md).

## Coppie chosen/rejected

Coppia di risposte allo stesso prompt nella quale `chosen` è preferita a
`rejected`; è un'unità dati per il preference learning. Vedi
[Dati chosen/rejected](modules/chosen-rejected-data.md).

## Data leakage

Passaggio al training di informazioni che non sarebbero disponibili al momento
della predizione reale, con metriche troppo ottimistiche. Vedi
[Data leakage](modules/data-leakage.md).

## Decadimento temporale

Riduzione del contributo di una memoria al crescere del tempo trascorso, secondo
una funzione esplicita. Vedi
[Decadimento temporale](modules/time-recency-decay.md).

## DPO

`Direct Preference Optimization`: metodo che usa direttamente coppie di
preferenza per aumentare la probabilità della risposta scelta rispetto a quella
rifiutata, senza addestrare prima un reward model separato. Vedi
[Intuizione di DPO](modules/dpo-intuition.md).

## Drift

Cambiamento nel tempo dei dati, delle predizioni o delle prestazioni rispetto
alla distribuzione di riferimento. Vedi
[Monitoraggio del capstone](modules/capstone-monitoring.md).

## Dropout

Tecnica di regolarizzazione che durante il training azzera casualmente una
frazione delle attivazioni, riducendo la dipendenza da singoli neuroni. Vedi
[Regolarizzazione e dropout](modules/regularization-dropout.md).

## Duplicato

Record ripetuto che rappresenta la stessa osservazione e può alterare conteggi,
split e metriche. Vedi
[Duplicati, tipi e outlier](modules/duplicates-types-outliers.md).

## Embedding

Vettore denso appreso che rappresenta un elemento in modo che elementi utilmente
simili possano risultare vicini nello spazio vettoriale. Vedi
[Embedding layer](modules/embedding-layer.md).

## Episodic

Memoria di un evento specifico, legato a un contesto e spesso a un momento. Vedi
[Memorie episodiche, semantiche e di preferenza](modules/episodic-semantic-preference.md).

## Freezing

Esclusione temporanea di alcuni pesi dall'aggiornamento durante il training,
tipica del transfer learning. Vedi
[Transfer learning e freezing](modules/transfer-learning-freezing.md).

## Gradiente

Vettore delle derivate parziali della loss rispetto ai parametri; indica la
direzione di crescita più rapida della loss. Vedi
[Derivate, gradienti e chain rule](modules/derivatives-gradients-chain-rule.md).

## `GradientTape`

Meccanismo TensorFlow che registra le operazioni eseguite per calcolare poi i
gradienti tramite autodiff. Vedi
[Dentro `fit`](modules/model-fit-under-the-hood.md).

## Grafo delle memorie

Rappresentazione in cui entità o memorie sono nodi e le loro relazioni sono
archi. Vedi [Grafo delle memorie](modules/graph-memory-networkx.md).

## Imputazione

Sostituzione di un valore mancante con un valore calcolato o scelto secondo una
regola esplicita. Vedi
[Dati mancanti](modules/data-cleaning-01-missing-values.md).

## Learning rate

Iperparametro che controlla l'ampiezza dell'aggiornamento applicato ai parametri
a ogni passo di ottimizzazione. Vedi
[Derivate, gradienti e chain rule](modules/derivatives-gradients-chain-rule.md).

## LoRA

`Low-Rank Adaptation`: adattamento parameter-efficient che congela i pesi di
base e apprende aggiornamenti fattorizzati a rango ridotto. Vedi
[La matematica di LoRA](modules/lora-math.md).

## Loss function

Funzione scalare che misura l'errore del modello e fornisce l'obiettivo da
minimizzare durante il training. Vedi
[Probabilità e loss function](modules/probability-loss-functions.md).

## Memoria semantica

Memoria di un fatto o concetto che non dipende necessariamente da un singolo
episodio. Vedi
[Memorie episodiche, semantiche e di preferenza](modules/episodic-semantic-preference.md).

## Missing value

Valore assente in una tabella. In pandas può apparire con sentinelle diverse,
come `NaN`, `NaT` o `NA`. Vedi
[Dati mancanti](modules/data-cleaning-01-missing-values.md).

## Monitoring

Osservazione continuativa di qualità dei dati, drift, prestazioni e salute del
sistema per rilevare cambiamenti dopo il rilascio. Vedi
[Monitoraggio del capstone](modules/capstone-monitoring.md).

## MRR

`Mean Reciprocal Rank`: media del reciproco della posizione del primo risultato
rilevante; premia i sistemi che lo collocano presto nella lista. Vedi
[Metriche di retrieval](modules/retrieval-metrics.md).

## Near-duplicate

Record quasi uguale a un altro, ma non identico byte per byte; può attraversare
gli split e produrre leakage. Vedi
[Duplicati, tipi e outlier](modules/duplicates-types-outliers.md).

## Optimizer

Algoritmo che usa i gradienti per aggiornare i parametri con l'obiettivo di
ridurre la loss. Vedi [Dentro `fit`](modules/model-fit-under-the-hood.md).

## Outlier

Osservazione molto distante dal comportamento tipico dei dati, da investigare
prima di decidere se correggerla, conservarla o escluderla. Vedi
[Duplicati, tipi e outlier](modules/duplicates-types-outliers.md).

## Overfitting

Condizione in cui il modello si adatta molto ai dati di training ma generalizza
peggio su dati non visti. Vedi
[Regolarizzazione e dropout](modules/regularization-dropout.md).

## PCA

Tecnica lineare di riduzione dimensionale che proietta i dati lungo direzioni di
varianza decrescente. Vedi [PCA e UMAP](modules/pca-umap.md).

## Pipeline

Sequenza ordinata e ripetibile di trasformazioni e controlli che porta dai dati
in ingresso a un risultato del sistema. Vedi
[Pipeline del capstone](modules/capstone-pipeline.md).

## Preference

Memoria che descrive un gusto, una scelta o una preferenza di una persona. Vedi
[Memorie episodiche, semantiche e di preferenza](modules/episodic-semantic-preference.md).

## Preference learning online

Aggiornamento del modello mentre arrivano nuovi dati o feedback, con rischi di
instabilità, manipolazione e degradazione difficili da controllare. Vedi
[Rischi dell'online learning](modules/online-learning-risks.md).

## Punteggio di importanza

Calcolo di un punteggio che combina segnali espliciti per ordinare o filtrare le
memorie in base alla loro utilità attesa. Vedi
[Importance scoring](modules/importance-scoring.md).

## QLoRA

Adattamento che combina un modello di base quantizzato con adapter LoRA
addestrabili, riducendo la memoria richiesta. Vedi
[Concetti di QLoRA](modules/qlora-concepts.md).

## Quantizzazione

Rappresentazione dei pesi con precisione numerica ridotta per diminuire memoria
e costo computazionale, accettando una possibile perdita di accuratezza. Vedi
[Concetti di QLoRA](modules/qlora-concepts.md).

## Rank

Dimensione interna della fattorizzazione LoRA: controlla la capacità
dell'aggiornamento e il numero di parametri addestrabili. Vedi
[La matematica di LoRA](modules/lora-math.md).

## Recall@K

Frazione degli elementi rilevanti recuperati tra i primi `K` risultati. Vedi
[Metriche di retrieval](modules/retrieval-metrics.md).

## Retrieval ibrido

Recupero che combina più segnali, per esempio similarità semantica, importanza,
recenza e relazioni nel grafo. Vedi
[Retrieval ibrido](modules/hybrid-retrieval.md).

## Reward function

Funzione che assegna un punteggio a un comportamento o a una risposta per
esprimere ciò che il sistema dovrebbe preferire. Vedi
[Reward function](modules/reward-functions.md).

## RLAIF

`Reinforcement Learning from AI Feedback`: famiglia di metodi in cui il segnale
di preferenza è prodotto da un sistema di AI invece che direttamente da persone.
Vedi [RLHF e RLAIF](modules/rlhf-rlaif-overview.md).

## RLHF

`Reinforcement Learning from Human Feedback`: adattamento di una politica con
un segnale derivato da preferenze umane. Vedi
[RLHF e RLAIF](modules/rlhf-rlaif-overview.md).

## Sampler

Componente che sceglie il token successivo dalla distribuzione prodotta dal
modello, secondo una strategia di generazione. Vedi
[Inferenza con Gemma](modules/gemma-inference.md).

## Schema per il feedback

Struttura esplicita dei dati di feedback, con identificativi, contesto, risposta
valutata, segnale di preferenza e metadati necessari alla tracciabilità. Vedi
[Schema del feedback](modules/feedback-schema.md).

## Self-attention

Operazione in cui ogni token combina informazioni dagli altri token tramite pesi
calcolati da query, key e value. Vedi
[Matematica della self-attention](modules/self-attention-math.md).

## Sentence embedding

Un singolo vettore che rappresenta il contenuto semantico di un'intera frase o
memoria. Vedi [Sentence embeddings](modules/sentence-embeddings.md).

## Similarita' coseno

Misura della somiglianza tra due vettori basata sul coseno dell'angolo che li
separa, non sulla loro lunghezza. Vedi
[Similarità coseno](modules/cosine-similarity.md).

## Tensore

Array multidimensionale descritto da forma, numero di assi e tipo dei valori.
Vedi [Vettori, matrici e tensori](modules/vectors-matrices-tensors.md).

## Tokenizzazione

Trasformazione del testo in una sequenza di unità discrete che il modello può
mappare a identificativi numerici. Vedi
[Tokenizzazione e vocabolario](modules/tokenization-vocabulary.md).

## Train/validation/test

Tre partizioni con ruoli distinti: il train aggiorna i parametri, la validation
guida le scelte, il test misura una sola volta la generalizzazione finale. Vedi
[Train, validation e test](modules/train-validation-test.md).

## Transfer learning

Riutilizzo delle rappresentazioni apprese da un modello pre-addestrato per un
nuovo compito. Vedi
[Transfer learning e freezing](modules/transfer-learning-freezing.md).

## UMAP

Tecnica non lineare di riduzione dimensionale usata per esplorare e visualizzare
strutture locali negli embedding. Vedi [PCA e UMAP](modules/pca-umap.md).

## Vocabolario

Insieme finito dei token conosciuti da un sistema di rappresentazione del testo,
costruito sui dati di training per evitare leakage. Vedi
[Tokenizzazione e vocabolario](modules/tokenization-vocabulary.md).
