---
id: categorical-encoding-scaling
title: Encoding e scaling
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [data-leakage]
deliverables: [notebooks/lezione-05-encoding-scaling.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/preprocessing.html
  - https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
---

# Encoding e scaling

> **La lezione si segue nel notebook** `notebooks/lezione-05-encoding-scaling.ipynb`:
> teoria, dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> quinto passo del progetto Memory AI Lab (la prima matrice di feature).
> Questa pagina e' il riassunto di riferimento. Prerequisito: Lezione 4.

## Cosa saprai fare

Trasformare una tabella mista (testi, categorie, numeri su scale diverse)
in input numerici corretti per un modello, senza ordini fittizi ne' leakage.

## Teoria essenziale

I modelli calcolano: le categorie vanno codificate. L'**encoding ordinale**
inventa un ordine e delle distanze tra categorie, accettabile solo per
categorie realmente ordinate; il **one-hot** crea una colonna binaria per
categoria, senza ordini fittizi ma con un costo in dimensionalita' (per
cardinalita' alte si usano gli embedding, tema della Fase 3). Il **target**
si mappa a interi: non e' una feature.

Le **scale** distorcono distanze e gradienti: una feature con valori grandi
domina i calcoli per un incidente di unita' di misura. Standardizzazione
(media 0, deviazione 1) come default; min-max quando serve un range chiuso.
Ogni statistica viene dal solo train; l'encoding del test si riallinea al
vocabolario del train (`reindex(..., fill_value=0)`).

## Nel progetto

Dagli insiemi auditati nascono `memory_features_{train,val,test}.csv`:
lunghezza del testo, numero di parole, `importance` e i flag di audit come
feature standardizzate; `type` mappato a interi come target. La fase dati
del progetto e' completa: la Fase 2 trasforma questa matrice in tensori.

## Errori comuni

- Encoding ordinale su categorie senza ordine.
- Colonne one-hot diverse tra train e test.
- Scalare con statistiche calcolate su tutti i dati.
- Buttare i flag di audit invece di usarli come feature.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, *Preprocessing data*:
  https://scikit-learn.org/stable/modules/preprocessing.html
- pandas, `get_dummies`:
  https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
