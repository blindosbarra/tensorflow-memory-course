---
id: capstone-monitoring
title: Monitoraggio e drift
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-pipeline, online-learning-risks]
deliverables: [notebooks/lezione-59-capstone-monitoring.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/model_evaluation.html
---

# Monitoraggio e drift

> **La lezione si segue nel notebook**
> `notebooks/lezione-59-capstone-monitoring.ipynb`: teoria, codice eseguibile, esercizio e il 59esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Monitorare il drift dei dati in ingresso e far scattare un allarme, in NumPy.

## Teoria essenziale

Un modello in produzione non e' 'finito': il **drift** e' lo spostamento della distribuzione in ingresso rispetto al riferimento (il train). Il **PSI** lo misura; convenzione: <0.1 stabile, 0.1-0.25 moderato, >0.25 forte.

## Cosa mostra il notebook

Riferimento = distribuzione dei tipi nel train. Un batch simile ha PSI 0.038 (OK); un batch con drift (quasi solo preferenze) ha PSI 6.779 (ALLARME). Un `assert` verifica che l'allarme scatti solo sul secondo. Output reali.

## Collegamento al progetto

Il passo 59 aggiunge `monitor(batch)`: oltre soglia si raccoglie nuovo feedback (Fase 7) e si ri-tarano i componenti.

## Fonti

- scikit-learn, *Metrics and scoring* — <https://scikit-learn.org/stable/modules/model_evaluation.html>
