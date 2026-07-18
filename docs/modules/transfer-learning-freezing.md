---
id: transfer-learning-freezing
title: Transfer learning e freezing
module: lora
status: learner_review
estimated_minutes: 25
prerequisites: [model-fit-under-the-hood, transformer-block]
deliverables: [notebooks/lezione-38-transfer-learning.ipynb]
sources:
  - https://keras.io/guides/transfer_learning/
  - https://arxiv.org/abs/2106.09685
---

# Transfer learning e freezing

> **La lezione si segue nel notebook**
> `notebooks/lezione-38-transfer-learning.ipynb`. Prerequisiti: Lezioni 11, 32.
> Apre la Fase 6 (LoRA e adattamento efficiente).

## Cosa saprai fare

Capire perche' si **congelano** i pesi pre-addestrati e si addestra solo una
piccola parte, e misurare quanti parametri restano addestrabili — la premessa
che rende sensato LoRA (Lezione 39).

## Teoria essenziale

Un modello pre-addestrato porta rappresentazioni gia' utili. Per adattarlo:

- **Full fine-tuning**: aggiorni tutti i pesi → massima flessibilita', ma costo
  e memoria enormi e rischio di *catastrophic forgetting*.
- **Freezing + testa nuova**: **congeli** il corpo (nessun gradiente applicato)
  e addestri solo una testa piccola → economico, a volte poco espressivo.

LoRA sta nel mezzo: corpo congelato *piu'* pochi parametri addestrabili dentro
gli strati (Lezioni 39–40).

## Cosa mostra il notebook

Su un corpo finto a due strati densi piu' una testa, i parametri totali sono
432 e gli addestrabili (solo testa) 48 = **11.1%**. Un passo di training abbassa
la perdita (1.2423 → 0.9098) aggiornando *solo* la testa, e un `assert` verifica
che il corpo congelato resti **bit-identico**. Numeri realmente eseguiti.

## Collegamento al progetto

Il passo 38 aggiunge `riepilogo_parametri(moduli, addestrabili)`: il metro con
cui confronteremo full fine-tuning, freezing e LoRA nelle prossime lezioni con
numeri coerenti.

## Riepilogo

1. Il pre-addestrato porta rappresentazioni utili.
2. Full fine-tuning: tutto → costoso, rischio forgetting.
3. Freezing: corpo fermo, testa piccola → economico.
4. Congelare = non applicare il gradiente; i pesi restano invariati.
5. LoRA sta nel mezzo (Lezione 39).
6. Contare i parametri addestrabili confronta le strategie.

## Fonti

- *Transfer learning & fine-tuning* (Keras) — <https://keras.io/guides/transfer_learning/>
- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685>
