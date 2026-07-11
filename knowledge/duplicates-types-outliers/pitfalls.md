# Pitfalls: duplicates-types-outliers

- Rimuovere duplicati senza sapere quale chiave e' stata usata.
- Confondere un numero scritto come testo con un numero gia' pronto.
- Usare `astype(float)` su valori non puliti: un singolo valore come `"high"`
  puo' fermare tutto.
- Chiamare outlier qualunque valore raro senza spiegare la regola.
- Correggere outlier senza salvare un flag.
- Cancellare record con `importance` errata quando basta segnalarli e usare una
  regola conservativa.
