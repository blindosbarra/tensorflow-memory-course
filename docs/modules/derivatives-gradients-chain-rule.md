---
id: derivatives-gradients-chain-rule
title: Derivate, gradienti e chain rule
module: foundations
status: learner_review
estimated_minutes: 30
prerequisites: [vectors-matrices-tensors]
deliverables: [notebooks/lezione-08-gradienti.ipynb]
sources:
  - https://www.deeplearningbook.org/
  - https://numpy.org/doc/stable/user/absolute_beginners.html
---

# Derivate, gradienti e chain rule

> **La lezione si segue nel notebook** `notebooks/lezione-08-gradienti.ipynb`.
> Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Leggere la derivata come sensibilita', verificare qualsiasi gradiente
numericamente, capire la discesa del gradiente e l'effetto del learning
rate (lento / giusto / divergente), e cosa fa davvero la backpropagation
(chain rule applicata all'indietro).

## Nel progetto

Il progetto impara i suoi primi parametri: una regressione lineare
addestrata a mano con discesa del gradiente (previsione, errore, gradiente,
passo), confrontata con la baseline "predici sempre la media".

## Fonti

- Goodfellow, Bengio, Courville, *Deep Learning*, cap. 4:
  https://www.deeplearningbook.org/
