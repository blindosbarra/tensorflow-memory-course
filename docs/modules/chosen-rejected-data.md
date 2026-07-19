---
id: chosen-rejected-data
title: Coppie chosen/rejected
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [feedback-schema]
deliverables: [notebooks/lezione-46-chosen-rejected.ipynb]
sources:
  - https://arxiv.org/abs/2203.02155
---

# Coppie chosen/rejected

> **La lezione si segue nel notebook**
> `notebooks/lezione-46-chosen-rejected.ipynb`: teoria, codice eseguibile, esercizio e il
> 46esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.

## Cosa saprai fare

Trasformare feedback grezzo in coppie (chosen, rejected) pulite: la struttura
dati che reward model (47) e DPO (48) consumano.

## Teoria essenziale

RLHF/DPO imparano da **coppie** (chosen $y_w$, rejected $y_l$), non da voti
isolati. Le coppie vengono da feedback `preference` o sono **derivate** da altri
segnali. Igiene dei dati: niente chosen==rejected, un margine minimo di
preferenza, e attenzione alle scorciatoie (es. bias di lunghezza).

## Cosa mostra il notebook

Dalle 61 memorie di tipo `preference` del corso il notebook costruisce 40
coppie (chosen = importanza piu' alta, con margine minimo; scartate le coppie a
testo identico). Un controllo sul bias di lunghezza mostra che la chosen e' piu'
lunga nel 60% delle coppie — un bias lieve segnalato onestamente da tenere
d'occhio. Output reali sui dati veri.

## Collegamento al progetto

Il passo 46 impacchetta la costruzione delle coppie con le regole d'igiene,
pronta per il reward model.

## Fonti

- Ouyang et al., *InstructGPT*, 2022 — <https://arxiv.org/abs/2203.02155>
