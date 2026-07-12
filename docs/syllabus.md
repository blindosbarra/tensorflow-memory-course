# Syllabus

TensorFlow arriva dopo la fase dati per una ragione metodologica: un modello
trasforma gli input che riceve, ma non corregge definizioni ambigue, record
duplicati o split contaminati. Prima impari a rendere osservabili le decisioni
sui dati; poi trasformi quei dati in tensori e alleni modelli.

Questa mappa e' allineata 1:1 ai moduli e alle lezioni di
`course/course.yaml`. Il modulo `foundations`, prima saltato, e' reintegrato
come Fase 0: e' la scelta conservativa prevista dalla progressione obbligatoria
della spec. Non vengono create nuove lezioni da questo syllabus.

Ogni lezione dura 15-30 minuti. Le ore includono lettura, codice, quiz ed
esercizio; sono stime da validare con learner review.

## Come funziona una lezione

Ogni lezione e' un **notebook autosufficiente** in `notebooks/`: prima la
teoria del concetto generale (valida per qualsiasi dataset, non solo per il
corso), poi esempi eseguibili, poi un esercizio guidato con la soluzione
spiegata subito sotto, e infine **il passo del progetto**: un'unica
applicazione (il Memory AI Lab) che cresce di un componente a ogni lezione,
fino a diventare il sistema completo del capstone. Le pagine di questo sito
sono i riassunti di riferimento.

## Percorso minimo prioritario

Il percorso minimo mantiene le lezioni necessarie a produrre e valutare il
Memory AI Lab locale: `python-numpy-refresh`, `vectors-matrices-tensors`, tutte
le lezioni `data-engineering`, `perceptron-dense-layer`, `losses-optimizers`,
`backprop-autodiff`, `sequential-functional-api`, `evaluation-calibration`,
`tokenization-vocabulary`, `sentence-embeddings`, `cosine-similarity`,
`retrieval-metrics`, `memory-schema`, `importance-scoring`,
`entity-event-relations`, `graph-memory-networkx`, `hybrid-retrieval`,
`attention-intuition`, `keras-hub`, `gemma-inference`, `structured-output`,
`evaluation-generative`, `transfer-learning-freezing`, `lora-math`,
`gemma-lora`, `baseline-comparison`, `reproducible-project`,
`local-training-pipeline`, `model-evaluation`, `monitoring-drift`, tutte le
lezioni `preference-learning` e tutte le lezioni `capstone`.

Si tagliano dal percorso minimo solo approfondimenti ridondanti, visualizzazioni
opzionali e varianti cloud/hardware. Non si tagliano prerequisiti, controlli di
leakage, metriche, sicurezza, evaluation o artifact necessari al capstone.

## Fase 0 — Fondamenti minimi (2 ore)

Lezioni: `python-numpy-refresh`, `vectors-matrices-tensors`,
`derivatives-gradients-chain-rule`, `probability-loss-functions`.

Obiettivi misurabili: scrivere trasformazioni NumPy testate; prevedere shape e
broadcasting; calcolare un gradiente semplice; confrontare MSE e cross-entropy
su esempi piccoli. Assessment: implementare e testare una mini pipeline numerica
con controllo di shape, loss e gradiente.

## Fase 1 — Pulizia e pipeline dei dati (4 ore)

Lezioni: `data-cleaning-01-missing-values`, `duplicates-types-outliers`,
`train-validation-test`, `data-leakage`, `categorical-encoding-scaling`,
`tfdata-basics`, `tfdata-performance`, `data-validation`.

Obiettivi misurabili: diagnosticare e pulire dati senza nascondere modifiche;
creare split disgiunti; prevenire leakage; costruire e misurare una pipeline
`tf.data`. Assessment: consegnare dataset pulito, split verificati, pipeline
eseguibile e report delle decisioni.

## Fase 2 — Keras e reti neurali dense (4,5 ore)

Lezioni: `perceptron-dense-layer`, `forward-pass`, `losses-optimizers`,
`backprop-autodiff`, `sequential-functional-api`, `model-fit-under-the-hood`,
`regularization-dropout`, `callbacks-checkpoints`, `evaluation-calibration`.

Obiettivi misurabili: costruire una DNN, spiegare forward/backward pass,
confrontare loss e optimizer, diagnosticare overfitting e calibrazione.
Assessment: addestrare una DNN sintetica riproducibile e produrre metriche,
checkpoint e analisi degli errori.

