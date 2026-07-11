# Soluzione commentata: duplicati, tipi e outlier

L'implementazione completa del challenge e' in
`solutions/duplicates-types-outliers_starter.py`. Normalizza il testo soltanto
per proporre candidati: in un sistema reale i near-duplicates richiedono review
o regole di dominio prima della cancellazione.

## Risposte al quiz

1. **Un outlier statistico e' insolito rispetto ai dati; uno di dominio viola un
   vincolo dichiarato.** Un valore raro puo' essere valido, mentre `1.4` non e'
   valido per uno score definito in `[0, 1]`.
2. **Il clipping accumula osservazioni sui confini.** Conserva il numero di
   righe, ma altera forma, varianza e relazioni; per questo serve un flag.
3. **La normalizzazione genera candidati, non identita' certa.** Maiuscole e
   spazi possono essere irrilevanti, ma due testi simili possono descrivere
   eventi distinti; timestamp e regole di dominio riducono i falsi positivi.
