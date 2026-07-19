---
id: reward-functions
title: Una reward function da zero
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [chosen-rejected-data, probability-loss-functions]
deliverables: [notebooks/lezione-47-reward-functions.ipynb]
sources:
  - https://arxiv.org/abs/2203.02155
---

# Una reward function da zero

> **La lezione si segue nel notebook**
> `notebooks/lezione-47-reward-functions.ipynb`: teoria, codice eseguibile, esercizio e il
> 47esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.

## Cosa saprai fare

Addestrare in NumPy un reward model che dia a ogni elemento un punteggio tale
che chosen > rejected, con la loss di Bradley-Terry.

## Teoria essenziale

Un **reward model** $r_\phi(x)$ da' un punteggio scalare. Non conosciamo il
vero punteggio, solo **preferenze**. Bradley-Terry:
$P(w\succ l)=\sigma(r_w-r_l)$; si addestra minimizzando $-\log\sigma(r_w-r_l)$
sulle coppie. E' la base del reward model di RLHF (Ouyang et al., 2022).

## Cosa mostra il notebook

In un esperimento **controllato** (una reward vera $w^\star$ nota genera
etichette rumorose), il reward addestrato solo dalle coppie **recupera** la
direzione vera a coseno `0.995` con accuratezza `0.84` (limitata dal rumore
delle etichette). Nota di onesta': una prima stesura tentava di predire
l'importanza da feature testuali deboli (lunghezza, parole forti) e falliva
(accuratezza 0.32, peggio del caso); sostituita dall'esperimento controllato
invece di sopravvalutare feature deboli.

## Collegamento al progetto

Il passo 47 aggiunge `allena_reward(Xw, Xl)`, verificato con un `assert` su
accuratezza e allineamento con la reward vera.

## Fonti

- Ouyang et al., *InstructGPT*, 2022 — <https://arxiv.org/abs/2203.02155>
