---
id: tfdata-basics
title: Pipeline di input con tf.data
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [model-fit-under-the-hood]
deliverables: [notebooks/lezione-14-tf-data.ipynb]
sources:
  - https://www.tensorflow.org/guide/data
  - https://www.tensorflow.org/guide/data_performance
---

# Pipeline di input con tf.data

> **La lezione si segue nel notebook** `notebooks/lezione-14-tf-data.ipynb`.
> Questa pagina e' il riassunto di riferimento. Completa la parte
> TensorFlow della fase dati.

## Cosa saprai fare

Costruire pipeline di input pigre con shuffle/map/batch/prefetch,
conoscendo la trappola del buffer dello shuffle (mescola solo dentro la
finestra: su dati ordinati per tempo, buffer piccolo = batch quasi
ordinati) e l'ordine canonico degli operatori.

## Nel progetto

L'input del training diventa una pipeline tf.data con buffer pieno (i
dati del progetto sono ordinati per tempo), batch e prefetch: stessa rete,
stessi risultati, forma dell'input pronta per il testo al volo della
Fase 3.

## Fonti

- TensorFlow, *tf.data: Build TensorFlow input pipelines*:
  https://www.tensorflow.org/guide/data
- TensorFlow, *Better performance with the tf.data API*:
  https://www.tensorflow.org/guide/data_performance
