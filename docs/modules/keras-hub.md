---
id: keras-hub
title: 'KerasHub: caricare un modello pre-addestrato'
module: transformers-gemma
status: learner_review
estimated_minutes: 25
prerequisites: [transformer-block, tokenizer-generation]
deliverables: [notebooks/lezione-34-keras-hub.ipynb]
sources:
  - https://keras.io/keras_hub/
---

# KerasHub: caricare un modello pre-addestrato

> **La lezione si segue nel notebook**
> `notebooks/lezione-34-keras-hub.ipynb`. Prerequisiti: Lezioni 32–33.
>
> ⚠️ **Nota di ambiente.** Le celle che scaricano/eseguono Gemma sono
> **guardate**: in questo ambiente (e in CI) vengono saltate, perche' il
> pacchetto KerasHub e i pesi Gemma sono un extra opzionale che richiede un
> download autenticato di diversi GB e una GPU. Il codice mostrato e' l'API
> reale e gira su una macchina configurata. La parte di progetto e' pienamente
> eseguibile. Dettaglio in `course/research_gaps.md`.

## Cosa saprai fare

Capire cosa e' **KerasHub**, usare `from_preset` per caricare un modello
pre-addestrato e distinguere **backbone** da **task model**.

## Teoria essenziale

Riscrivere un Transformer da zero (Lezioni 30–32) serve a capirlo, non a usarlo
in produzione. **KerasHub** distribuisce architetture e **preset** (pesi
pre-addestrati). Due livelli:

- **Backbone**: la pila di blocchi Transformer; produce rappresentazioni.
- **Task model** (es. `GemmaCausalLM`): backbone + testa per un compito (qui
  *causal language modeling*), tokenizer incluso.

Tutto si carica con `keras_hub.models.GemmaCausalLM.from_preset("gemma_2b_en")`.

## Cosa mostra il notebook

La cella del modello (guardata) e' l'API reale. La cella di **progetto**
eseguibile definisce un registro dei preset e una funzione `scegli_preset`
che, dato il fabbisogno (multilingua o no), restituisce il preset adatto — con
`assert` di non-regressione che girano senza il modello.

## Riepilogo

1. KerasHub distribuisce architetture e **preset**.
2. `from_preset("...")` carica backbone + tokenizer + testa.
3. **Backbone** = rappresentazioni; **task model** = backbone + testa.
4. Un preset da miliardi di parametri richiede tipicamente una GPU.
5. Il contratto (quale preset, quali requisiti) si testa anche senza modello.

## Fonti

- *KerasHub* — <https://keras.io/keras_hub/>
