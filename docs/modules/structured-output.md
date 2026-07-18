---
id: structured-output
title: Output strutturato
module: transformers-gemma
status: learner_review
estimated_minutes: 30
prerequisites: [memory-schema, gemma-inference]
deliverables: [notebooks/lezione-36-output-strutturato.ipynb]
sources:
  - https://docs.python.org/3/library/json.html
---

# Output strutturato

> **La lezione si segue nel notebook**
> `notebooks/lezione-36-output-strutturato.ipynb`. Prerequisiti: Lezioni 22, 35.
>
> ⚠️ **Nota di ambiente.** La cella che chiama Gemma e' guardata; il
> **validatore** gira sempre (parte pienamente eseguibile). Vedi
> `course/research_gaps.md`.

## Cosa saprai fare

Far produrre al modello un **JSON** conforme allo schema Memory AI Lab (Lezione
22) e — parte eseguibile — costruire il **validatore/riparatore** che accetta o
rifiuta l'output.

## Teoria essenziale

Un modello genera **testo libero**: per una pipeline serve un formato
macchina-leggibile. Strategia in due mosse:

1. **Chiedere** il formato nel prompt ("rispondi in JSON con i campi ...").
2. **Non fidarsi**: si estrae il blocco JSON, si valida contro lo schema
   (Lezione 22) e si **ripara o rifiuta**. `json.loads` solleva
   `JSONDecodeError` su input malformato — ed e' proprio questo a rendere
   necessario il validatore.

Il pezzo affidabile non e' il modello: e' il **validatore** attorno.

## Cosa mostra il notebook

La cella guardata mostra (o simula, con un output volutamente "sporco" avvolto
in testo discorsivo) la generazione. La funzione `estrai_e_valida` isola il
primo blocco `{...}` con una regex, fa `json.loads`, controlla campi e valori
(`type` ∈ episodic/semantic/preference). I test eseguibili verificano che
**accetti** un JSON valido e **rifiuti** sia un `type` errato sia un JSON
malformato.

## Riepilogo

1. Il modello produce testo libero; la pipeline vuole **JSON**.
2. Chiedi il formato ma **non fidarti** dell'output.
3. Estrai → valida (schema Lezione 22) → ripara o rifiuta.
4. Il pezzo affidabile e' il **validatore**.
5. Cosi' solo dati conformi entrano nel sistema di memorie.

## Fonti

- *json — JSON encoder and decoder* — <https://docs.python.org/3/library/json.html>
