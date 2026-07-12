---
id: model-fit-under-the-hood
title: Dentro il training
module: keras-dnn
status: learner_review
estimated_minutes: 30
prerequisites: [perceptron-dense-layer]
deliverables: [notebooks/lezione-11-dentro-il-training.ipynb]
sources:
  - https://www.tensorflow.org/guide/autodiff
  - https://keras.io/guides/writing_a_custom_training_loop_in_tensorflow/
---

# Dentro il training

> **La lezione si segue nel notebook**
> `notebooks/lezione-11-dentro-il-training.ipynb`. Questa pagina e' il
> riassunto di riferimento. Consolida le lezioni pianificate
> `model-fit-under-the-hood` e `backprop-autodiff`.

## Cosa saprai fare

Aprire la scatola di `model.fit`: batch ed epoche, autodiff
(`GradientTape`) e un training loop scritto a mano in TensorFlow che
riproduce fit.

## Teoria essenziale

Il mini-batch stima il gradiente su una fetta di dati: piu' economico e
rumoroso il giusto. Un'epoca e' un giro completo. L'autodiff registra le
operazioni eseguite e applica la chain rule all'indietro (backpropagation
meccanizzata, esatta): la stessa derivata verificata numericamente nella
Lezione 8, automatizzata.

## Nel progetto

Il training della rete della Lezione 10 viene riscritto senza fit: dataset
a batch, GradientTape, apply_gradients — il ciclo previsione/errore/
gradiente/passo della Lezione 9, con gli upgrade veri.

## Fonti

- TensorFlow, *Autodiff*: https://www.tensorflow.org/guide/autodiff
- Keras, *Writing a training loop from scratch*:
  https://keras.io/guides/writing_a_custom_training_loop_in_tensorflow/
