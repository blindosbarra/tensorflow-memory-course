---
id: data-cleaning-01-missing-values
title: Missing values nei dati di memoria
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [Python base, Tabelle CSV]
deliverables: [exercises/data-cleaning-01-missing-values_starter.py]
sources:
  - https://doi.org/10.1093/biomet/63.3.581
  - https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm
  - https://scikit-learn.org/stable/modules/impute.html
---

# Missing values nei dati di memoria

## Cosa saprai fare

Scegliere e implementare una strategia tracciabile per campi mancanti critici e
recuperabili, verificandone l'effetto sui dati.

## Perche' serve nel Memory AI Lab

Assenza di testo, tempo o score non significa la stessa cosa. La pulizia decide
quali memorie potranno raggiungere modelli e retrieval: e' una scelta sul
significato dei dati, non un passaggio cosmetico.

## Teoria essenziale

### Il meccanismo viene prima della tecnica

Rubin distingue processi in cui la probabilita' di assenza e' indipendente dai
dati, dipende da valori osservati, oppure dipende anche dal valore non
osservato. Questa distinzione conta: cancellare righe e imputare non eliminano
automaticamente il bias quando l'assenza e' informativa [Rubin, 1976]. Qui non
stimiamo il meccanismo da un piccolo CSV; dichiariamo invece le assunzioni.

Un campo e' **critico** quando senza di esso il record non soddisfa il contratto
del sistema. Nel lab, una memoria senza testo o timestamp non puo' supportare
retrieval testuale o temporale. Uno score ausiliario puo' essere imputato, purche'
la sostituzione resti visibile.

### Media o mediana

La media minimizza gli errori quadratici ma risente dei valori estremi. La
mediana divide le osservazioni ordinate ed e' piu' robusta in distribuzioni
asimmetriche [NIST, Measures of Location]. Nessuna delle due recupera
l'informazione mancante. Ripetere un valore centrale crea massa artificiale,
riduce spesso la variabilita' e puo' alterare relazioni tra colonne; scikit-learn
presenta l'imputazione univariata come baseline, non come ricostruzione neutra.

Per questo aggiungiamo un flag prima dell'imputazione: un modello futuro potra'
distinguere valori osservati e sostituiti.

## Dentro TensorFlow/Keras

Questa lezione non usa ancora TensorFlow. Prepara il contratto tabellare che
verra' convertito in `tf.data.Dataset` in `tfdata-basics`; TensorFlow arriva
dopo split, leakage, encoding e scaling, quando le decisioni sui dati sono gia'
esplicite.

## Esempio guidato

Sul piccolo dataset dimostrativo misuriamo, poi applichiamo una policy gia'
testata:

```python
import pandas as pd
from memory_ai.data_cleaning import clean_memory_records, missing_summary

raw = pd.read_csv("datasets/synthetic/memory_events_raw.csv")
print(missing_summary(raw))
result = clean_memory_records(raw)
print(result.report)
```

`isna` e `fillna` sono strumenti; la decisione e' aver definito campi critici,
statistica di imputazione e flag di audit.

## Prova tu

Prima di aprire la soluzione, implementa i TODO sul dataset challenge e fai
passare gli assert dedicati.

## Errori comuni

- Dedurre il meccanismo di missingness dalla sola cella vuota.
- Calcolare l'imputazione prima di separare futuri train e test.
- Usare la media su dati asimmetrici senza controllarne l'effetto.
- Eliminare flag e report dopo aver riempito i buchi.

## Riepilogo

- La causa dell'assenza orienta la strategia.
- Criticita' significa violazione del contratto del record.
- Media e mediana incorporano trade-off diversi.
- Imputare altera la distribuzione e non ricrea informazione.
- Un flag conserva la provenienza del valore.

## Quiz

1. Perche' contare i mancanti non basta a dimostrare che cancellare righe sia sicuro?
2. Quando preferiresti la mediana alla media per `importance`, e perche'?
3. Quale effetto distributivo puo' avere l'imputazione con un valore centrale?

Le risposte commentate sono in `solutions/data-cleaning-01-missing-values.md`.

## Esercizio

Completa `exercises/data-cleaning-01-missing-values_starter.py`; istruzioni e
test sono in `exercises/data-cleaning-01-missing-values.md`.

## Fonti

- Rubin (1976), *Inference and Missing Data*: meccanismi e ignorabilita'.
  https://doi.org/10.1093/biomet/63.3.581
- NIST/SEMATECH, *Measures of Location*: sensibilita' di media e mediana.
  https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm
- scikit-learn, *Imputation of missing values*: strategie semplici e indicatori.
  https://scikit-learn.org/stable/modules/impute.html
