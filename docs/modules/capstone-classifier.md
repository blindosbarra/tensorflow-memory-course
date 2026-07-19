---
id: capstone-classifier
title: Il classificatore del tipo di memoria
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-dataset, tokenization-vocabulary]
deliverables: [notebooks/lezione-54-capstone-classificatore.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/linear_model.html
---

# Il classificatore del tipo di memoria

> **La lezione si segue nel notebook**
> `notebooks/lezione-54-capstone-classificatore.ipynb`: teoria, codice eseguibile, esercizio e il 54esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Addestrare in NumPy un classificatore bag-of-words + regressione softmax per il tipo di memoria.

## Teoria essenziale

Bag of words con vocabolario **solo dal train** (no leakage) e regressione softmax (Lezione 9) addestrata a mano; baseline onesta = la classe di maggioranza.

## Cosa mostra il notebook

Vocabolario di 64 parole (solo train); il classificatore batte nettamente la baseline di maggioranza (0.68 sul val) raggiungendo alta accuratezza di validazione. Nota di onesta': il val set e' piccolo (19 righe), quindi un'accuratezza molto alta non va sovra-interpretata — il segnale lessicale (prefers/likes -> preference, nomi+luoghi -> episodic, fatti -> semantic) e' pero' genuinamente forte.

## Collegamento al progetto

Il passo 54 fornisce `classifica_tipo`, il primo componente reale della pipeline.

## Fonti

- scikit-learn, *Logistic regression* — <https://scikit-learn.org/stable/modules/linear_model.html>
