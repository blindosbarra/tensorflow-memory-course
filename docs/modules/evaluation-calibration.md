---
id: evaluation-calibration
title: Valutare un classificatore
module: keras-dnn
status: learner_review
estimated_minutes: 30
prerequisites: [regularization-dropout]
deliverables: [notebooks/lezione-13-valutare-un-classificatore.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html
  - https://arxiv.org/abs/1706.04599
---

# Valutare un classificatore

> **La lezione si segue nel notebook**
> `notebooks/lezione-13-valutare-un-classificatore.ipynb`. Questa pagina
> e' il riassunto di riferimento. Chiude la Fase 2.

## Cosa saprai fare

Giudicare un classificatore oltre l'accuratezza: precision (falsi
allarmi), recall (casi persi), F1, confusion matrix come mappa degli
errori, e il controllo minimo di calibrazione (confidenza dichiarata vs
accuratezza reale).

## Nel progetto

La pagella completa del classificatore su validation (il test resta
consumato dalla Lezione 12): classification report, confusion matrix e
verifica di sovraconfidenza, con la lettura onesta dei numeri piccoli.

## Fonti

- scikit-learn, *Model evaluation*:
  https://scikit-learn.org/stable/modules/model_evaluation.html
- Guo et al. (2017), *On Calibration of Modern Neural Networks*:
  https://arxiv.org/abs/1706.04599
