# Riferimenti

Tutte le fonti citate dalle lezioni, raggruppate per modulo.

<!-- Pagina generata da scripts/build_references.py: non modificarla a mano.
     Le fonti si aggiungono nella sezione "## Fonti" della lezione, poi si
     rigenera con `uv run python scripts/build_references.py`. -->

## foundations

- NumPy, *the absolute basics for beginners* — <https://numpy.org/doc/stable/user/absolute_beginners.html> (python-numpy-refresh)
- NumPy, *What is NumPy?* — <https://numpy.org/doc/stable/user/whatisnumpy.html> (python-numpy-refresh)
- NumPy, *Broadcasting* — <https://numpy.org/doc/stable/user/basics.broadcasting.html> (vectors-matrices-tensors)
- NumPy, `matmul` — <https://numpy.org/doc/stable/reference/generated/numpy.matmul.html> (vectors-matrices-tensors)
- Goodfellow, Bengio, Courville, *Deep Learning*, cap. 4 — <https://www.deeplearningbook.org/> (derivatives-gradients-chain-rule, probability-loss-functions)
- scikit-learn, *Log loss* — <https://scikit-learn.org/stable/modules/model_evaluation.html#log-loss> (probability-loss-functions)

## data-engineering

- Rubin (1976), *Inference and Missing Data*: meccanismi e ignorabilita' — <https://doi.org/10.1093/biomet/63.3.581> (data-cleaning-01-missing-values)
- NIST/SEMATECH, *Measures of Location*: sensibilita' di media e mediana — <https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm> (data-cleaning-01-missing-values)
- scikit-learn, *Imputation of missing values*: baseline e indicatori — <https://scikit-learn.org/stable/modules/impute.html> (data-cleaning-01-missing-values)
- NIST/SEMATECH, *Detection of Outliers*: criterio statistico IQR — <https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm> (duplicates-types-outliers)
- Chaudhuri et al. (2003), *Robust and Efficient Fuzzy Match for Online Data Cleaning*: trade-off del matching — <https://doi.org/10.1145/872757.872796> (duplicates-types-outliers)
- pandas, `DataFrame.duplicated`: subset e keep policy — <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html> (duplicates-types-outliers)
- scikit-learn, *Cross-validation: evaluating estimator performance* — <https://scikit-learn.org/stable/modules/cross_validation.html> (train-validation-test)
- scikit-learn, `train_test_split` — <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html> (train-validation-test)
- scikit-learn, *Common pitfalls: data leakage* — <https://scikit-learn.org/stable/common_pitfalls.html> (data-leakage)
- scikit-learn, *Pipelines and composite estimators* — <https://scikit-learn.org/stable/modules/compose.html> (data-leakage)
- scikit-learn, *Preprocessing data* — <https://scikit-learn.org/stable/modules/preprocessing.html> (categorical-encoding-scaling)
- pandas, `get_dummies` — <https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html> (categorical-encoding-scaling)
- TensorFlow, *tf.data: Build TensorFlow input pipelines* — <https://www.tensorflow.org/guide/data> (tfdata-basics)
- TensorFlow, *Better performance with the tf.data API* — <https://www.tensorflow.org/guide/data_performance> (tfdata-basics)

## keras-dnn

- Keras, *The Sequential model* — <https://keras.io/guides/sequential_model/> (perceptron-dense-layer)
- Keras, `Dense` — <https://keras.io/api/layers/core_layers/dense/> (perceptron-dense-layer)
- TensorFlow, *Basic classification* — <https://www.tensorflow.org/tutorials/keras/classification> (perceptron-dense-layer)
- TensorFlow, *Autodiff* — <https://www.tensorflow.org/guide/autodiff> (model-fit-under-the-hood)
- Keras, *Writing a training loop from scratch* — <https://keras.io/guides/writing_a_custom_training_loop_in_tensorflow/> (model-fit-under-the-hood)
- TensorFlow, *Overfit and underfit* — <https://www.tensorflow.org/tutorials/keras/overfit_and_underfit> (regularization-dropout)
- Keras, `EarlyStopping` — <https://keras.io/api/callbacks/early_stopping/> (regularization-dropout)
- Keras, `Dropout` — <https://keras.io/api/layers/regularization_layers/dropout/> (regularization-dropout)
- scikit-learn, *Model evaluation* — <https://scikit-learn.org/stable/modules/model_evaluation.html> (evaluation-calibration)
- Guo et al. (2017), *On Calibration of Modern Neural Networks* — <https://arxiv.org/abs/1706.04599> (evaluation-calibration)

