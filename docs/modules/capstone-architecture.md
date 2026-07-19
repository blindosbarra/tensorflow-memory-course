---
id: capstone-architecture
title: L'architettura del Memory AI Lab
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [hybrid-retrieval, online-learning-risks]
deliverables: [notebooks/lezione-52-capstone-architettura.ipynb]
sources:
  - https://arxiv.org/abs/1706.03762
---

# L'architettura del Memory AI Lab

> **La lezione si segue nel notebook**
> `notebooks/lezione-52-capstone-architettura.ipynb`: teoria, codice eseguibile, esercizio e il 52esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Fissare il contratto di output del progetto finale e lo scheletro della pipeline che le Lezioni 53-60 riempiranno con i componenti reali.

## Teoria essenziale

Il Memory AI Lab riceve una memoria testuale e produce un record strutturato; ogni campo e' il frutto di una fase del corso. Fissare ora il contratto (schema esplicito, Lezione 22) abilita sviluppo e test indipendenti dei componenti.

## Cosa mostra il notebook

Il notebook definisce la dataclass `MemoryRecord` con un validatore e uno scheletro di pipeline con componenti stub piu' una funzione `processa` che li orchestra; uno smoke test verifica che l'assemblaggio produca un record valido (`should_store` True/False).

## Collegamento al progetto

Il passo 52 fissa il contratto e lo scheletro; i componenti hanno firme stabili, cosi' le Lezioni 54-56 sostituiranno gli stub senza toccare l'orchestrazione.

## Fonti

- Vaswani et al., 2017, *Attention Is All You Need* — <https://arxiv.org/abs/1706.03762>
