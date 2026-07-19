---
id: preference-tuning
title: Preference tuning di una politica
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [dpo-intuition, lora-from-scratch]
deliverables: [notebooks/lezione-49-preference-tuning.ipynb]
sources:
  - https://arxiv.org/abs/2305.18290
---

# Preference tuning di una politica

> **La lezione si segue nel notebook**
> `notebooks/lezione-49-preference-tuning.ipynb`: teoria, codice eseguibile, esercizio e il
> 49esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.

## Cosa saprai fare

Usare DPO per allineare una politica di scoring delle memorie alle
preferenze, con generalizzazione a memorie nuove.

## Teoria essenziale

Una **politica** $\pi_\theta(x)\propto\exp(\theta\cdot\text{feat}(x))$ da' un
punteggio dalle feature; la **reference** e' la politica iniziale; DPO alza la
log-prob relativa della chosen su ogni coppia. La costante di softmax si
**cancella** nella differenza chosen-rejected. Essendo un modello, generalizza.

## Cosa mostra il notebook

Il notebook DPO-tuna una politica lineare da 300 coppie rumorose: l'accuratezza
su coppie **mai viste** e' `0.79-0.84` e la politica si allinea alla preferenza
vera a coseno `0.974` — pur non avendola mai vista. Output reali.

## Collegamento al progetto

Il passo 49 aggiunge `preference_tuning(Fw, Fl)`, verificato con `assert` su
accuratezza train e generalizzazione.

## Fonti

- Rafailov et al., *DPO*, 2023 — <https://arxiv.org/abs/2305.18290>
