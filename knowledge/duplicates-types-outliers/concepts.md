# Concepts: duplicates-types-outliers

Decisione research: `READY_FOR_WRITING`.
Aggiornato 2026-07-12 per il rework B4: il dominio didattico della lezione e'
la telemetria ambientale; il Memory AI Lab compare solo nel trasferimento.

## Scope didattico

La lezione introduce tre controlli di qualita' prima dei modelli, su letture
di sensori dove i difetti nascono naturalmente (retry di rete, firmware
diversi, sensori guasti):

1. duplicati esatti e near-duplicates;
2. tipi errati (numeri arrivati come testo);
3. outlier statistici vs outlier di dominio.

Non introduce TensorFlow. Non introduce split train/test. Non usa dati reali.

## Duplicati e near-duplicates

Un duplicato esatto dipende da una chiave dichiarata (stesso `reading_id`;
stessa coppia stazione+istante). Un near-duplicate differisce per dettagli di
rappresentazione (spazi, maiuscole) pur descrivendo lo stesso evento. Il
record linkage bilancia falsi match e match mancati (Chaudhuri et al., 2003):
la normalizzazione propone candidati, non dimostra identita'. Si conserva la
prima occorrenza e si registra quante righe escono.

## Tipi errati

Un CSV contiene testo: la conversione numerica deve essere esplicita con
`to_numeric(errors="coerce")`, e i parse falliti vanno flaggati, non fatti
sparire nel fallback.

## Outlier statistici e di dominio

Un outlier statistico e' insolito rispetto alla distribuzione secondo una
regola dichiarata, per esempio quartili e IQR (NIST, Detection of Outliers).
Un outlier di dominio viola un contratto esterno (range certificato della
stazione, `[-50, 60]` gradi). Un valore raro ma nel range non va corretto.
Il clipping conserva la riga ma accumula massa sui confini e cambia forma e
varianza: si applica solo con un vincolo motivato e un flag di audit.

## Collegamento al Memory AI Lab

I retry di ingestion possono duplicare una memoria; estrattori diversi
variano la rappresentazione; un parser puo' restituire testo al posto di un
numero. Il contratto dello score `importance` (0.0-1.0) gioca il ruolo del
range certificato della stazione.
