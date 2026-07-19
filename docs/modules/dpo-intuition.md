---
id: dpo-intuition
title: L'intuizione di DPO
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [reward-functions, lora-from-scratch]
deliverables: [notebooks/lezione-48-dpo-intuition.ipynb]
sources:
  - https://arxiv.org/abs/2305.18290
---

# L'intuizione di DPO

> **La lezione si segue nel notebook**
> `notebooks/lezione-48-dpo-intuition.ipynb`: teoria, codice eseguibile, esercizio e il
> 48esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.

## Cosa saprai fare

Implementare la loss DPO in NumPy e vedere che ottimizza la politica
direttamente dalle preferenze, senza un ciclo di RL separato.

## Teoria essenziale

RLHF classico: reward model + RL con vincolo KL verso una reference. **DPO**
(Rafailov et al., 2023) fonde i due passi in **una sola loss** sulle coppie;
$\log\pi_\theta-\log\pi_{ref}$ e' un **reward implicito**, e $\beta$ controlla
quanto ci si allontana dalla reference. Niente reward model esplicito, niente
RL.

## Cosa mostra il notebook

Il notebook implementa la loss DPO su log-prob giocattolo: partendo dalla
reference (margine implicito 0.0), il training porta la loss `0.6931 -> 0.4202`
e il margine medio `0.0 -> 1.30`, con il 100% delle coppie che finisce
chosen>rejected. Output reali.

## Collegamento al progetto

Il passo 48 prepara il metodo con cui, nella Lezione 49, si allinea una
politica di scoring alle preferenze senza infrastruttura RL.

## Fonti

- Rafailov et al., *DPO*, 2023 — <https://arxiv.org/abs/2305.18290>
