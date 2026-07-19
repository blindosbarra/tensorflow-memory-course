---
id: capstone-evaluation
title: Valutazione offline del lab
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-classifier, retrieval-metrics, evaluation-generative]
deliverables: [notebooks/lezione-57-capstone-valutazione.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html
---

# Valutazione offline del lab

> **La lezione si segue nel notebook**
> `notebooks/lezione-57-capstone-valutazione.ipynb`: teoria, codice eseguibile, esercizio e il 57esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Produrre un unico report che valuta classificatore, retrieval ed estrazione relazioni sul test set.

## Teoria essenziale

'Funziona' richiede numeri, componente per componente, su dati mai visti: accuratezza (Lezione 13), Precision@k (Lezione 21), F1 sulle relazioni (Lezione 37). Un report unico rende il progetto verificabile.

## Cosa mostra il notebook

Sul test set: classificatore accuratezza 0.93 (n=14), retrieval Precision@3 medio 0.80, relazioni F1 1.00 (gold set piccolo). Le soglie minime sono guardie di regressione. Output reali.

## Collegamento al progetto

Il passo 57 produce il report di valutazione del lab, baseline per le regressioni.

## Fonti

- scikit-learn, *Metrics and scoring* — <https://scikit-learn.org/stable/modules/model_evaluation.html>
