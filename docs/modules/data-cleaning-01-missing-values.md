---
id: data-cleaning-01-missing-values
title: Missing values nelle letture ambientali
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [Python base, Tabelle CSV]
deliverables: [notebooks/data-cleaning-01-missing-values.ipynb]
sources:
  - https://doi.org/10.1093/biomet/63.3.581
  - https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm
  - https://scikit-learn.org/stable/modules/impute.html
---

# Missing values nelle letture ambientali

> **La lezione si segue nel notebook** `notebooks/data-cleaning-01-missing-values.ipynb`:
> teoria, esempi eseguibili, esercizio con soluzione spiegata e il primo passo
> del progetto Memory AI Lab, tutto in un unico posto. Questa pagina e' il
> riassunto di riferimento.

## Cosa saprai fare

Scegliere e implementare una policy tracciabile per letture mancanti,
verificandone l'effetto sulla distribuzione.

## Il problema nel suo dominio naturale

Una stazione ambientale registra temperatura e umidita' ogni ora. Un sensore
puo' non rispondere, la rete puo' perdere un pacchetto o la stazione puo' essere
offline. Il buco nasce quindi dal processo di misura. Prima di riempirlo devi
chiederti quale causa lo ha prodotto e quale decisione analitica vuoi sostenere.

## Teoria essenziale

### La causa viene prima della tecnica

Rubin distingue assenze indipendenti dai dati, dipendenti da valori osservati e
dipendenti anche dal valore non osservato. Se un termometro smette di rispondere
proprio alle temperature estreme, le righe visibili non sono un campione neutro:
cancellare o imputare non rimuove automaticamente il bias [Rubin, 1976]. Da un
CSV piccolo non puoi identificare con certezza il meccanismo; devi documentare
le informazioni sul processo e l'assunzione adottata.

Un campo e' **critico** quando senza di esso la riga perde identita' o contesto:
per una lettura servono id, stazione e istante. Una misura numerica assente puo'
essere recuperabile, ma la sostituzione deve restare distinguibile dall'originale.

### Media, mediana ed effetto dell'imputazione

La media usa tutte le distanze e risente degli estremi; la mediana e' resistente
a pochi valori molto lontani [NIST, Measures of Location]. Nessuna delle due
ricrea la misura persa. Inserire ripetutamente un valore centrale crea un picco
artificiale, tende a ridurre la variabilita' e puo' cambiare le relazioni tra
colonne. L'imputazione univariata e' una baseline, non una trasformazione neutra
[scikit-learn, Imputation]. Un flag creato prima dell'imputazione conserva la
provenienza del valore.

## Dentro TensorFlow/Keras

Questa lezione non usa TensorFlow. Prepara il contratto tabellare che verra'
convertito in `tf.data.Dataset` in `tfdata-basics`; TensorFlow arriva dopo split,
leakage, encoding e scaling, quando le decisioni sui dati sono esplicite.

## Esempio guidato

Su quattro letture dimostrative misuriamo l'assenza e confrontiamo statistiche:

```python
import pandas as pd

demo = pd.DataFrame({"temperature_c": [18.2, 18.7, None, 41.0]})
missing_rate = demo.isna().mean()
mean_value = demo["temperature_c"].mean()
median_value = demo["temperature_c"].median()
demo["temperature_was_missing"] = demo["temperature_c"].isna()
demo["temperature_c"] = demo["temperature_c"].fillna(median_value)
```

`isna` e `fillna` sono strumenti. La decisione e' usare una statistica coerente
con la forma osservata, conservare il flag e dichiarare che non conosciamo la
misura originale.

## Prova tu

Apri il notebook della lezione: nella Parte 3 trovi la cella "Prova tu" con
l'esercizio sul dataset dei sensori, e subito sotto la soluzione spiegata
riga per riga. Nella Parte 4 applichi la stessa policy al progetto del corso.

## Errori comuni

- Dedurre il meccanismo di missingness dalla sola cella vuota.
- Calcolare l'imputazione prima di separare futuri train e test.
- Usare la media su dati asimmetrici senza misurarne l'effetto.
- Eliminare flag e report dopo aver riempito i buchi.

## Riepilogo

- La causa dell'assenza orienta la strategia.
- I campi critici definiscono l'identita' della lettura.
- Media e mediana hanno sensibilita' diverse agli estremi.
- L'imputazione modifica la distribuzione.
- Un flag distingue valori osservati e sostituiti.

## Quiz

1. Una stazione perde soprattutto misure durante picchi di calore. Perche'
   cancellare le righe puo' distorcere l'analisi?
2. Quale controllo faresti prima di scegliere media o mediana?
3. Perche' il flag di imputazione va creato prima di `fillna`?

Le risposte commentate sono in `solutions/data-cleaning-01-missing-values.md`.

## Esercizio

L'esercizio e la sua soluzione spiegata sono nel notebook della lezione
(Parte 3). Non servono terminale ne' strumenti aggiuntivi.

## Trasferimento al Memory AI Lab

Nella pipeline finale un timeout di ingestion puo' perdere l'intero record;
un'estrazione strutturata puo' invece produrre `text` e `timestamp` ma omettere
`importance`. Il mapping e': id/testo/tempo identificano e rendono recuperabile
la memoria, come id/stazione/tempo per la lettura; uno score derivato e' una
misura recuperabile, come temperatura o umidita'. La policy non assume memorie
difettose per natura: collega il difetto a ingestion ed estrazione parziale.

## Fonti

- Rubin (1976), *Inference and Missing Data*: meccanismi e ignorabilita'.
  https://doi.org/10.1093/biomet/63.3.581
- NIST/SEMATECH, *Measures of Location*: sensibilita' di media e mediana.
  https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm
- scikit-learn, *Imputation of missing values*: baseline e indicatori.
  https://scikit-learn.org/stable/modules/impute.html
