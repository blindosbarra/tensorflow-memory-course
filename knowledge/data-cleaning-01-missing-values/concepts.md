# Concepts: missing values

Decisione research: `READY_FOR_WRITING`.
Aggiornato 2026-07-12 per il rework B4: il dominio didattico della lezione e'
la telemetria ambientale; il Memory AI Lab compare solo nel trasferimento.

## Concetti coperti

1. Il meccanismo di missingness orienta la strategia: Rubin (1976) distingue
   assenze indipendenti dai dati, dipendenti da valori osservati e dipendenti
   dal valore non osservato. Da una tabella piccola il meccanismo non e'
   identificabile con certezza: l'assunzione va documentata.
2. Un campo e' critico quando senza di esso la riga perde identita' o
   contesto (id, stazione, istante per una lettura). Una misura numerica
   assente puo' essere recuperabile, ma deve restare distinguibile.
3. La media e' sensibile agli estremi, la mediana e' resistente (NIST,
   Measures of Location). L'imputazione univariata con un valore centrale
   crea un picco artificiale e riduce la variabilita': e' una baseline, non
   una trasformazione neutra.
4. Un flag creato prima dell'imputazione conserva la provenienza del valore.
5. pandas distingue sentinelle come `NaN`, `NaT` e `NA` in base al dtype;
   la rilevazione usa `isna()`/`notna()`, non confronti di uguaglianza.

## Collegamento al Memory AI Lab

Il trasferimento e' motivato dal processo, non assunto: un timeout di
ingestion puo' perdere l'intero record; un'estrazione strutturata puo'
produrre `text` e `timestamp` ma omettere uno score derivato. Il mapping e'
id/testo/tempo come campi critici, score derivati come misure recuperabili.

## Limiti

La lezione introduce i meccanismi di Rubin come intuizione, senza test
statistici di identificabilita' ne' imputazione multivariata: temi per una
lezione successiva.