## text-embeddings

- Keras, `TextVectorization` — <https://keras.io/api/layers/preprocessing_layers/text/text_vectorization/> (tokenization-vocabulary)
- TensorFlow, *Basic text classification* — <https://www.tensorflow.org/tutorials/keras/text_classification> (tokenization-vocabulary)
- Keras, `Embedding` layer — <https://keras.io/api/layers/core_layers/embedding/> (embedding-layer)
- Keras, `GlobalAveragePooling1D` — <https://keras.io/api/layers/pooling_layers/global_average_pooling1d/> (embedding-layer)
- TensorFlow, *Word embeddings* — <https://www.tensorflow.org/text/guide/word_embeddings> (embedding-layer)
- Keras, `GlobalMaxPooling1D` — <https://keras.io/api/layers/pooling_layers/global_max_pooling1d/> (sentence-embeddings)
- Keras, *The Functional API* — <https://keras.io/guides/functional_api/> (sentence-embeddings)
- TensorFlow Hub, *Universal Sentence Encoder* (citato per contesto, non usato in questo notebook) — <https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder> (sentence-embeddings)
- scikit-learn, `cosine_similarity` — <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html> (cosine-similarity, retrieval-metrics)
- scikit-learn, *Pairwise metrics, Affinities and Kernels* — <https://scikit-learn.org/stable/modules/metrics.html> (cosine-similarity)
- scikit-learn, `PCA` — <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html> (pca-umap)
- scikit-learn, *Decomposing signals in components (PCA)* — <https://scikit-learn.org/stable/modules/decomposition.html#pca> (pca-umap)
- UMAP, documentazione ufficiale (citata per contesto teorico, pacchetto non installato in questo ambiente) — <https://umap-learn.readthedocs.io/en/latest/how_umap_works.html> (pca-umap)
- scikit-learn, `KMeans` — <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html> (clustering-memories)
- scikit-learn, *Clustering* — <https://scikit-learn.org/stable/modules/clustering.html#k-means> (clustering-memories)
- scikit-learn, `adjusted_rand_score` — <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html> (clustering-memories)
- Wikipedia, *Mean reciprocal rank* — <https://en.wikipedia.org/wiki/Mean_reciprocal_rank> (retrieval-metrics)

## memory-representation

- Python, documentazione ufficiale, modulo `dataclasses` — <https://docs.python.org/3/library/dataclasses.html> (memory-schema)
- pandas, `to_datetime` — <https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html> (memory-schema)
- pandas, `Series.map` — <https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html> (episodic-semantic-preference)
- pandas, `DataFrame.groupby` — <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html> (episodic-semantic-preference)
- Wikipedia, *Exponential decay* — <https://en.wikipedia.org/wiki/Exponential_decay> (time-recency-decay)
- Wikipedia, *Half-life* — <https://en.wikipedia.org/wiki/Half-life> (time-recency-decay)
- pandas, `Timestamp` — <https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html> (time-recency-decay)
- pandas, `DataFrame.sort_values` — <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html> (importance-scoring)
- Python, documentazione ufficiale, modulo `re` — <https://docs.python.org/3/library/re.html> (entity-event-relations, contradiction-and-update)
- Python, documentazione ufficiale, `itertools.combinations` — <https://docs.python.org/3/library/itertools.html#itertools.combinations> (entity-event-relations)
- NetworkX, `Graph` — <https://networkx.org/documentation/stable/reference/classes/graph.html> (graph-memory-networkx, hybrid-retrieval)
- NetworkX, `spring_layout` — <https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html> (graph-memory-networkx)
- scikit-learn, `cosine_similarity` — <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html> (hybrid-retrieval)

## transformers-gemma

