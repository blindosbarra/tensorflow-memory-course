---
id: feedback-schema
title: Uno schema per il feedback
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [memory-schema, evaluation-generative]
deliverables: [notebooks/lezione-45-feedback-schema.ipynb]
sources:
  - https://arxiv.org/abs/2203.02155
---

# Uno schema per il feedback

> **La lezione si segue nel notebook**
> `notebooks/lezione-45-feedback-schema.ipynb`: teoria, codice eseguibile, esercizio e il
> 45esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.
> Apre la Fase 7 (feedback e preference training).

## Cosa saprai fare

Definire uno schema esplicito per il feedback dell'utente e un validatore: la
materia prima del preference training.

## Teoria essenziale

Il feedback puo' essere **assoluto** (un voto su una risposta) o **relativo**
(preferisco A a B). Il relativo e' piu' robusto perche' confrontare e' piu'
coerente che votare, ed e' la forma che alimenta RLHF e DPO (Lezioni 48-50).
Come le memorie (Lezione 22), lo schema va reso esplicito e validato.

## Cosa mostra il notebook

Il notebook definisce una dataclass `Feedback` (tipo, memory_id, `rispetto_a`
per le preferenze, peso) e un validatore: su un lotto di 5 feedback ne accetta 1
valido e ne scarta 4, ognuno con un motivo esplicito (id mancante, tipo
sconosciuto, preferenza senza controparte, peso fuori range). Output reali.

## Collegamento al progetto

Il passo 45 aggiunge `raccogli(feedbacks)`: solo i feedback conformi entrano
nella pipeline, gli altri sono scartati con motivo. E' il guardiano d'ingresso
del preference training.

## Fonti

- Ouyang et al., *InstructGPT*, 2022 — <https://arxiv.org/abs/2203.02155>
