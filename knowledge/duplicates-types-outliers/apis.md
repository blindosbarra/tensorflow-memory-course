# APIs: duplicates-types-outliers

## pandas.DataFrame.duplicated

Uso previsto:

```python
frame.duplicated(subset=["memory_id"], keep="first")
```

Serve a marcare le righe successive alla prima con la stessa chiave.

## pandas.DataFrame.drop_duplicates

Uso previsto:

```python
frame.drop_duplicates(subset=["memory_id"], keep="first")
```

Nella lezione preferiamo costruire una maschera esplicita, per poter salvare nel
report quali righe sono state rimosse.

## pandas.to_numeric

Uso previsto:

```python
pd.to_numeric(series, errors="coerce")
```

Con `errors="coerce"`, i valori non convertibili diventano missing values. La
lezione li sostituisce con un fallback locale e aggiunge un flag.

## pandas.Series.clip

Uso previsto:

```python
series.clip(lower=0.0, upper=1.0)
```

Serve a limitare un punteggio al range di dominio dichiarato.
