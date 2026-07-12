---
id: data-leakage
title: Data leakage
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [train-validation-test]
deliverables: [notebooks/lezione-04-data-leakage.ipynb]
sources:
  - https://scikit-learn.org/stable/common_pitfalls.html
  - https://scikit-learn.org/stable/modules/compose.html
---

# Data leakage

> **La lezione si segue nel notebook** `notebooks/lezione-04-data-leakage.ipynb`:
> teoria, dimostrazioni numeriche del danno, esercizio con soluzione
> spiegata e il quarto passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 3.

## Cosa saprai fare

Riconoscere le tre forme principali di leakage in qualunque pipeline e
sapere dove guardare quando un risultato sembra troppo bello.

## Teoria essenziale

Il leakage e' informazione **non disponibile in produzione** che entra
nell'addestramento: metriche eccellenti offline, fallimento reale. Non da'
sintomi: la pipeline gira e i numeri salgono.

Le tre forme: **target leakage** (una feature deriva dalla risposta, come
"giorni dalla cancellazione" per predire la cancellazione);
**contaminazione train/test** (duplicati o near-duplicates distribuiti tra
gli insiemi: il modello riconosce righe gia' viste); **leakage da
preprocessing** (statistiche calcolate su tutti i dati prima della
divisione).

La regola d'oro: prima dividi; poi ogni statistica (`fit`) si calcola solo
sul train e si applica (`transform`) agli altri insiemi.

## Nel progetto

Audit anti-leakage degli split della Lezione 3: nessun `memory_id`
condiviso, near-duplicates testuali rimossi da validation e test (restano
nel train: gli strumenti di misura devono restare puliti), statistiche di
imputazione ricavate dal solo train.

## Errori comuni

- Festeggiare un'accuratezza sospettosamente alta invece di indagarla.
- Deduplicare dentro i singoli insiemi invece che prima della divisione.
- Imputare o scalare sull'intero dataset e poi dividere.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, *Common pitfalls: data leakage*:
  https://scikit-learn.org/stable/common_pitfalls.html
- scikit-learn, *Pipelines and composite estimators*:
  https://scikit-learn.org/stable/modules/compose.html
