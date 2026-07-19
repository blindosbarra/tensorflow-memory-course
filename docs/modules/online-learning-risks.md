---
id: online-learning-risks
title: I rischi del preference learning online
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [reward-functions, preference-tuning]
deliverables: [notebooks/lezione-51-online-learning-risks.ipynb]
sources:
  - https://arxiv.org/abs/2210.10760
---

# I rischi del preference learning online

> **La lezione si segue nel notebook**
> `notebooks/lezione-51-online-learning-risks.ipynb`: teoria, codice eseguibile, esercizio e il
> 51esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.
> Chiude la Fase 7.

## Cosa saprai fare

Mostrare in NumPy il reward hacking (legge di Goodhart): ottimizzare un proxy
imperfetto fa salire il proxy ma peggiorare l'obiettivo vero.

## Teoria essenziale

**Reward hacking / Goodhart**: si ottimizza un *proxy* (il reward model), non
l'obiettivo vero; oltre un punto il proxy sale ma la qualita' vera scende
(Gao et al., 2022). Altri rischi online: **feedback loop** (gli output
diventano dati e amplificano i bias) e **distribution shift** (le preferenze
cambiano).

## Cosa mostra il notebook

L'ascesa sul proxy produce una **U rovesciata** nella qualita' vera: cresce,
**tocca il massimo al passo 29**, poi cala, mentre il proxy sale sempre (massimo
al passo 59). Un freno di **early stopping** sull'obiettivo vero si ferma al
passo 29, non al massimo del proxy. Output reali (una prima stesura lineare non
faceva davvero calare il vero ed e' stata corretta a un obiettivo distanza-dal-
target reale).

## Collegamento al progetto

Il passo 51 aggiunge `tuning_con_freno`: si smette di ottimizzare quando la
qualita' vera (misurata su un hold-out umano fidato) smette di salire.

## Fonti

- Gao et al., *Reward Model Overoptimization*, 2022 — <https://arxiv.org/abs/2210.10760>
