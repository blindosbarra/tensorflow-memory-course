# Glossario

## Adapter

Insieme compatto di parametri addestrati per adattare un modello mantenendo
separati i pesi di base. Vedi [Packaging degli adapter](modules/adapter-packaging.md).

## Backpropagation

Applicazione della regola della catena che propaga il gradiente della loss
dall'output verso i parametri del modello. Vedi [Derivate, gradienti e chain
rule](modules/derivatives-gradients-chain-rule.md).

## Blocco Transformer

Componente che combina self-attention, rete feed-forward, connessioni residue e
normalizzazione. Vedi [Blocco Transformer](modules/transformer-block.md).

## Calibrazione

Coerenza tra una probabilita' prevista e la frequenza osservata dell'evento.
Vedi [Evaluation e calibrazione](modules/evaluation-calibration.md).

## Chosen/rejected

Coppia di risposte in cui `chosen` indica quella preferita e `rejected` quella
scartata. Vedi [Dati chosen/rejected](modules/chosen-rejected-data.md).

## Clustering

Raggruppamento non supervisionato di elementi simili senza etichette di classe
fornite in anticipo. Vedi [Clustering delle memorie](modules/clustering-memories.md).

## Contraddizione

Incompatibilita' tra due memorie riferite allo stesso fatto o stato. Deve
essere rilevata prima di decidere se conservare, aggiornare o collegare i
record. Vedi [Contraddizioni e aggiornamenti](modules/contradiction-and-update.md).

## Data leakage

Uso, durante il training o la preparazione delle feature, di informazione che
non sarebbe disponibile al momento della previsione. Vedi [Data
leakage](modules/data-leakage.md).

## Decadimento temporale

Riduzione del contributo di una memoria all'aumentare del tempo trascorso,
secondo una funzione dichiarata. Vedi [Tempo e recency
decay](modules/time-recency-decay.md).

## DPO

`Direct Preference Optimization`: adattamento diretto di un modello sulle
preferenze espresse da coppie chosen/rejected, senza addestrare separatamente
un reward model. Vedi [Intuizione della DPO](modules/dpo-intuition.md).

## Drift

Cambiamento nel tempo dei dati, delle predizioni o della relazione tra input e
risultato rispetto al riferimento usato per valutare il sistema. Vedi
[Monitoring del capstone](modules/capstone-monitoring.md).

## Dropout

Tecnica di regolarizzazione che durante il training disattiva casualmente una
parte delle attivazioni. Vedi [Regolarizzazione e
dropout](modules/regularization-dropout.md).

## Duplicato

Riga o memoria che replica un altro record secondo la chiave scelta. Vedi
[Duplicati, tipi e outlier](modules/duplicates-types-outliers.md).

## Embedding

Vettore denso appreso che rappresenta un elemento in modo che relazioni utili
possano emergere nello spazio vettoriale. Vedi [Embedding
layer](modules/embedding-layer.md).

## Episodic

Memoria di un evento collocato in un contesto, spesso con persone, luogo e
tempo. Vedi [Memorie episodiche, semantiche e di
preferenza](modules/episodic-semantic-preference.md).

## Freezing

Esclusione di alcuni pesi dagli aggiornamenti durante il training. Vedi
[Transfer learning e freezing](modules/transfer-learning-freezing.md).

## Gradiente

Vettore delle derivate parziali della loss rispetto ai parametri; indica la
direzione di crescita locale della loss. Vedi [Derivate, gradienti e chain
rule](modules/derivatives-gradients-chain-rule.md).

## GradientTape

Meccanismo TensorFlow che registra le operazioni necessarie a calcolare
automaticamente i gradienti. Vedi [Cosa fa `fit` sotto il
cofano](modules/model-fit-under-the-hood.md).

## Grafo delle memorie

Rappresentazione in cui memorie, entita' o eventi sono nodi e le loro relazioni
sono archi. Vedi [Grafo delle memorie con
NetworkX](modules/graph-memory-networkx.md).

## Imputazione

Sostituzione di un valore mancante con un valore calcolato o scelto secondo una
regola esplicita. Vedi [Valori
mancanti](modules/data-cleaning-01-missing-values.md).

## Learning rate

Iperparametro che controlla l'ampiezza dell'aggiornamento applicato ai pesi a
ogni passo di ottimizzazione. Vedi [Loss function e
probabilita'](modules/probability-loss-functions.md).

## LoRA

`Low-Rank Adaptation`: tecnica che mantiene congelati i pesi di base e
addestra matrici aggiuntive a rango ridotto. Vedi [LoRA da
zero](modules/lora-from-scratch.md).

## Loss function

Funzione scalare che misura l'errore da minimizzare durante il training. Vedi
[Loss function e probabilita'](modules/probability-loss-functions.md).

## Missing value

Valore assente in una tabella. In pandas puo' apparire con sentinelle diverse,
come `NaN`, `NaT` o `NA`. Vedi [Valori
mancanti](modules/data-cleaning-01-missing-values.md).

## Monitoring

Raccolta e osservazione continuativa di segnali che permettono di individuare
degrado, drift ed errori dopo il rilascio. Vedi [Monitoring del
capstone](modules/capstone-monitoring.md).

## MRR

`Mean Reciprocal Rank`: media del reciproco della posizione del primo risultato
rilevante nelle query valutate. Vedi [Metriche di
retrieval](modules/retrieval-metrics.md).

## Near-duplicate

Record non identico ma sufficientemente simile a un altro da richiedere una
regola esplicita di deduplicazione. Vedi [Duplicati, tipi e
outlier](modules/duplicates-types-outliers.md).

## Optimizer

Algoritmo che usa i gradienti per aggiornare i parametri e ridurre la loss.
Vedi [Cosa fa `fit` sotto il cofano](modules/model-fit-under-the-hood.md).

## Outlier

Osservazione molto distante dal comportamento atteso secondo una regola
dichiarata; non e' automaticamente un errore. Vedi [Duplicati, tipi e
outlier](modules/duplicates-types-outliers.md).

## Overfitting

Condizione in cui il modello si adatta troppo ai dati di training e generalizza
peggio su dati non visti. Vedi [Regolarizzazione e
dropout](modules/regularization-dropout.md).

## PCA

Tecnica lineare che proietta i dati lungo direzioni di varianza decrescente per
ridurne la dimensionalita'. Vedi [PCA e UMAP](modules/pca-umap.md).

## Pipeline

Sequenza riproducibile di passaggi che trasforma dati e artifact fino a
training, valutazione e rilascio. Vedi [Pipeline del
capstone](modules/capstone-pipeline.md).

## Preference

Memoria che descrive un gusto, una scelta o un vincolo associato a una persona
o a un contesto. Vedi [Memorie episodiche, semantiche e di
preferenza](modules/episodic-semantic-preference.md).

## Preference learning online

Aggiornamento del modello mentre arrivano nuovi dati o feedback, con rischi di
instabilita', bias e contaminazione. Vedi [Rischi dell'online
learning](modules/online-learning-risks.md).

