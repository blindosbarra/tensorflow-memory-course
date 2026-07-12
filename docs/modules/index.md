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

## Prossime lezioni previste

Queste lezioni verranno costruite una alla volta, nell'ordine del
[syllabus](../syllabus.md). L'ordine puo' sembrare lento, ma serve a non
arrivare ai modelli con basi fragili.

### Fase 2 — Keras e reti neurali dense

10. Dense layer e prima rete
11. Forward pass
12. Loss e optimizer in Keras
13. Autodiff e backprop
14. Sequential e Functional API

### Fase 1 — Dati e pulizia (code TensorFlow, dopo l'introduzione di TF)

15. `tf.data` base
16. Performance con `tf.data`
17. Validazione dati

### Keras e DNN

13. Dense layer
14. Forward pass
15. Loss e optimizer
16. Autodiff e backprop
17. Sequential e Functional API
18. Cosa succede dentro `model.fit`
19. Regularization e dropout
20. Evaluation e calibration

### Memorie, retrieval e modelli open

21. Testo ed embedding
22. Rappresentazione delle memorie
23. Grafi e retrieval
24. Transformer e Gemma
25. LoRA
26. Pipeline, monitoring e capstone

## Come leggere una lezione

Ogni lezione dovrebbe rispondere a quattro domande:

- Che problema sto risolvendo?
- Quale concetto nuovo mi serve?
- Quale codice devo saper leggere?
- Come provo da solo?

Se una lezione non risponde a queste domande, va corretta prima di andare avanti.
