# Examples: pmle-07-architetture-end-to-end

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). I tre scenari sono sviluppati
per esteso, con numeri costruiti, direttamente nella pagina della
lezione (`docs/modules/pmle-07-architetture-end-to-end.md`) invece che
in un file separato — la stessa scelta fatta per pmle-01..06 dopo il
feedback dello studente sui riferimenti a file non raggiungibili dal
sito pubblicato. Questo file esiste solo per coerenza di struttura del
knowledge pack (vedi gli altri knowledge pack del modulo).

Riepilogo dei tre scenari, per riferimento rapido:

1. **Previsione acquisto entro 30 giorni** (dati tabellari) —
   `BOOSTED_TREE_CLASSIFIER`, troubleshooting di overfitting con una
   tabella AUC training/validation per iterazione.
2. **Previsione pioggia per pianificare le consegne** (serie temporale
   con feature esterne) — confronto `ARIMA_PLUS` vs
   `BOOSTED_TREE_REGRESSOR` con feature di lag, troubleshooting di
   underfitting con una tabella MAE prima/dopo la correzione.
3. **Classificazione specie di fiori** (immagini, AutoML) —
   troubleshooting di sbilanciamento di classi con una matrice di
   confusione per classe, decisione edge vs cloud per il deploy.
