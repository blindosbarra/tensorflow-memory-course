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

**Sintesi eseguibile delle Lezioni 1-15**: `notebooks/consolidato-memoria-lezioni-01-15.ipynb`
esegue l'intera pipeline in un solo notebook, dai dati grezzi al
classificatore di memoria finale, con una stima delle risorse di calcolo
necessarie (RAM, disco, tempo) in fondo. Non sostituisce le 15 lezioni
singole (che restano il modo giusto per imparare passo per passo) — è un
riferimento rapido per vedere il percorso completo girare in un colpo solo.

## Prossime lezioni previste

Queste lezioni verranno costruite una alla volta, nell'ordine del
[syllabus](../syllabus.md). L'ordine puo' sembrare lento, ma serve a non
arrivare ai modelli con basi fragili.

### Fase 3 — Testo ed embedding (continua)

16. Embedding layer
17. Sentence embeddings e similarita'
18. Visualizzazione (PCA/UMAP) e clustering
19. Metriche di retrieval (Recall@K, MRR)

### E poi

20. Rappresentazione delle memorie (schema, importance, grafi, retrieval)
21. Transformer e Gemma
22. LoRA
23. Pipeline, monitoring e capstone

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
