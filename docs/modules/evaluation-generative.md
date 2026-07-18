---
id: evaluation-generative
title: Valutare un modello generativo
module: transformers-gemma
status: learner_review
estimated_minutes: 30
prerequisites: [evaluation-calibration, structured-output]
deliverables: [notebooks/lezione-37-valutazione-generativa.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html
---

# Valutare un modello generativo

> **La lezione si segue nel notebook**
> `notebooks/lezione-37-valutazione-generativa.ipynb`: **interamente
> eseguibile** (nessun modello richiesto). Prerequisiti: Lezioni 13, 36.

## Cosa saprai fare

Valutare un estrattore con metriche **a livello di campo** (precision/recall/F1
sulle entita') su un set etichettato a mano, e capire il ruolo — e i rischi —
dell'**LLM-as-judge**.

## Teoria essenziale

Valutare la generazione e' piu' difficile della classificazione: spesso non
esiste **una** risposta giusta. Tre livelli:

1. **Exact match**: l'output e' esattamente quello atteso? Adatto a compiti
   vincolati (es. il `type` della memoria), inadatto al testo libero.
2. **Metriche a livello di campo**: per l'estrazione di entita' si contano
   TP/FP/FN **per entita'** e si calcolano precision/recall/F1 (le stesse della
   Lezione 13, applicate a insiemi).
3. **LLM-as-judge**: un secondo modello giudica la qualita' soggettiva
   (fluidita', pertinenza). Potente ma va **calibrato** su giudizi umani,
   altrimenti misura il bias del giudice.

## Cosa mostra il notebook

Su un piccolo set etichettato a mano (4 memorie, 7 entita' gold), l'estrattore a
regole della Lezione 26 ottiene `precision=1.0, recall=1.0, F1=1.0` (numeri
realmente eseguiti — il set e' piccolo e scelto per essere diagnostico, non un
benchmark). Il conteggio `tp/fp/fn` e' **diagnostico**: dice *dove* si sbaglia,
non solo un voto. Il passo di progetto fissa una **soglia di regressione**
(`assert F1 >= 0.8`): se una modifica futura peggiora l'estrattore, il test se
ne accorge.

## Riepilogo

1. Valutare la generazione e' difficile: spesso non c'e' una sola risposta
   giusta.
2. **Exact match** per compiti vincolati.
3. **P/R/F1 a livello di campo** per l'estrazione.
4. `fp`/`fn` sono **diagnostici**.
5. **LLM-as-judge** per la qualita' soggettiva, ma va **calibrato**.
6. Una soglia di F1 = **guardia di regressione** nel progetto.

## Fonti

- *Metrics and scoring* (scikit-learn) — <https://scikit-learn.org/stable/modules/model_evaluation.html>
