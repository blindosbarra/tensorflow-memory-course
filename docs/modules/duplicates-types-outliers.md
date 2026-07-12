---
id: duplicates-types-outliers
title: Duplicati, tipi e outlier nelle letture ambientali
module: data-engineering
status: learner_review
estimated_minutes: 30
prerequisites: [data-cleaning-01-missing-values, Python base]
deliverables: [notebooks/lezione-02-duplicati-tipi-outlier.ipynb]
sources:
  - https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
  - https://doi.org/10.1145/872757.872796
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html
---

# Duplicati, tipi e outlier nelle letture ambientali

> **La lezione si segue nel notebook** `notebooks/lezione-02-duplicati-tipi-outlier.ipynb`:
> teoria, esempi eseguibili, esercizio con soluzione spiegata e il secondo passo
> del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.
> Prerequisito: aver eseguito il notebook della Lezione 1.

## Cosa saprai fare

Implementare un audit che separa candidati duplicati, errori di tipo e misure
fuori dominio senza nascondere le correzioni.

## Il problema nel suo dominio naturale

Una stazione ritenta l'invio dopo un timeout: il collector puo' ricevere due
volte la stessa lettura. Firmware diversi possono inviare `18.4` oppure
`"18.4"`; un sensore guasto puo' produrre una temperatura fisicamente
impossibile. Sono difetti naturali di una pipeline di telemetria.

## Teoria essenziale

### Identita' e near-duplicates

Un duplicato esatto dipende da una chiave dichiarata. Un near-duplicate puo'
differire per spazi o maiuscole pur descrivendo la stessa stazione e lo stesso
istante. Il record linkage bilancia falsi match e match mancati: la somiglianza
propone candidati, non dimostra identita' [Chaudhuri et al., 2003]. Per questo
normalizziamo etichette, ma conserviamo tempo e regole di dominio nel confronto.

### Outlier statistico e di dominio

Un outlier statistico e' insolito rispetto alla distribuzione e dipende da una
regola dichiarata, per esempio quartili e IQR [NIST, Detection of Outliers]. Un
outlier di dominio viola invece un contratto esterno: se la stazione e'
certificata da -50 a 60 gradi, 79 e' invalido anche se compare spesso. Un valore
raro ma nel range non va corretto solo perche' sorprende.

Il clipping conserva la riga ma accumula i valori oltre soglia sul confine.
Cambia forma, varianza e potenzialmente correlazioni. Si applica soltanto con un
vincolo motivato e un flag di audit; non e' una cura generica per gli outlier.

## Dentro TensorFlow/Keras

TensorFlow non e' ancora usato. Questo audit prepara feature numeriche e record
univoci per `tfdata-basics`; una preprocessing layer non puo' decidere se due
letture rappresentano la stessa misura fisica.

## Esempio guidato

```python
import pandas as pd

demo = pd.DataFrame({
    "station_id": ["north", "north", "south"],
    "recorded_at": ["10:00", "10:00", "10:00"],
    "temperature_c": [18.4, "18.4", "sensor_error"],
})
duplicate = demo.duplicated(["station_id", "recorded_at"], keep="first")
numeric = pd.to_numeric(demo["temperature_c"], errors="coerce")
```

Le API rendono visibile l'audit. Non stabiliscono da sole la chiave corretta,
il range fisico o la policy per i parse falliti.

## Prova tu

Apri il notebook della lezione: nella Parte 3 trovi la cella "Prova tu" con
l'audit completo del dataset dei sensori, e subito sotto la soluzione
spiegata. Nella Parte 4 il progetto riceve un nuovo batch di memorie.

## Errori comuni

- Usare una sola colonna non documentata come identita'.
- Cancellare automaticamente ogni near-duplicate.
- Chiamare invalido ogni valore raro.
- Applicare clipping senza misurare l'accumulo sui confini.

## Riepilogo

- L'identita' dipende da chiavi e contesto.
- I near-duplicates sono candidati, non prove.
- Gli outlier statistici dipendono dalla distribuzione.
- Gli outlier di dominio violano un contratto.
- Il clipping modifica forma e variabilita'.
- Flag e report rendono le correzioni auditabili.

## Quiz

1. Una temperatura rara ma nel range certificato e' necessariamente invalida?
2. Perche' normalizzare `station_id` senza confrontare l'istante puo' produrre
   falsi duplicati?
3. Quale traccia serve per valutare l'effetto del clipping?

Le risposte commentate sono in `solutions/duplicates-types-outliers.md`.

## Esercizio

L'esercizio e la sua soluzione spiegata sono nel notebook della lezione
(Parte 3). Problemi, quantita' e posizioni non sono anticipati.

## Trasferimento al Memory AI Lab

I retry di ingestion possono duplicare una memoria; estrattori diversi possono
variare spazi o maiuscole; un parser puo' restituire testo invece di un numero.
Il mapping e': `reading_id` diventa `memory_id`, stazione+istante diventa una
chiave candidata evento+tempo, il range fisico diventa il contratto dello score.
Il clipping di `importance` ha senso solo dopo che quel contratto e' definito:
non assumiamo che una memoria nasca con uno score invalido.

## Fonti

- NIST/SEMATECH, *Detection of Outliers*: criterio statistico IQR.
  https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
- Chaudhuri et al. (2003), *Robust and Efficient Fuzzy Match for Online Data
  Cleaning*: trade-off del matching. https://doi.org/10.1145/872757.872796
- pandas, `DataFrame.duplicated`: subset e keep policy.
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html
