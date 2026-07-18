---
id: lora-math
title: La matematica di LoRA
module: lora
status: learner_review
estimated_minutes: 30
prerequisites: [transfer-learning-freezing, derivatives-gradients-chain-rule]
deliverables: [notebooks/lezione-39-lora-math.ipynb]
sources:
  - https://arxiv.org/abs/2106.09685
  - https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html
---

# La matematica di LoRA

> **La lezione si segue nel notebook**
> `notebooks/lezione-39-lora-math.ipynb`. Prerequisiti: Lezioni 8, 38.

## Cosa saprai fare

Capire e implementare la decomposizione a basso rango $W = W_0 + BA$, misurare
il risparmio di parametri e vedere quando una LoRA di rango $r$ ricostruisce
esattamente un aggiornamento.

## Teoria essenziale

LoRA (Hu et al., 2021) osserva che l'aggiornamento $\Delta W$ per adattare un
grande strato $W_0$ ($d\times k$) e' spesso di **rango basso**. Invece di
imparare tutto $\Delta W$ ($d\cdot k$ parametri), lo scrive come:

$$W = W_0 + BA,\quad B\in\mathbb{R}^{d\times r},\ A\in\mathbb{R}^{r\times k},\ r\ll\min(d,k)$$

$W_0$ resta congelato; si addestrano solo $A,B$. Parametri: da $d\cdot k$ a
$r(d+k)$.

## Cosa mostra il notebook

Per $d=64,k=48$: a $r=1$ la LoRA usa 112 parametri (3.6% del pieno, 27x meno); a
$r=4$ ne usa 448 (14.6%, 6.9x meno). Costruendo un $\Delta W$ di rango esatto 3,
la migliore approssimazione di rango $r$ (via **SVD**, teorema di Eckart-Young)
ha errore relativo `0.6153` a $r=1$, `0.3509` a $r=2$ e **`0.0000` a $r=3$**:
quando $r$ raggiunge il rango vero, la LoRA cattura *esattamente*
l'aggiornamento. Numeri realmente eseguiti.

## Collegamento al progetto

Il passo 39 aggiunge `risparmio_lora(d, k, r)`, che giustifica la scelta di $r$
quando adatteremo il classificatore di memorie.

## Riepilogo

1. $\Delta W$ e' spesso di **rango basso**.
2. LoRA: $W_0 + BA$, con $r\ll d,k$.
3. $W_0$ congelato; si addestrano solo $A,B$.
4. Parametri: da $d\cdot k$ a $r(d+k)$.
5. Se rango($\Delta W$) $\le r$, $BA$ lo ricostruisce (SVD / Eckart-Young).
6. $r$ e' il pomello capacita'/costo.

## Fonti

- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685>
- *numpy.linalg.svd* — <https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html>
