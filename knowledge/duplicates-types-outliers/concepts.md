# Concepts: duplicates-types-outliers

## Scope didattico

La lezione introduce tre controlli di qualita' prima dei modelli:

1. duplicati;
2. tipi errati;
3. outlier di dominio.

Non introduce TensorFlow. Non introduce split train/test. Non usa dati reali.

## Duplicati

Un duplicato e' una riga che rischia di contare due volte lo stesso evento.

Nel Memory AI Lab usiamo due regole conservative:

- stesso `memory_id`: duplicato forte;
- stessa coppia `text` e `timestamp`: possibile duplicato semantico semplice.

La regola conserva la prima occorrenza e registra quante righe rimuove.

## Tipi errati

Un CSV contiene testo. Alcune colonne devono pero' diventare numeriche prima di
essere usate come feature o metriche.

Per `importance` la conversione deve essere esplicita:

- valori come `"0.72"` diventano numeri;
- valori come `"high"` non sono numeri e vanno segnalati.

## Outlier di dominio

In questa lezione `importance` e' definita localmente come punteggio tra `0` e
`1`. Un valore minore di `0` o maggiore di `1` non e' solo "strano": viola la
regola del campo.

La lezione usa una correzione semplice e tracciabile:

- valori sotto `0` vengono portati a `0`;
- valori sopra `1` vengono portati a `1`;
- ogni correzione lascia un flag.

## Collegamento al Memory AI Lab

Un sistema di memoria deve evitare che la stessa memoria pesi due volte. Deve
anche sapere se un punteggio di importanza e' davvero numerico e dentro il range
atteso.