- Vaswani et al., *Attention Is All You Need*, 2017 — <https://arxiv.org/abs/1706.03762> (attention-intuition, self-attention-math, transformer-block, tokenizer-generation, gemma-inference)
- *numpy.exp* — <https://numpy.org/doc/stable/reference/generated/numpy.exp.html> (attention-intuition)
- Ba, Kiros e Hinton, *Layer Normalization*, 2016 — <https://arxiv.org/abs/1607.06450> (transformer-block)
- *numpy.random.Generator.choice* — <https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.choice.html> (tokenizer-generation)
- Hinton, Vinyals e Dean, *Distilling the Knowledge in a Neural Network*, 2015 — <https://arxiv.org/abs/1503.02531> (tokenizer-generation, gemma-inference)
- NumPy, *Random Generator* (`default_rng`) — <https://numpy.org/doc/stable/reference/random/generator.html> (tokenizer-generation)
- *KerasHub* — <https://keras.io/keras_hub/> (keras-hub)
- *KerasHub Models and Presets* — <https://keras.io/keras_hub/presets/> (keras-hub)
- *API `GemmaCausalLM`* — <https://keras.io/keras_hub/api/models/gemma/gemma_causal_lm/> (keras-hub, gemma-inference)
- *Gemma model card* (Google AI for Developers) — <https://ai.google.dev/gemma/docs/core/model_card> (keras-hub)
- *Gemma models — KerasHub* — <https://keras.io/keras_hub/api/models/gemma/> (gemma-inference)
- *API dei sampler KerasHub* — <https://keras.io/keras_hub/api/samplers/> (gemma-inference)
- *json — JSON encoder and decoder* — <https://docs.python.org/3/library/json.html> (structured-output)
- *JSON standard, RFC 8259* (IETF) — <https://www.rfc-editor.org/rfc/rfc8259> (structured-output)
- *JSON Schema: validazione* — <https://json-schema.org/draft/2020-12/json-schema-validation.html> (structured-output)
- *Metrics and scoring* (scikit-learn) — <https://scikit-learn.org/stable/modules/model_evaluation.html> (evaluation-generative)
- *FastChat — LLM Judge* (LMSYS Org) — <https://github.com/lm-sys/FastChat/blob/main/fastchat/llm_judge/README.md> (evaluation-generative)

## lora

- *Transfer learning & fine-tuning* (Keras) — <https://keras.io/guides/transfer_learning/> (transfer-learning-freezing)
- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685> (transfer-learning-freezing, lora-math, lora-from-scratch, gemma-lora, baseline-comparison, adapter-packaging)
- *Keras — Transfer learning & fine-tuning* (codice sorgente della guida) — <https://github.com/keras-team/keras-io/blob/master/guides/transfer_learning.py> (transfer-learning-freezing)
- *numpy.linalg.svd* — <https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html> (lora-math)
- Microsoft Research, *LoRA: Low-Rank Adaptation of Large Language Models* (repository ufficiale) — <https://github.com/microsoft/LoRA> (lora-math, lora-from-scratch, baseline-comparison, adapter-packaging)
- Microsoft Research, *LoRA reference implementation — loralib/layers.py* — <https://github.com/microsoft/LoRA/blob/main/loralib/layers.py> (lora-from-scratch)
- *Gemma models — KerasHub* — <https://keras.io/keras_hub/api/models/gemma/> (gemma-lora)
- Keras team, *sorgente `Backbone.enable_lora` di KerasHub* — <https://github.com/keras-team/keras-hub/blob/master/keras_hub/src/models/backbone.py> (gemma-lora)
- Dettmers et al., *QLoRA*, 2023 — <https://arxiv.org/abs/2305.14314> (qlora-concepts)
- *numpy.round* — <https://numpy.org/doc/stable/reference/generated/numpy.round.html> (qlora-concepts)
- Dettmers et al., *QLoRA — repository ufficiale* — <https://github.com/artidoro/qlora> (qlora-concepts)

## preference-learning

- Ouyang et al., *InstructGPT*, 2022 — <https://arxiv.org/abs/2203.02155> (feedback-schema, chosen-rejected-data, reward-functions, rlhf-rlaif-overview)
- Hugging Face, *documentazione TRL, formati dei dataset* — <https://github.com/huggingface/trl/blob/main/docs/source/dataset_formats.md> (feedback-schema)
- Hugging Face, *documentazione TRL, reward trainer* — <https://github.com/huggingface/trl/blob/main/docs/source/reward_trainer.md> (chosen-rejected-data, reward-functions, online-learning-risks)
- Rafailov et al., *DPO*, 2023 — <https://arxiv.org/abs/2305.18290> (dpo-intuition, preference-tuning)
- Hugging Face, *documentazione TRL, DPO trainer* — <https://github.com/huggingface/trl/blob/main/docs/source/dpo_trainer.md> (dpo-intuition, preference-tuning)
- Bai et al., *Constitutional AI*, 2022 — <https://arxiv.org/abs/2212.08073> (rlhf-rlaif-overview)
- Hugging Face, *documentazione TRL, indice dei trainer* — <https://github.com/huggingface/trl/blob/main/docs/source/index.md> (rlhf-rlaif-overview)
- Gao et al., *Reward Model Overoptimization*, 2022 — <https://arxiv.org/abs/2210.10760> (online-learning-risks)

