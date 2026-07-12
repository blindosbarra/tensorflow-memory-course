---
id: probability-loss-functions
title: Loss function
module: foundations
status: learner_review
estimated_minutes: 30
prerequisites: [derivatives-gradients-chain-rule]
deliverables: [notebooks/lezione-09-loss.ipynb]
sources:
  - https://www.deeplearningbook.org/
  - https://scikit-learn.org/stable/modules/model_evaluation.html#log-loss
---

# Loss function

> **La lezione si segue nel notebook** `notebooks/lezione-09-loss.ipynb`.
> Questa pagina e' il riassunto di riferimento. Chiude la Fase 0.

## Cosa saprai fare

Scegliere la loss giusta: MSE per la regressione (sensibile agli outlier),
softmax + cross-entropy per la classificazione (il -log punisce la
sicurezza sbagliata); capire perche' accuratezza e cross-entropy possono
dare verdetti diversi.

## Nel progetto

Tutti i pezzi della Fase 0 si compongono: una softmax regression addestrata
interamente a mano sulla matrice di feature, valutata contro le baseline
oneste (classe frequente, caso). I parametri salvati sono l'asticella che
la prima rete Keras della Fase 2 dovra' battere.

## Fonti

- Goodfellow, Bengio, Courville, *Deep Learning*, cap. 5-6:
  https://www.deeplearningbook.org/
- scikit-learn, *Log loss*:
  https://scikit-learn.org/stable/modules/model_evaluation.html#log-loss
