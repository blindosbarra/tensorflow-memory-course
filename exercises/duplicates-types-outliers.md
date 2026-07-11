# Esercizio: trova duplicati, tipi errati e outlier

Userai questo file:

```text
datasets/synthetic/memory_events_quality_issues.csv
```

## Parte 1: guarda la tabella

Apri Python o una cella notebook:

```python
import pandas as pd

raw = pd.read_csv("datasets/synthetic/memory_events_quality_issues.csv")
print(raw)
```

Domande:

- quali righe sembrano ripetute?
- quali valori di `importance` non sembrano numeri?
- quali valori di `importance` sono fuori dal range `0`-`1`?

## Parte 2: trova i duplicati

Usa la funzione gia' pronta:

```python
from memory_ai.data_quality import duplicate_memory_mask

duplicate_mask = duplicate_memory_mask(raw)
print(raw.loc[duplicate_mask])
```

Domanda:

- perche' una riga puo' essere duplicata anche se ha un `memory_id` diverso?

## Parte 3: pulisci e leggi il report

```python
from memory_ai.data_quality import clean_memory_quality_issues

result = clean_memory_quality_issues(raw)

print(result.data)
print(result.report)
```

## Criteri di successo

Hai completato l'esercizio se riesci a spiegare:

- quanti duplicati sono stati rimossi;
- cosa e' successo al valore `"high"`;
- cosa e' successo ai valori `1.70` e `-0.20`;
- perche' i flag sono utili;
- perche' la soluzione non introduce TensorFlow.

## Controllo automatico

Quando vuoi verificare che il codice del repository funzioni:

```bash
uv run pytest
```

## Hint

1. Un duplicato dipende dalla chiave scelta.
2. `to_numeric` serve a convertire testo in numeri.
3. Un valore non convertibile non e' uguale a un outlier.
4. Qui un outlier e' un valore fuori dal range dichiarato per `importance`.
