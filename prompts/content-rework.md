# Prompt: rework contenuti dopo learner review fallita

Da incollare in un nuovo thread Codex, da solo, senza altri task in parallelo.

```text
Agisci come lead engineer e instructional designer del corso.

La learner review del 2026-07-11 ha BOCCIATO il contenuto del corso.
Il report è vincolante: reports/reviews/course-content-review.md.
Leggilo integralmente prima di toccare qualsiasi file, insieme a:

- COURSE_FACTORY_SPEC.md
- docs/syllabus.md
- course/course.yaml
- course/progress.yaml
- docs/modules/data-cleaning-01-missing-values.md
- docs/modules/duplicates-types-outliers.md
- exercises/, solutions/, templates/

Diagnosi confermata, da tenere davanti mentre lavori:
le lezioni attuali sono spiegazioni di codice già scritto nel repo.
Lo studente non scrive mai una riga di codice, la "teoria" descrive
API pandas invece di concetti, il quiz non ha risposte, e il syllabus
contraddice course.yaml (il modulo foundations è dichiarato ma saltato).
In più il dominio degli esempi è invertito (finding B4): le lezioni
partono dal contesto "memoria AI" come se fosse il caso standard del
problema, quando missing values, duplicati e outlier sono problemi
generici che vanno insegnati prima su un dominio dove nascono in modo
naturale (sensori con letture mancanti o fuori scala, log duplicati,
form incompleti). Una "memoria" con importance "high" o senza timestamp
è un difetto fabbricato: lo studente non impara il problema generico e
non crede al caso specifico.
Il tuo compito è eliminare queste cause, non aggiungere contenuto sopra.

VIETATO in questo task:
- generare nuove lezioni (train-validation-test resta bloccata);
- marcare qualsiasi lezione `done`: l'unico che può farlo è il learner umano;
- esercizi risolvibili senza scrivere codice;
- soluzioni identiche all'esempio guidato della lezione;
- quiz con domande che si rispondono copiando il riepilogo o che
  richiedono concetti non ancora insegnati;
- dataset in cui la lezione elenca in anticipo i problemi da trovare;
- lezioni che usano il Memory AI Lab come dominio di partenza: il
  progetto è il punto di arrivo di ogni lezione, mai il punto di
  partenza del problema.

Esegui in quest'ordine, con un commit logico per passo:

1. TEMPLATE LEZIONE (templates/lesson.md)
   Ristruttura il template così:
   - la lezione parte SEMPRE dal problema generico, con un dataset
     realistico dove il difetto è naturale del dominio (es. letture di
     sensori con buchi e valori fuori scala, log applicativi duplicati,
     risposte di form incomplete); teoria, esempio guidato ed esercizio
     lavorano su quel dominio;
   - la sezione "Perché serve nel Memory AI Lab" diventa la sezione di
     TRASFERIMENTO in coda: spiega perché lo stesso difetto compare nei
     record di memoria (es. pipeline di estrazione che fallisce su
     alcuni campi) e mostra il mapping, con motivazione esplicita, non
     per assunzione;
   - "Teoria essenziale" deve spiegare concetti e trade-off (il perché
     delle decisioni), con le API confinate in "Esempio guidato".
     Per le lezioni dati: meccanismi di missingness, media vs mediana,
     effetto di imputazione e clipping sulla distribuzione, outlier
     statistici vs di dominio, near-duplicates. Ogni claim con fonte.
   - "Esercizio" deve puntare a codice starter con TODO che lo studente
     completa, validato da test dedicati.
   - "Quiz" deve dichiarare che le risposte commentate stanno in
     solutions/<lesson-id>.md.
   - La sezione "Dentro TensorFlow/Keras" è obbligatoria: se una lezione
     non tocca TF deve dire esplicitamente cosa prepara e quando TF arriva.

2. TEMPLATE LEARNER REVIEW (templates/learner-review.md, nuovo)
   Rubrica minima: tempo effettivo vs stimato, punteggio quiz,
   esercizio completato senza guardare la soluzione (sì/no),
   "cosa so fare ora che prima non sapevo fare" (risposta libera),
   chiarezza per sezione (1-5), decisione PASS/FAIL.
   La state machine non può passare learner_review senza questo file
   compilato in reports/reviews/.

3. SYLLABUS (docs/syllabus.md)
   Riscrivilo allineato 1:1 a course/course.yaml:
   - risolvi il conflitto foundations: o lo reintegri come Fase 0 con
     le sue lezioni, o lo elimini da course.yaml e motivi il taglio;
     la decisione deve essere esplicita e coerente in entrambi i file;
   - ogni fase mappa un modulo del yaml, con: obiettivi misurabili,
     assessment concreto di fine fase, ore totali stimate;
   - dichiara un "percorso minimo" prioritario dentro le lezioni
     pianificate, con criteri di taglio;
   - spiega in apertura perché TensorFlow arriva dopo la fase dati.

4. REWORK DELLE DUE LEZIONI ESISTENTI
   Per data-cleaning-01-missing-values e duplicates-types-outliers:
   - porta le lezioni sul nuovo template (teoria vera, con fonti
     concettuali primarie, non solo reference API);
   - ribalta il dominio: il dataset principale della lezione diventa
     generico e realistico (es. sensori ambientali con letture mancanti,
     duplicate e fuori scala), >= 100 righe, generato da uno script con
     seed fisso in scripts/, problemi NON elencati nella lezione; il
     dataset dei record di memoria resta solo nella sezione di
     trasferimento finale, con la spiegazione di come quei difetti si
     originano davvero (ingestion/estrazione), non come dato di fatto;
   - riscrivi gli esercizi in formato starter: file
     exercises/<lesson-id>_starter.py con firme e TODO, test in
     tests/exercises/test_<lesson-id>.py che validano il codice dello
     studente e falliscono finché i TODO non sono completati
     (esclusi dal pytest di default del repo, eseguibili con un comando
     documentato nell'esercizio);
   - soluzioni: implementazione completa dello starter più risposte
     commentate del quiz;
   - aggiorna i notebook: le celle finali diventano "prova tu" con
     assert che lo studente deve far passare, non una copia dell'esempio.

5. CHIUSURA
   - aggiorna course/progress.yaml: duplicates-types-outliers riparte
     dalla state machine writing -> lab_build -> technical_review e si
     ferma a learner_review in_progress; data-cleaning-01 torna in
     learner_review (non più done) perché il rework la modifica;
   - esegui tutti i gate: ruff, mypy, pytest, execute_notebooks,
     mkdocs build --strict; riporta gli output veri, senza nasconderli;
   - scrivi reports/reviews/content-rework.md con cosa è cambiato,
     mappando ogni modifica al finding del report (B1, B2, B3, M1-M5).

Definition of done di questo task:
- nessun finding del report resta senza una modifica corrispondente;
- ogni lezione parte dal problema generico su un dominio realistico e
  arriva al Memory AI Lab solo come trasferimento finale motivato;
- un esercizio non è completabile senza scrivere codice;
- il quiz ha risposte e ogni domanda è rispondibile col testo della lezione;
- syllabus, course.yaml e spec raccontano lo stesso corso;
- tutti i gate tecnici passano;
- le due lezioni sono in learner_review, in attesa del learner umano.

Non chiedere conferme intermedie. Se una decisione richiede il learner
umano (es. tagliare foundations), scegli l'opzione più conservativa,
motivala nel report e segnalala come punto da validare.
```
