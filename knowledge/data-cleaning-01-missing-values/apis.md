# APIs: missing values

## pandas

- `DataFrame.isna()` rileva valori mancanti in modo coerente tra sentinelle
  diverse.
- `DataFrame.notna()` e' utile per costruire maschere di righe complete.
- `DataFrame.convert_dtypes()` aiuta a usare dtype nullable quando possibile.

## scikit-learn

- `sklearn.impute.SimpleImputer` fornisce strategie semplici: `mean`, `median`,
  `most_frequent` e `constant`.
- L'imputer deve essere addestrato sui dati ammessi alla fase di trasformazione.
  In una pipeline reale, il fit va fatto solo sul training set.

## TensorFlow/Keras

- Il tutorial TensorFlow sui dati strutturati mostra un flusso in cui le feature
  tabellari vengono convertite in tensori e preprocessate prima del modello.
  Questa lezione prepara i record tabellari prima di quel passaggio.
