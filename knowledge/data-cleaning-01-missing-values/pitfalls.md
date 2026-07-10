# Pitfalls: missing values

- Non usare `== np.nan` o `== pd.NA` per rilevare missing value: usare `isna()`.
- Non imputare senza registrare cosa e' stato imputato.
- Non scartare righe prima di sapere quante informazioni si stanno perdendo.
- Non calcolare statistiche di imputazione sul test set in una pipeline di
  machine learning.
- Non trattare campi critici e feature ausiliarie nello stesso modo.
