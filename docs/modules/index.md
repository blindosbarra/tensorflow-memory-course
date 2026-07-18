# Lezioni

Ogni lezione e' un notebook autosufficiente in `notebooks/` (teoria, esempi
eseguibili, esercizio con soluzione, passo del progetto); la pagina qui sul
sito e' il riassunto di riferimento. I notebook vanno eseguiti in ordine.

## Disponibili ora

1. [Missing values](data-cleaning-01-missing-values.md) —
   `notebooks/lezione-01-dati-mancanti.ipynb`
2. [Duplicati, tipi e outlier](duplicates-types-outliers.md) —
   `notebooks/lezione-02-duplicati-tipi-outlier.ipynb`
3. [Train, validation e test](train-validation-test.md) —
   `notebooks/lezione-03-train-validation-test.ipynb`
4. [Data leakage](data-leakage.md) —
   `notebooks/lezione-04-data-leakage.ipynb`
5. [Encoding e scaling](categorical-encoding-scaling.md) —
   `notebooks/lezione-05-encoding-scaling.ipynb`
6. [NumPy, pensare per array](python-numpy-refresh.md) —
   `notebooks/lezione-06-numpy.ipynb`
7. [Vettori, matrici e tensori](vectors-matrices-tensors.md) —
   `notebooks/lezione-07-tensori.ipynb`
8. [Derivate, gradienti e chain rule](derivatives-gradients-chain-rule.md) —
   `notebooks/lezione-08-gradienti.ipynb`
9. [Loss function](probability-loss-functions.md) —
   `notebooks/lezione-09-loss.ipynb`
10. [La prima rete neurale](perceptron-dense-layer.md) —
    `notebooks/lezione-10-prima-rete-neurale.ipynb`
11. [Dentro il training](model-fit-under-the-hood.md) —
    `notebooks/lezione-11-dentro-il-training.ipynb`
12. [Overfitting, dropout ed early stopping](regularization-dropout.md) —
    `notebooks/lezione-12-overfitting.ipynb`
13. [Valutare un classificatore](evaluation-calibration.md) —
    `notebooks/lezione-13-valutare-un-classificatore.ipynb`
14. [Pipeline di input con tf.data](tfdata-basics.md) —
    `notebooks/lezione-14-tf-data.ipynb`
15. [Tokenizzazione e vocabolario](tokenization-vocabulary.md) —
    `notebooks/lezione-15-tokenizzazione.ipynb`
16. [Embedding layer](embedding-layer.md) —
    `notebooks/lezione-16-embedding.ipynb`
