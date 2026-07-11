# Instructional design guide

Scopo: mantenere il corso coerente per studenti beginner-to-intermediate.

## Persona target

La persona target:

- conosce Python base ma non e' fluente in machine learning;
- puo' leggere codice breve;
- ha poca familiarita' con TensorFlow, Keras, embedding, LLM e MLOps;
- studia in sessioni da 15-30 minuti;
- vuole risultati osservabili, non solo teoria.

## Struttura obbligatoria di una lezione

Usare `templates/lesson.md` e rispettare:

- un solo obiettivo pratico;
- massimo 3 concetti nuovi;
- output osservabile;
- esempio eseguito;
- quiz breve;
- esercizio con soluzione separata;
- fonti in fondo.

## Livello di spiegazione

Ordine consigliato:

1. intuizione concreta;
2. esempio minimo;
3. regola tecnica;
4. collegamento al progetto finale;
5. errore comune;
6. esercizio.

La matematica va introdotta solo quando serve all'azione della lezione.

## Requisiti per quiz

Ogni quiz deve includere almeno:

- una domanda di comprensione;
- una domanda su rischio o errore comune;
- una domanda applicativa legata al Memory AI Lab.

Evitare domande puramente mnemoniche come "quale funzione fa X" se non
richiedono ragionamento.

## Requisiti per esercizi

Ogni esercizio deve avere:

- input locale;
- criteri di successo;
- hint progressivi;
- soluzione separata;
- test automatico quando riguarda codice.

L'esercizio non deve introdurre una API non spiegata nella lezione.

## Learner review

Prima di marcare `done`, una persona deve rispondere:

- Ho completato la lezione in 15-30 minuti?
- Ho eseguito comandi e notebook?
- Ho capito perche' serve nel Memory AI Lab?
- Ho risolto l'esercizio senza guardare subito la soluzione?
- Quale passaggio era ambiguo?

Registrare l'esito usando integralmente `templates/learner-review.md` in
`reports/reviews/<lesson-id>-learner-review.md`. Senza tempo effettivo,
punteggio quiz, prova dell'esercizio, risposta libera, punteggi di chiarezza e
decisione umana PASS, la state machine resta in `learner_review`.

## Stile

- Italiano chiaro.
- Frasi brevi.
- Termini tecnici inglesi quando standard.
- Nessuna metafora decorativa.
- Nessun testo copiato da fonti.
- Nessuna promessa non verificata.

## Anti-pattern

- Lezione enciclopedica.
- Notebook non eseguito.
- Esercizio che e' solo copia-incolla dell'esempio.
- Modelli complessi prima di baseline semplici.
- Cloud obbligatorio per completare il corso base.
