---
id: capstone-pipeline
title: La pipeline: MemoryAILab
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-evaluation, memory-schema]
deliverables: [notebooks/lezione-58-capstone-pipeline.ipynb]
sources:
  - https://arxiv.org/abs/2106.09685
---

# La pipeline: MemoryAILab

> **La lezione si segue nel notebook**
> `notebooks/lezione-58-capstone-pipeline.ipynb`: teoria, codice eseguibile, esercizio e il 58esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Assemblare tutti i componenti in un'unica classe `MemoryAILab` che produce il record strutturato completo.

## Teoria essenziale

Si sostituiscono gli stub della Lezione 52 con i componenti reali (54-56) piu' l'importanza composita (Lezione 25). `process` li orchestra; `should_store` applica una soglia all'importanza: il lab decide cosa vale la pena ricordare.

## Cosa mostra il notebook

Un solo `process` produce il record completo (JSON) conforme allo schema obiettivo del `COURSE_FACTORY_SPEC.md` — per 'Marco visited Glasgow with his son.': type episodic, entities [Marco, Glasgow], relation (Marco, visited, Glasgow), importance 0.42, should_store true. Un `assert` verifica la presenza di tutti i campi del contratto.

## Collegamento al progetto

Il passo 58 e' l'obiettivo del corso: il Memory AI Lab funzionante end-to-end.

## Fonti

- Hu et al., 2021, *LoRA: Low-Rank Adaptation* — <https://arxiv.org/abs/2106.09685>