## capstone

- Vaswani et al., 2017, *Attention Is All You Need* — <https://arxiv.org/abs/1706.03762> (capstone-architecture, capstone-embedding-graph)
- scikit-learn, *documentazione, Pipeline* — <https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/compose.rst> (capstone-architecture, capstone-dataset)
- scikit-learn, *Cross-validation* — <https://scikit-learn.org/stable/modules/cross_validation.html> (capstone-dataset)
- scikit-learn, *Logistic regression* — <https://scikit-learn.org/stable/modules/linear_model.html> (capstone-classifier)
- scikit-learn, *documentazione, model evaluation* — <https://github.com/scikit-learn/scikit-learn/blob/main/doc/modules/model_evaluation.rst> (capstone-classifier)
- scikit-learn, *Pairwise metrics — cosine similarity* — <https://scikit-learn.org/stable/modules/metrics.html> (capstone-embedding-graph)
- NetworkX, *Introduction* (rappresentazione del grafo) — <https://networkx.org/documentation/stable/reference/introduction.html> (capstone-embedding-graph)
- Keras documentation, *Gemma models — KerasHub* — <https://keras.io/keras_hub/api/models/gemma/> (capstone-gemma-lora)
- Keras documentation, *KerasHub, GemmaBackbone.enable_lora* — <https://keras.io/keras_hub/api/models/gemma/gemma_backbone/> (capstone-gemma-lora)
- scikit-learn, *Metrics and scoring* — <https://scikit-learn.org/stable/modules/model_evaluation.html> (capstone-evaluation, capstone-monitoring)
- Hu et al., 2021, *LoRA: Low-Rank Adaptation* — <https://arxiv.org/abs/2106.09685> (capstone-pipeline)
- scikit-learn, *Tuning the decision threshold for classification* — <https://scikit-learn.org/stable/modules/classification_threshold.html> (capstone-pipeline)
- Yurdakul e Naranjo, *The Population Resemblance Statistic: A Chi-Square Measure of Fit for Banking*, arXiv:2307.11878 — <https://arxiv.org/abs/2307.11878> (capstone-monitoring)
- Rafailov et al., 2023, *Direct Preference Optimization* — <https://arxiv.org/abs/2305.18290> (capstone-demo)
- IETF, *RFC 7231 §4.2.2, Idempotent Methods* — <https://www.rfc-editor.org/rfc/rfc7231> (capstone-demo)

## gcp-ml-certification

- Google Cloud, *Professional Machine Learning Engineer Certification exam guide* (fonte primaria verbatim, fornita dallo studente in questa sessione) — <https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf> (pmle-01-architect-low-code-ai-solutions, pmle-02-collaborate-manage-data-models, pmle-03-scale-prototypes-into-ml-models, pmle-04-serve-and-scale-models, pmle-05-automate-orchestrate-ml-pipelines, pmle-06-monitor-ai-solutions, pmle-07-architetture-end-to-end)
- Google Cloud, *Professional Machine Learning Engineer Certification* (pagina ufficiale, contesto generale sull'esame) — <https://cloud.google.com/learn/certification/machine-learning-engineer> (pmle-01-architect-low-code-ai-solutions, pmle-02-collaborate-manage-data-models, pmle-03-scale-prototypes-into-ml-models, pmle-04-serve-and-scale-models, pmle-05-automate-orchestrate-ml-pipelines, pmle-06-monitor-ai-solutions, pmle-07-architetture-end-to-end)
- Google Cloud, *BigQuery ML introduction* (da riverificare per i dettagli di sintassi/meccanismo, vedi riquadro in cima alla pagina) — <https://cloud.google.com/bigquery/docs/bqml-introduction> (pmle-01-architect-low-code-ai-solutions)