## Fase 3 — Testo, embedding e visualizzazione (3,5 ore)

Lezioni: `tokenization-vocabulary`, `embedding-layer`, `sentence-embeddings`,
`cosine-similarity`, `pca-umap`, `clustering-memories`, `retrieval-metrics`.

Obiettivi misurabili: trasformare testo in vettori, calcolare similarita',
visualizzare cluster e misurare retrieval. Assessment: indice locale di memorie
con Recall@K e MRR su query etichettate.

## Fase 4 — Rappresentare le memorie (4 ore)

Lezioni: `memory-schema`, `episodic-semantic-preference`,
`time-recency-decay`, `importance-scoring`, `entity-event-relations`,
`graph-memory-networkx`, `hybrid-retrieval`, `contradiction-and-update`.

Obiettivi misurabili: validare record, calcolare recency/importance, costruire
un grafo e gestire conflitti. Assessment: pipeline locale che produce record,
grafo, retrieval ibrido e report di consistenza.

## Fase 5 — Transformer e modello open (4 ore)

Lezioni: `attention-intuition`, `self-attention-math`, `transformer-block`,
`tokenizer-generation`, `keras-hub`, `gemma-inference`, `structured-output`,
`evaluation-generative`.

Obiettivi misurabili: spiegare attention, verificare un preset compatibile,
generare output strutturato e misurarne gli errori. Assessment: estrazione JSON
con valid rate, field accuracy e confronto con baseline.

## Fase 6 — LoRA e adattamento efficiente (3,5 ore)

Lezioni: `transfer-learning-freezing`, `lora-math`, `lora-from-scratch`,
`gemma-lora`, `qlora-concepts`, `baseline-comparison`, `adapter-packaging`.

Obiettivi misurabili: distinguere pesi fissi/addestrabili, implementare LoRA,
misurare baseline e impacchettare adapter. Assessment: esperimento riproducibile
baseline/LoRA; QLoRA resta opzionale se l'hardware non e' adeguato.

## Fase 7 — Pipeline, deploy e monitoring (5 ore)

Lezioni: `reproducible-project`, `containers-artifacts`,
`local-training-pipeline`, `vertex-ai-training`, `vertex-ai-pipelines`,
`registry-deployment`, `batch-online-inference`, `model-evaluation`,
`monitoring-drift`, `cost-cleanup-security`.

Obiettivi misurabili: versionare artifact, eseguire una pipeline locale,
valutare, monitorare e documentare costi/cleanup cloud. Assessment: pipeline
locale completa e piano Vertex AI opzionale con smoke test e cleanup.

## Fase 8 — Feedback e preference training (3,5 ore)

Lezioni: `feedback-schema`, `chosen-rejected-data`, `reward-functions`,
`dpo-intuition`, `preference-tuning`, `rlhf-rlaif-overview`,
`online-learning-risks`.

Obiettivi misurabili: validare feedback, costruire coppie, definire reward,
eseguire un confronto controllato e descrivere rischi. Assessment: dataset di
preferenze validato e report baseline/tuning con limiti.

## Fase 9 — Memory AI Lab completo (4,5 ore)

Lezioni: `capstone-architecture`, `capstone-dataset`, `capstone-classifier`,
`capstone-embedding-graph`, `capstone-gemma-lora`, `capstone-evaluation`,
`capstone-pipeline`, `capstone-monitoring`, `capstone-demo`.

Obiettivi misurabili: integrare ingestion, modelli, retrieval, evaluation e
monitoring in un sistema locale riproducibile. Assessment: demo end-to-end con
test, report, artifact e limiti noti.

Totale stimato: 38,5 ore.

Stato corrente: sono disponibili come notebook le lezioni 1-5 (Fase 1,
parte pandas), 6-9 (Fase 0 completa) e 10-12 (primo blocco della Fase 2:
prima rete Keras, training loop aperto, overfitting e valutazione finale).
Il progetto ha un classificatore salvato (`models/`) valutato onestamente
contro la baseline della Fase 0. Le lezioni 10-12 consolidano coppie di
lezioni pianificate del modulo keras-dnn (perceptron+forward,
fit+backprop-autodiff, regularization+callbacks). Prossimi blocchi: il
resto della Fase 2 (functional API, evaluation/calibration), le lezioni
`tf.data`, poi la Fase 3 (testo ed embedding).
