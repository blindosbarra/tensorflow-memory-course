---
id: duplicates-types-outliers
title: Duplicati, tipi e outlier nei dati di memoria
module: data-engineering
status: learner_review
estimated_minutes: 25
prerequisites:
  - data-cleaning-01-missing-values
  - Python base
  - File CSV
deliverables:
  - datasets/processed/memory_events_quality_clean.csv
  - reports/evaluation/duplicates-types-outliers.json
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html
  - https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
  - https://pandas.pydata.org/docs/reference/api/pandas.Series.clip.html
---

# Duplicati, tipi e outlier nei dati di memoria

## Il problema

Nella lezione precedente hai visto i valori mancanti. Ora guardi altri tre
problemi piccoli ma frequenti.

| memory_id | text | timestamp | type | importance |
|---|---|---|---|---|
| mem_001 | Marco visited Glasgow with his son. | 2026-07-03 | episodic | 0.72 |
| mem_001 | Marco visited Glasgow with his son. | 2026-07-03 | episodic | 0.72 |
| mem_003 | The user likes walking meetings. | 2026-07-05 | preference | high |
| mem_004 | A trip lasted 400 days. | 2026-07-06 | episodic | 1.70 |

La seconda riga ripete la prima. Il valore `high` sembra informativo, ma non e'
un numero. Il valore `1.70` e' numerico, ma non rispetta la regola locale:
`importance` deve stare tra `0` e `1`.

Questa lezione ha un obiettivo pratico: **pulire questi problemi senza
nascondere cosa e' stato cambiato**.

## Cosa impari

Alla fine saprai fare tre cose:

1. trovare duplicati con una chiave esplicita;
2. convertire un campo numerico letto come testo;
3. segnalare e correggere outlier di dominio.

## Perche' serve nel Memory AI Lab

Un sistema di memoria usa i record per decidere cosa salvare, cercare e valutare.
Se una memoria appare due volte, puo' pesare troppo. Se `importance` e' testo,
non puoi confrontarla con altri punteggi. Se `importance` esce dal range
previsto, le regole successive diventano ambigue.

Qui non stai ancora addestrando un modello. Stai proteggendo i dati che un
modello usera' piu' avanti.

## Concetto 1: duplicati

Un duplicato non e' sempre "una riga identica". Dipende dalla chiave che scegli.

In questa lezione usiamo due controlli:

- stesso `memory_id`;
- stessa coppia `text` e `timestamp`.

Il primo caso e' forte: due righe con lo stesso identificatore dicono di essere
la stessa memoria. Il secondo caso e' una regola semplice: stesso testo nello
stesso giorno probabilmente descrive lo stesso evento.

Il codice conserva la prima riga e marca le successive:

```python
from memory_ai.data_quality import duplicate_memory_mask

duplicate_mask = duplicate_memory_mask(raw)
duplicates = raw.loc[duplicate_mask]
```

La maschera non cancella nulla. Prima ti fa vedere cosa verrebbe rimosso.

## Concetto 2: tipi errati

Un CSV e' testo. Anche quando vedi `0.40`, pandas puo' leggerlo insieme ad altri
valori come una colonna non numerica, soprattutto se nella stessa colonna appare
`high`.

Per questo la conversione deve essere esplicita:

```python
import pandas as pd

numeric_importance = pd.to_numeric(raw["importance"], errors="coerce")
```

Con `errors="coerce"`, i valori non convertibili diventano mancanti. Nel nostro
codice non li lasciamo sparire: aggiungiamo il flag
`importance_was_invalid_type` e usiamo un fallback conservativo.

## Concetto 3: outlier di dominio

Qui "outlier" non significa "valore raro". Significa "valore impossibile per la
regola del campo".

Nel repository `importance` e' un punteggio locale tra `0.0` e `1.0`. Quindi:

- `-0.20` viola il limite inferiore;
- `1.70` viola il limite superiore;
- `0.72` e' nel range.

La funzione della lezione fa due cose:

- aggiunge `importance_was_outlier`;
- porta il valore dentro il range con `clip`.

Questo e' semplice, ma non e' neutro. Per questo il report deve dire quanti
valori sono stati corretti.

## Il dataset della lezione

Userai:

```text
datasets/synthetic/memory_events_quality_issues.csv
```

Il file e' sintetico. Contiene solo sette righe e tre problemi intenzionali:

- duplicati;
- `importance` non numerica;
- `importance` fuori range.

## Esempio guidato

Dal terminale, nella root del repository:

```bash
uv run python examples/duplicates_types_outliers.py
```

Il comando crea:

```text
datasets/processed/memory_events_quality_clean.csv
reports/evaluation/duplicates-types-outliers.json
```

Il codice principale e':

```python
from pathlib import Path

import pandas as pd

from memory_ai.data_quality import clean_memory_quality_issues

raw_path = Path("datasets/synthetic/memory_events_quality_issues.csv")
raw = pd.read_csv(raw_path)

result = clean_memory_quality_issues(raw)
cleaned = result.data
report = result.report
```

`cleaned` contiene la tabella pulita. `report` contiene le decisioni:

- quante righe sono entrate;
- quante sono uscite;
- quanti duplicati sono stati rimossi;
- quanti valori di `importance` non erano numerici;
- quanti valori erano fuori range.

## Notebook

Puoi eseguire gli stessi passaggi in:

```text
notebooks/duplicates-types-outliers.ipynb
```

Il notebook include assert finali. Se una regola cambia senza essere aggiornata,
il notebook fallisce.

## Cosa deve restare chiaro

La pulizia non deve far sembrare i dati migliori di quanto siano. Il punto non e'
solo ottenere una tabella "ordinata". Il punto e' poter dire:

> ho rimosso questi duplicati, ho convertito questi valori e ho corretto questi
> outlier perche' violavano una regola dichiarata.

Nel Memory AI Lab questa tracciabilita' evita decisioni nascoste prima dei
modelli.

## Errori comuni

- Cercare duplicati senza decidere la chiave.
- Usare `astype(float)` prima di controllare valori come `high`.
- Correggere outlier senza lasciare un flag.
- Chiamare outlier un valore solo perche' sembra grande.
- Cancellare righe recuperabili senza salvare un report.

## Riepilogo

- Un duplicato dipende dalla chiave scelta.
- Qui controlli `memory_id` e la coppia `text`/`timestamp`.
- Un CSV puo' contenere numeri letti come testo.
- `pd.to_numeric(..., errors="coerce")` rende espliciti i valori non convertibili.
- In questa lezione `importance` deve stare tra `0.0` e `1.0`.
- Gli outlier di dominio vengono segnalati e portati nel range.
- Ogni modifica importante deve apparire nel report.

## Quiz

1. Perche' due righe con lo stesso `memory_id` sono piu' sospette di due righe
   con lo stesso `type`?
2. Cosa rischi usando `astype(float)` su una colonna che contiene `"high"`?
3. Nel Memory AI Lab, perche' e' utile sapere che `importance` e' stata corretta?

## Esercizio

Vai a `exercises/duplicates-types-outliers.md`.

## Fonti

- pandas, `DataFrame.duplicated`:
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html
- pandas, `to_numeric`:
  https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
- pandas, `Series.clip`:
  https://pandas.pydata.org/docs/reference/api/pandas.Series.clip.html
