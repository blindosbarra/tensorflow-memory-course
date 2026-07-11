# Soluzione commentata: duplicati, tipi e outlier

L'implementazione completa del challenge sui sensori e' in
`solutions/duplicates-types-outliers_starter.py`. La normalizzazione propone
candidati: una cancellazione reale richiede ancora la chiave di dominio.

## Risposte al quiz

1. No. E' un outlier statistico possibile, ma non viola il contratto di
   dominio. Va investigato, non corretto automaticamente.
2. La stessa stazione produce molte letture valide. Senza l'istante, tutte
   diventerebbero falsi duplicati; identita' e' una decisione sulla chiave.
3. Serve almeno un flag per i valori modificati e il conteggio dei valori
   spostati su ciascun confine. Confrontare distribuzione e variabilita' prima e
   dopo rende osservabile l'effetto.
