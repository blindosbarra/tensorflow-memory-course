---
id: train-validation-test
title: Train, validation e test
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [data-cleaning-01-missing-values, duplicates-types-outliers]
deliverables: [notebooks/lezione-03-train-validation-test.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
---

# Train, validation e test

> **La lezione si segue nel notebook** `notebooks/lezione-03-train-validation-test.ipynb`:
> teoria, dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> terzo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento. Prerequisito: aver eseguito i notebook delle Lezioni 1 e 2.

## Cosa saprai fare

Stimare onestamente quanto una regola predittiva funzionera' su dati mai
visti, scegliendo il tipo di divisione adatto alla natura dei dati.

## Teoria essenziale

Valutare sui dati di addestramento misura la memorizzazione, non
l'apprendimento: un modello flessibile puo' memorizzare qualsiasi tabella.
La valutazione onesta usa dati mai toccati.

I tre insiemi hanno contratti distinti: **train** per imparare,
**validation** per confrontare alternative e regolare scelte (usato molte
volte), **test** per la stima finale (usato una volta sola: ogni scelta
fatta guardando il test lo consuma).

Il tipo di divisione dipende dai dati: **casuale** con seed per righe
indipendenti; **stratificata** quando una classe e' rara (il caso puro puo'
lasciarla fuori da un insieme); **temporale** quando i dati hanno ordine nel
tempo — si impara dal passato e si valuta sul futuro, mai il contrario.

## Nel progetto

Il Memory AI Lab riceve lo storico simulato di tre mesi
(`memory_events_history.csv`), lo fa passare dalle difese delle Lezioni 1-2
e lo divide temporalmente in `memory_train/val/test.csv`, con assert che
verificano il contratto temporale.

## Errori comuni

- Scegliere il modello guardando il punteggio sul test set.
- Dividere casualmente dati che hanno un ordine temporale.
- Divisioni non riproducibili (senza seed).
- Ignorare la distribuzione delle classi negli insiemi risultanti.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, *Cross-validation: evaluating estimator performance*:
  https://scikit-learn.org/stable/modules/cross_validation.html
- scikit-learn, `train_test_split`:
  https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
