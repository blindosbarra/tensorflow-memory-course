---
id: tokenization-vocabulary
title: Tokenizzazione e vocabolario
module: text-embeddings
status: learner_review
estimated_minutes: 30
prerequisites: [categorical-encoding-scaling, regularization-dropout]
deliverables: [notebooks/lezione-15-tokenizzazione.ipynb]
sources:
  - https://keras.io/api/layers/preprocessing_layers/text/text_vectorization/
  - https://www.tensorflow.org/tutorials/keras/text_classification
---

# Tokenizzazione e vocabolario

> **La lezione si segue nel notebook**
> `notebooks/lezione-15-tokenizzazione.ipynb`. Questa pagina e' il
> riassunto di riferimento. Apre la Fase 3 (testo ed embedding).

## Cosa saprai fare

Trasformare testo in numeri: tokenizzazione, vocabolario costruito sul
solo train (leakage!), token OOV per le parole mai viste, bag of words
multi-hot e i suoi limiti (niente ordine, niente somiglianza tra parole).

## Nel progetto

Il momento della verita' del corso: il classificatore legge le parole
delle memorie (TextVectorization multi-hot) e l'accuratezza su validation
salta dal ~60-65% delle feature povere al ~95% — la conferma della
diagnosi onesta delle Lezioni 10-12 ("il collo di bottiglia sono le
feature"). I limiti del bag of words motivano gli embedding.

## Fonti

- Keras, `TextVectorization`:
  https://keras.io/api/layers/preprocessing_layers/text/text_vectorization/
- TensorFlow, *Basic text classification*:
  https://www.tensorflow.org/tutorials/keras/text_classification
