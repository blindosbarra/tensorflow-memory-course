# Piano di rework dei contenuti

Data: 2026-07-11

## Diagnosi

Le due lezioni spiegano implementazioni gia' complete e assumono il Memory AI
Lab come dominio standard invece di insegnare prima il problema generico. Gli esercizi non
richiedono di scrivere codice, le soluzioni replicano l'esempio guidato, i quiz
non hanno risposte commentate e il syllabus non rappresenta tutti i moduli di
`course/course.yaml`.

Il report indicato come `reports/reviews/course-content-review.md` non e'
presente nel workspace ne' nella cronologia Git disponibile. Il rework usa come
vincolante la diagnosi B1-B4 e M1-M5 riportata nel task; l'assenza verra'
registrata nel report finale senza inventarne il testo.

## Sequenza di patch e commit

1. Rendere `templates/lesson.md` concept-first e code-producing.
2. Rendere la learner review obbligatoria e verificabile nel template e nella
   documentazione della state machine.
3. Allineare il syllabus 1:1 al YAML, reintegrando `foundations` come Fase 0.
4. Riscrivere le due vertical slice su sensori ambientali: teoria, dataset
   challenge riproducibili, starter con TODO, test learner separati, soluzioni,
   notebook attivi e trasferimento finale motivato al Memory AI Lab.
5. Riportare entrambe le lezioni a `learner_review`, eseguire i gate e
   documentare la corrispondenza con tutti i finding.

## Vincoli

- Nessuna nuova lezione.
- Nessuno stato `done`.
- I test learner devono fallire sugli starter e restare esclusi dal pytest di
  default.
- I dataset challenge non devono essere anticipati nelle lezioni.
- Le soluzioni devono usare il dataset challenge e un compito diverso
  dall'esempio guidato.
