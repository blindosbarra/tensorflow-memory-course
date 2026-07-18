---
id: qlora-concepts
title: 'QLoRA: quantizzazione + LoRA'
module: lora
status: learner_review
estimated_minutes: 30
prerequisites: [lora-from-scratch]
deliverables: [notebooks/lezione-42-qlora.ipynb]
sources:
  - https://arxiv.org/abs/2305.14314
  - https://numpy.org/doc/stable/reference/generated/numpy.round.html
---

# QLoRA: quantizzazione + LoRA

> **La lezione si segue nel notebook**
> `notebooks/lezione-42-qlora.ipynb`: **interamente eseguibile** in NumPy.
> Prerequisito: Lezione 40.

## Cosa saprai fare

Capire la **quantizzazione** (mostrata davvero: da float32 a interi e ritorno,
con l'errore misurato) e come **QLoRA** la combini con LoRA per adattare modelli
enormi su poca memoria.

## Teoria essenziale

I pesi in float32 costano 4 byte ciascuno. La **quantizzazione** li memorizza con
meno bit (int8, o 4-bit in QLoRA) dividendo per una *scala* e arrotondando: si
risparmia memoria al prezzo di un piccolo **errore**.

**QLoRA** (Dettmers et al., 2023):

1. **congela** il modello base **quantizzato a 4-bit** (poca memoria);
2. addestra **adapter LoRA** in precisione piu' alta *sopra* la base quantizzata.

Cosi' un modello enorme si adatta su una singola GPU.

## Cosa mostra il notebook

La quantizzazione int8 di una matrice 256×256 passa da `262144` a `65540` byte
(**4x meno**) con errore relativo `0.0113` — numeri realmente eseguiti. Un
`assert` verifica che QLoRA all'avvio (B=0) produca l'output della sola base
quantizzata. La tabella di memoria mostra il crollo con i bit (32→4 bit = 8→1 GB
per 2 miliardi di parametri) con la verifica `4-bit = 1/8 di float32`.

## Collegamento al progetto

Il passo 42 aggiunge `memoria_pesi(n_parametri, bit)`: decide se un modello
"entra" nell'hardware disponibile — la domanda pratica prima di scegliere QLoRA.

## Riepilogo

1. I pesi float32 costano 4 byte: tanta memoria.
2. Quantizzare = meno bit via scala + arrotondamento.
3. Si risparmia memoria al prezzo di un piccolo errore.
4. int8 ≈ 4x meno; 4-bit ≈ 8x meno.
5. **QLoRA**: base congelata a 4-bit + adapter LoRA in alta precisione.
6. Cosi' modelli enormi si adattano su una sola GPU.

## Fonti

- Dettmers et al., *QLoRA*, 2023 — <https://arxiv.org/abs/2305.14314>
- *numpy.round* — <https://numpy.org/doc/stable/reference/generated/numpy.round.html>
