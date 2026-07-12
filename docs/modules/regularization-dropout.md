---
id: regularization-dropout
title: Overfitting, dropout ed early stopping
module: keras-dnn
status: learner_review
estimated_minutes: 30
prerequisites: [model-fit-under-the-hood]
deliverables: [notebooks/lezione-12-overfitting.ipynb]
sources:
  - https://www.tensorflow.org/tutorials/keras/overfit_and_underfit
  - https://keras.io/api/callbacks/early_stopping/
  - https://keras.io/api/layers/regularization_layers/dropout/
---

# Overfitting, dropout ed early stopping

> **La lezione si segue nel notebook**
> `notebooks/lezione-12-overfitting.ipynb`. Questa pagina e' il riassunto
> di riferimento. Consolida le lezioni pianificate `regularization-dropout`
> e `callbacks-checkpoints`, e apre la valutazione finale.

## Cosa saprai fare

Diagnosticare l'overfitting dalle curve train/validation, contenerlo con
early stopping e dropout, e condurre una valutazione finale onesta con il
test set aperto una volta sola.

## Teoria essenziale

Un modello con piu' parametri che esempi memorizza: loss di train verso
zero, validation che risale — il punto di svolta e' il momento di fermarsi.
Early stopping (patience + restore_best_weights) e dropout sono le prime
contromisure. Su un test piccolo la stima e' rumorosa: differenze di pochi
esempi non sono verdetti, e l'incertezza va dichiarata insieme al numero.

## Nel progetto

Il modello finale (capacita' moderata + dropout + early stopping) viene
scelto su train+validation e valutato una sola volta sul test, accanto alla
baseline della Fase 0. Il classificatore e' salvato in
`models/memory_type_classifier.keras`: il primo modello di produzione del
Memory AI Lab.

## Fonti

- TensorFlow, *Overfit and underfit*:
  https://www.tensorflow.org/tutorials/keras/overfit_and_underfit
- Keras, `EarlyStopping`: https://keras.io/api/callbacks/early_stopping/
- Keras, `Dropout`: https://keras.io/api/layers/regularization_layers/dropout/
