---
id: perceptron-dense-layer
title: La prima rete neurale
module: keras-dnn
status: learner_review
estimated_minutes: 30
prerequisites: [probability-loss-functions]
deliverables: [notebooks/lezione-10-prima-rete-neurale.ipynb]
sources:
  - https://keras.io/guides/sequential_model/
  - https://keras.io/api/layers/core_layers/dense/
  - https://www.tensorflow.org/tutorials/keras/classification
---

# La prima rete neurale

> **La lezione si segue nel notebook**
> `notebooks/lezione-10-prima-rete-neurale.ipynb`. Questa pagina e' il
> riassunto di riferimento. Con questa lezione comincia la Fase 2
> (TensorFlow/Keras). Richiede `uv sync --extra ml`.
> Consolida le lezioni pianificate `perceptron-dense-layer`,
> `forward-pass` e l'introduzione a `sequential-functional-api`.

## Cosa saprai fare

Costruire, addestrare e valutare una rete densa con Keras sapendo cosa fa
ogni riga: strato denso = somma pesata (Lezione 7), loss = cross-entropy
(Lezione 9), fit = il ciclo di training della Fase 0.

## Teoria essenziale

Un modello a un solo strato traccia solo confini lineari. La non-linearita'
(ReLU) tra gli strati e' cio' che permette confini curvi: senza, impilare
strati collassa in un solo strato lineare. La dimostrazione visiva usa le
due mezzelune: il modello lineare fallisce per costruzione, la rete piega
il confine. La capacita' (neuroni/strati) e' una scelta con un prezzo.

## Nel progetto

La prima rete del Memory AI Lab affronta l'asticella della Fase 0 (softmax
regression a mano) sulle stesse feature e gli stessi split, confrontandosi
su validation. Se il vantaggio e' piccolo, la diagnosi onesta e' che il
collo di bottiglia sono le feature, non il modello: la motivazione della
Fase 3 (embedding).

## Fonti

- Keras, *The Sequential model*: https://keras.io/guides/sequential_model/
- Keras, `Dense`: https://keras.io/api/layers/core_layers/dense/
- TensorFlow, *Basic classification*:
  https://www.tensorflow.org/tutorials/keras/classification
