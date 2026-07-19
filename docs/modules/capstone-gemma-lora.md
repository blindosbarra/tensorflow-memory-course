---
id: capstone-gemma-lora
title: Estrazione strutturata con Gemma + LoRA
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-embedding-graph, gemma-lora, structured-output]
deliverables: [notebooks/lezione-56-capstone-gemma-lora.ipynb]
sources:
  - https://keras.io/keras_hub/api/models/gemma/
---

# Estrazione strutturata con Gemma + LoRA

> **La lezione si segue nel notebook**
> `notebooks/lezione-56-capstone-gemma-lora.ipynb`: teoria, codice eseguibile, esercizio e il 56esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.
> ⚠️ **Nota di ambiente**: la cella Gemma e' guardata e saltata in questo
> ambiente/CI; il fallback a regole e' eseguibile. Vedi `course/research_gaps.md`.

## Cosa saprai fare

Aggiungere l'estrazione delle relazioni con un modello open adattato via LoRA, con un fallback a regole sempre funzionante.

## Teoria essenziale

Le `relations` sono triple (source, type, target). Gemma+LoRA (Lezione 41) vincolato a output strutturato (Lezione 36) le estrae; il lab pero' deve funzionare **anche senza modello**, quindi un estrattore a regole (verbo noto tra due entita') fa da fallback.

## Cosa mostra il notebook

La cella Gemma (con `enable_lora`) e' **guardata** e saltata in questo ambiente; il fallback a regole gira davvero ed estrae `(Marco, visited, Glasgow)`. Un `assert` lo verifica.

## Collegamento al progetto

Il passo 56 fornisce `estrai_relazioni`, l'ultimo componente-contenuto del record.

## Fonti

- Keras documentation, *Gemma models — KerasHub* — <https://keras.io/keras_hub/api/models/gemma/>