## Punteggio di importanza

Assegnazione di un punteggio che stima quanto una memoria sia rilevante per la
conservazione o il recupero. Vedi [Importance
scoring](modules/importance-scoring.md).

## QLoRA

Variante di LoRA che quantizza il modello di base per ridurre la memoria
necessaria, mentre addestra adapter a rango ridotto. Vedi [Concetti di
QLoRA](modules/qlora-concepts.md).

## Quantizzazione

Rappresentazione di pesi o attivazioni con precisione numerica ridotta per
diminuire l'uso di memoria e, in alcuni casi, il costo di calcolo. Vedi
[Concetti di QLoRA](modules/qlora-concepts.md).

## Rank

Dimensione del sottospazio usato dalle matrici a basso rango di LoRA; regola la
capacita' dell'adapter e il numero di parametri addestrabili. Vedi [Matematica
di LoRA](modules/lora-math.md).

## Recall@K

Quota degli elementi rilevanti recuperati entro i primi `K` risultati. Vedi
[Metriche di retrieval](modules/retrieval-metrics.md).

## Retrieval ibrido

Recupero che combina segnali diversi, per esempio similarita' vettoriale e
vincoli o punteggi simbolici. Vedi [Retrieval
ibrido](modules/hybrid-retrieval.md).

## Reward function

Regola che trasforma il comportamento o il feedback in un segnale numerico da
ottimizzare. Vedi [Reward function](modules/reward-functions.md).

## RLAIF

`Reinforcement Learning from AI Feedback`: famiglia di metodi che usa feedback
generato da sistemi di AI come segnale di preferenza. Vedi [RLHF e
RLAIF](modules/rlhf-rlaif-overview.md).

## RLHF

`Reinforcement Learning from Human Feedback`: famiglia di metodi che usa
preferenze umane per orientare il comportamento di un modello. Vedi [RLHF e
RLAIF](modules/rlhf-rlaif-overview.md).

## Sampler

Regola che seleziona il token successivo dalla distribuzione prodotta dal
modello, in modo deterministico o stocastico. Vedi [Tokenizer e
generazione](modules/tokenizer-generation.md).

## Schema del feedback

Struttura dei campi usati per registrare una valutazione, la sua provenienza e
il contesto necessario a interpretarla. Vedi [Schema del
feedback](modules/feedback-schema.md).

## Self-attention

Operazione con cui ogni token pesa le rappresentazioni degli altri token della
sequenza per costruire una rappresentazione contestuale. Vedi [Matematica della
self-attention](modules/self-attention-math.md).

## Semantic

Memoria che rappresenta un fatto o una conoscenza senza dipendere da un
singolo episodio. Vedi [Memorie episodiche, semantiche e di
preferenza](modules/episodic-semantic-preference.md).

## Sentence embedding

Vettore che rappresenta un'intera frase o un intero testo in uno spazio adatto
al confronto semantico. Vedi [Sentence
embedding](modules/sentence-embeddings.md).

## Similarita' coseno

Similarita' tra due vettori misurata tramite il coseno dell'angolo che li
separa. Vedi [Cosine similarity](modules/cosine-similarity.md).

## Tensore

Array multidimensionale con forma e tipo definiti, usato come struttura dati di
base nei calcoli TensorFlow. Vedi [Vettori, matrici e
tensori](modules/vectors-matrices-tensors.md).

## Tokenizzazione

Trasformazione di un testo in unita' discrete che il modello puo' elaborare.
Vedi [Tokenizzazione e vocabolario](modules/tokenization-vocabulary.md).

## Train/validation/test

Tre partizioni con ruoli distinti: apprendimento dei parametri, scelta delle
configurazioni e valutazione finale su dati non usati nelle decisioni. Vedi
[Split train, validation e test](modules/train-validation-test.md).

## Transfer learning

Riutilizzo dei pesi appresi da un modello su un nuovo compito, con freezing o
fine-tuning di una parte dei parametri. Vedi [Transfer learning e
freezing](modules/transfer-learning-freezing.md).

## UMAP

Tecnica non lineare di riduzione dimensionale usata per esplorare strutture
locali in dati ad alta dimensionalita'. Vedi [PCA e UMAP](modules/pca-umap.md).

## Vocabolario

Insieme dei token conosciuti dal sistema e della loro associazione a indici
numerici. Vedi [Tokenizzazione e
vocabolario](modules/tokenization-vocabulary.md).
