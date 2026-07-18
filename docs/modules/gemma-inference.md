---
id: gemma-inference
title: Inferenza con Gemma
module: transformers-gemma
status: learner_review
estimated_minutes: 25
prerequisites: [tokenizer-generation, keras-hub]
deliverables: [notebooks/lezione-35-inferenza-gemma.ipynb]
sources:
  - https://keras.io/keras_hub/api/models/gemma/
---

# Inferenza con Gemma

> **La lezione si segue nel notebook**
> `notebooks/lezione-35-inferenza-gemma.ipynb`. Prerequisiti: Lezioni 33–34.
>
> ⚠️ **Nota di ambiente.** Come la Lezione 34, le celle Gemma sono guardate e
> saltate in questo ambiente/CI (pesi gated). Il codice e' l'API reale; la
> parte di progetto (estrattore con fallback a regole) e' eseguibile. Vedi
> `course/research_gaps.md`.

## Cosa saprai fare

Generare testo con **Gemma** via `.generate()`, ritrovando la temperatura/
sampler della Lezione 33, e costruire un estrattore che usa il modello se
disponibile e altrimenti un **fallback a regole**.

## Teoria essenziale

Caricato il task model (Lezione 34), l'inferenza e' una chiamata:
`gemma.generate(prompt, max_length=...)`. Il *come* si sceglie il prossimo
token — greedy o temperatura — e' la **stessa** meccanica della Lezione 33, e in
KerasHub si configura con `compile(sampler=...)`. Il modello sostituisce il
bigram come stimatore del prossimo token; **il ciclo autoregressivo e'
identico**.

## Cosa mostra il notebook

La cella `gemma.generate(...)` (guardata) mostra un prompt di estrazione della
citta'. La cella di **progetto** eseguibile definisce `estrai_entita(testo)`
che usa Gemma se presente e altrimenti l'euristica delle maiuscole della
Lezione 26 — con `assert` che verificano il fallback (`Marco`, `Glasgow`
estratti) senza alcun modello. Cosi' il sistema funziona sempre.

## Riepilogo

1. Inferenza = `gemma.generate(prompt, max_length=...)`.
2. Il sampler (`compile(sampler=...)`) e' il greedy/temperatura della Lezione 33.
3. Il modello sostituisce il bigram; il ciclo autoregressivo e' lo stesso.
4. Un buon sistema ha un **fallback** a regole quando il modello non c'e'.
5. L'output va sempre validato (Lezioni 36–37).

## Fonti

- *Gemma models — KerasHub* — <https://keras.io/keras_hub/api/models/gemma/>
