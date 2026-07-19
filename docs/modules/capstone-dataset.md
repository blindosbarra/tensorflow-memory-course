---
id: capstone-dataset
title: Il dataset del capstone
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-architecture, train-validation-test]
deliverables: [notebooks/lezione-53-capstone-dataset.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/cross_validation.html
---

# Il dataset del capstone

> **La lezione si segue nel notebook**
> `notebooks/lezione-53-capstone-dataset.ipynb`: teoria, codice eseguibile, esercizio e il 53esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Caricare, validare e preparare il dataset di memorie che alimenta l'intero lab, riusando lo schema della Lezione 22.

## Teoria essenziale

Un sistema vale quanto i suoi dati: split train/val/test (Lezione 3), validazione contro lo schema (Lezione 22), pulizia dei casi inutilizzabili (`type=unknown`), e un report di qualita'.

## Cosa mostra il notebook

Sui dati reali: train/val/test = 212/19/14 righe dopo la pulizia (scartata 1 riga con `type` non valido), importanza riportata in [0,1], e un `assert` conferma l'assenza di leakage (nessun id di test nel train).

## Collegamento al progetto

Il passo 53 produce il dataset pulito e validato, pronto per tutti i componenti.

## Fonti

- scikit-learn, *Cross-validation* — <https://scikit-learn.org/stable/modules/cross_validation.html>
