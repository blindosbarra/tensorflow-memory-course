---
id: <lesson-id>
title: <title>
module: <module-id>
status: draft
estimated_minutes: 25
prerequisites: []
deliverables: []
sources: []
---

# <Titolo>

## Cosa saprai fare

Un solo risultato pratico, osservabile e verificabile.

## Il problema nel suo dominio naturale

Parti sempre da un caso generico e realistico in cui il difetto nasce senza
forzature: sensori, log applicativi, form o un dominio equivalente. Teoria,
esempio guidato ed esercizio restano su questo dominio. Non introdurre qui il
Memory AI Lab.

## Teoria essenziale

Spiega concetti, assunzioni e trade-off: il *perche'* prima del *come*. Ogni
claim tecnico rilevante deve avere una citazione primaria vicina. Non descrivere
qui le API.

Per lezioni sui dati, quando pertinenti, distinguere: meccanismi di missingness;
media e mediana; effetti di imputazione e clipping sulla distribuzione; outlier
statistici e di dominio; duplicati esatti e near-duplicates.

## Dentro TensorFlow/Keras

Se la lezione usa TensorFlow/Keras, mostra il punto di contatto. Altrimenti
dichiara esplicitamente cosa prepara e in quale lezione o fase arriva
TensorFlow/Keras. Questa sezione non puo' essere omessa.

## Esempio guidato

Confina qui API e codice eseguito. L'esempio mostra il processo, ma non risolve
lo stesso caso dell'esercizio.

## Prova tu

Indica una modifica breve che richieda allo studente di scrivere codice e renda
verificabile l'output.

## Errori comuni

Elenca errori di decisione, non soltanto errori di sintassi.

## Riepilogo

Massimo 8 punti. Non deve contenere risposte copiabili al quiz.

## Quiz

Domande di comprensione, rischio e applicazione basate solo su concetti gia'
insegnati. Le risposte commentate sono in `solutions/<lesson-id>.md`.

## Esercizio

Completa i TODO in `exercises/<lesson-id>_starter.py`. Il file
`exercises/<lesson-id>.md` documenta input, criteri, hint e comando dei test
dedicati. I test devono fallire finche' i TODO non sono completati.

## Trasferimento al Memory AI Lab

Solo in coda, mappa il problema generico sui record di memoria. Spiega il
meccanismo reale che produce il difetto (per esempio timeout di ingestion,
estrazione parziale o retry) e motiva quali concetti e decisioni restano uguali.
Il progetto e' il punto di arrivo, non il dominio assunto in partenza.

## Fonti

- <fonte primaria e claim supportato>
