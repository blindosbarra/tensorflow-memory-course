---
id: duplicates-types-outliers
title: Duplicati, tipi e outlier nei dati di memoria
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [data-cleaning-01-missing-values, Python base]
deliverables: [exercises/duplicates-types-outliers_starter.py]
sources:
  - https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
  - https://doi.org/10.1145/1008992.1009037
  - https://pandas.pydata.org/docs/user_guide/duplicates.html
---

# Duplicati, tipi e outlier nei dati di memoria

## Cosa saprai fare

Implementare un audit che separa candidati duplicati, errori di tipo e valori
fuori dominio senza nascondere le correzioni.

## Perche' serve nel Memory AI Lab

Record ripetuti sovrappesano eventi nel training e nel retrieval. Correzioni
silenziose cambiano la distribuzione degli score. Il lab deve poter spiegare
quali record sono stati confrontati e quali valori sono stati limitati.

## Teoria essenziale

### Identita' e near-duplicates

Un duplicato esatto dipende da una chiave dichiarata. Un **near-duplicate** puo'
differire per maiuscole, spazi o piccole variazioni pur riferendosi allo stesso
contenuto. Il record linkage confronta attributi imperfetti e comporta falsi
positivi e falsi negativi; non trasforma automaticamente la somiglianza in
identita' [Chaudhuri et al., 2003]. In questa lezione la normalizzazione genera
candidati conservativi: la cancellazione reale richiede anche contesto.

### Outlier statistico e di dominio

Un outlier statistico e' insolito rispetto a una distribuzione e dipende dal
metodo scelto; NIST mostra, per esempio, una regola basata su quartili e IQR. Un
outlier di dominio viola invece un contratto indipendente dalla frequenza: se
`importance` e' definita in `[0, 1]`, `1.2` e' invalido anche in un dataset
piccolo. Un valore raro ma valido non va corretto solo perche' sorprende.

Il **clipping** conserva la riga ma sposta i valori oltre soglia sul confine.
Questo crea accumuli a 0 o 1, cambia varianza e puo' cambiare correlazioni. Va
quindi applicato solo con un vincolo di dominio e con un flag, non come cura
generica degli outlier statistici.

## Dentro TensorFlow/Keras

TensorFlow non e' ancora usato. Questo audit prepara feature numeriche e record
univoci per `tfdata-basics`; le preprocessing layer non possono decidere se due
memorie rappresentino lo stesso evento.

## Esempio guidato

Il dataset dimostrativo mostra come ispezionare prima di correggere:

```python
import pandas as pd
from memory_ai.data_quality import duplicate_memory_mask, flag_and_clip_importance_outliers

raw = pd.read_csv("datasets/synthetic/memory_events_quality_issues.csv")
print(raw.loc[duplicate_memory_mask(raw)])
numeric = raw.assign(importance=pd.to_numeric(raw["importance"], errors="coerce"))
print(flag_and_clip_importance_outliers(numeric.fillna({"importance": 0.0})))
```

Le API sono confinate qui. Nell'esercizio dovrai progettare anche confronto
normalizzato e fallback basato sui dati validi.

## Prova tu

Completa lo starter sul challenge senza conoscere in anticipo numero o posizione
dei problemi; gli assert verificano contratto e audit flag.

## Errori comuni

- Usare una sola colonna non documentata come identita'.
- Cancellare automaticamente ogni near-duplicate.
- Chiamare invalido ogni valore raro.
- Applicare clipping senza misurare quanti valori finiscono sui confini.

## Riepilogo

- L'identita' dipende da chiavi e contesto.
- I near-duplicates sono candidati con errori possibili.
- Gli outlier statistici dipendono dalla distribuzione.
- Gli outlier di dominio violano un contratto.
- Il clipping modifica forma e variabilita'.
- Flag e report rendono le correzioni auditabili.

## Quiz

1. In cosa differiscono un outlier statistico e uno di dominio?
2. Perche' il clipping puo' alterare la distribuzione anche se conserva le righe?
3. Perche' il testo normalizzato deve proporre candidati e non provare identita'?

Le risposte commentate sono in `solutions/duplicates-types-outliers.md`.

## Esercizio

Completa `exercises/duplicates-types-outliers_starter.py`; istruzioni e test
sono in `exercises/duplicates-types-outliers.md`.

## Fonti

- NIST/SEMATECH, *Detection of Outliers*: criterio statistico IQR.
  https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
- Chaudhuri et al. (2003), *Robust and Efficient Fuzzy Match for Online Data Cleaning*:
  matching approssimato e trade-off. https://doi.org/10.1145/1008992.1009037
- pandas, *Duplicate Labels*: comportamento delle etichette duplicate.
  https://pandas.pydata.org/docs/user_guide/duplicates.html