17. [Sentence embeddings e similarita'](sentence-embeddings.md) —
    `notebooks/lezione-17-sentence-embeddings.ipynb`
18. [Similarita' coseno](cosine-similarity.md) —
    `notebooks/lezione-18-cosine-similarity.ipynb`
19. [Visualizzazione (PCA/UMAP)](pca-umap.md) —
    `notebooks/lezione-19-pca-umap.ipynb`
20. [Clustering delle memorie](clustering-memories.md) —
    `notebooks/lezione-20-clustering.ipynb`
21. [Metriche di retrieval (Recall@K, MRR)](retrieval-metrics.md) —
    `notebooks/lezione-21-retrieval-metrics.ipynb`
22. [Schema della memoria](memory-schema.md) —
    `notebooks/lezione-22-schema-memoria.ipynb`
23. [Episodic, semantic, preference](episodic-semantic-preference.md) —
    `notebooks/lezione-23-episodic-semantic-preference.ipynb`
24. [Decadimento temporale (recency)](time-recency-decay.md) —
    `notebooks/lezione-24-recency-decay.ipynb`
25. [Un punteggio di importanza composito](importance-scoring.md) —
    `notebooks/lezione-25-importance-scoring.ipynb`
26. [Entita' e relazioni](entity-event-relations.md) —
    `notebooks/lezione-26-entita-e-relazioni.ipynb`
27. [Il grafo delle memorie](graph-memory-networkx.md) —
    `notebooks/lezione-27-grafo-memorie.ipynb`
28. [Retrieval ibrido](hybrid-retrieval.md) —
    `notebooks/lezione-28-retrieval-ibrido.ipynb`
29. [Contraddizioni e aggiornamento](contradiction-and-update.md) —
    `notebooks/lezione-29-contraddizioni.ipynb`
30. [L'attenzione come recupero morbido](attention-intuition.md) —
    `notebooks/lezione-30-attention-intuition.ipynb`
31. [Self-attention, la matematica](self-attention-math.md) —
    `notebooks/lezione-31-self-attention.ipynb`
32. [Il blocco Transformer](transformer-block.md) —
    `notebooks/lezione-32-blocco-transformer.ipynb`
33. [Tokenizer e generazione](tokenizer-generation.md) —
    `notebooks/lezione-33-tokenizer-generazione.ipynb`
34. [KerasHub: modelli pre-addestrati](keras-hub.md) —
    `notebooks/lezione-34-keras-hub.ipynb`
35. [Inferenza con Gemma](gemma-inference.md) —
    `notebooks/lezione-35-inferenza-gemma.ipynb`
36. [Output strutturato](structured-output.md) —
    `notebooks/lezione-36-output-strutturato.ipynb`
37. [Valutare un modello generativo](evaluation-generative.md) —
    `notebooks/lezione-37-valutazione-generativa.ipynb`
38. [Transfer learning e freezing](transfer-learning-freezing.md) —
    `notebooks/lezione-38-transfer-learning.ipynb`
39. [La matematica di LoRA](lora-math.md) —
    `notebooks/lezione-39-lora-math.ipynb`
40. [LoRA da zero: addestrare un adapter](lora-from-scratch.md) —
    `notebooks/lezione-40-lora-from-scratch.ipynb`
41. [LoRA su Gemma](gemma-lora.md) —
    `notebooks/lezione-41-gemma-lora.ipynb`
42. [QLoRA: quantizzazione + LoRA](qlora-concepts.md) —
    `notebooks/lezione-42-qlora.ipynb`
43. [LoRA vs full fine-tuning](baseline-comparison.md) —
    `notebooks/lezione-43-baseline-comparison.ipynb`
44. [Impacchettare e distribuire un adapter](adapter-packaging.md) —
    `notebooks/lezione-44-adapter-packaging.ipynb`

**Sintesi eseguibile delle Lezioni 1-15**: `notebooks/consolidato-memoria-lezioni-01-15.ipynb`
esegue l'intera pipeline in un solo notebook, dai dati grezzi al
classificatore di memoria finale, con una stima delle risorse di calcolo
necessarie (RAM, disco, tempo) in fondo. Non sostituisce le 15 lezioni
singole (che restano il modo giusto per imparare passo per passo) — è un
riferimento rapido per vedere il percorso completo girare in un colpo solo.

Con la Lezione 21 si chiude la **Fase 3** (testo ed embedding): dal testo
grezzo (Lezione 15) a un sistema che rappresenta le memorie come vettori,
le confronta, le visualizza, le raggruppa senza etichette e valuta
onestamente la qualita' della ricerca. La Lezione 19 copre UMAP solo a
livello concettuale (nessun codice eseguito): il pacchetto `umap-learn`
non si installa in questo ambiente (conflitto di versione con Python
3.11) — la parte pratica usa solo PCA. Dettagli in
`course/research_gaps.md`.

Con la Lezione 29 si chiude anche la **Fase 4** (rappresentare le
memorie): schema esplicito e validato, type con parametri di decadimento
differenziati, recency, un punteggio di importanza composito, entita'
estratte con un'euristica dichiarata, un grafo bipartito memoria-entita',
retrieval ibrido (con un confronto onesto — non sempre a favore
dell'ibrido — contro il solo embedding) e gestione delle contraddizioni
che non cancella mai la storia.

## Prossime lezioni previste

Queste lezioni verranno costruite una alla volta, nell'ordine del
[syllabus](../syllabus.md). L'ordine puo' sembrare lento, ma serve a non
arrivare ai modelli con basi fragili.

La **Fase 5 — Transformer e modello open** (Lezioni 30–37) e' ora completa
e disponibile qui sopra: dall'attenzione implementata da zero in NumPy fino
a inferenza con Gemma, output strutturato e valutazione generativa. Le
Lezioni 34–37 usano un modello open (Gemma via KerasHub): le celle che
richiedono i pesi del modello sono **guardate** e vengono saltate quando il
modello non e' presente (come in CI), cosi' i notebook restano eseguibili e
il codice del modello resta reale per chi ha GPU e accesso a Gemma. Dettagli
in `course/research_gaps.md`.

La **Fase 6 — LoRA e adattamento efficiente** (Lezioni 38–44) e' ora
completa e disponibile qui sopra: freezing, la matematica del basso rango,
un adapter LoRA addestrato da zero in NumPy, QLoRA/quantizzazione, il
confronto onesto con il full fine-tuning e l'impacchettamento degli adapter.
La sola Lezione 41 (LoRA su Gemma) ha le celle del modello **guardate** come
nelle Lezioni 34–37; tutte le altre della fase sono interamente eseguibili.

### Prossime fasi

45. Pipeline, deploy e monitoring (MLOps)
46. Feedback e preference training
47. Memory AI Lab completo (capstone)

## Modulo facoltativo: certificazione GCP PMLE

Fuori dalla progressione obbligatoria sopra. Teoria pura, nessun notebook,
nessuna credenziale cloud — copre letteratura di prodotto Google Cloud per
la certificazione *Professional Machine Learning Engineer*, mappata 1:1
sui sei domini della exam guide ufficiale.

Tutti e sei i domini sono coperti, con contenuto verificato parola per
parola contro la exam guide ufficiale (fornita dallo studente in questa
sessione). Alcuni dettagli supplementari di sintassi/prodotto (non parte
della exam guide stessa) restano `needs_reverification`, segnalati in
ogni pagina — vedi `course/research_gaps.md`.

- [Dominio 1 — Architetture low-code](pmle-01-architect-low-code-ai-solutions.md) (~13%)
- [Dominio 2 — Collaborare su dati e modelli](pmle-02-collaborate-manage-data-models.md) (~16%)
- [Dominio 3 — Scalare i prototipi](pmle-03-scale-prototypes-into-ml-models.md) (~21%)
- [Dominio 4 — Servire e scalare i modelli](pmle-04-serve-and-scale-models.md) (~20%)
- [Dominio 5 — Automatizzare le pipeline](pmle-05-automate-orchestrate-ml-pipelines.md) (~18%)
- [Dominio 6 — Monitorare le soluzioni AI](pmle-06-monitor-ai-solutions.md) (~13%)
- [Sintesi — Architetture end-to-end e MLOps](pmle-07-architetture-end-to-end.md)
  (non è un dominio dell'esame: collega la teoria dei sei domini in
  quattro architetture complete, con diagrammi, troubleshooting e
  confronto MLOps tradizionale/generativo)

Disponibile anche in inglese: [GCP PMLE Certification (English)](en/pmle-01-architect-low-code-ai-solutions.md),
una traduzione fedele delle stesse sette lezioni.

## Come leggere una lezione

Ogni lezione dovrebbe rispondere a quattro domande:

- Che problema sto risolvendo?
- Quale concetto nuovo mi serve?
- Quale codice devo saper leggere?
- Come provo da solo?

Se una lezione non risponde a queste domande, va corretta prima di andare avanti.
