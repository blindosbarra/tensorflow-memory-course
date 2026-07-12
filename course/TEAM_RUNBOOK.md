# Team runbook

Scopo: permettere a un team di completare il corso senza dipendere da una chat
precedente.

## Fonti autoritative del repository

Leggere in questo ordine:

1. `AGENTS.md`
2. `COURSE_FACTORY_SPEC.md`
3. `course/TEAM_RUNBOOK.md`
4. `course/QUALITY_GATE_MATRIX.md`
5. `course/INSTRUCTIONAL_DESIGN_GUIDE.md`
6. `course/course.yaml`
7. `course/progress.yaml`
8. `templates/` (lesson, review, learner-review)

Nota 2026-07-12: la lista precedente citava cinque documenti mai creati
(IMPLEMENTATION_ROADMAP, RESEARCH_AND_EVIDENCE_PROTOCOL,
DATA_AND_ARTIFACT_POLICY, CLOUD_AND_COST_POLICY,
docs/architecture/MEMORY_AI_LAB_ARCHITECTURE). Se uno di questi diventa
necessario, va scritto e aggiunto qui nello stesso commit; non citare
documenti che non esistono.

`COURSE_FACTORY_SPEC.md` contiene la visione. I documenti in `course/` rendono
operativa quella visione.

## Unita' di lavoro

L'unita' minima e' una lezione, non un modulo intero. Un modulo puo' essere
assegnato a piu' persone solo se nessuna modifica file condivisi nello stesso
momento.

File condivisi da modificare con una sola PR alla volta:

- `course/progress.yaml`
- `mkdocs.yml`
- `docs/index.md`
- `docs/modules/index.md`
- `docs/glossary.md`
- `docs/references.md`
- `src/memory_ai/` quando cambia un contratto pubblico
- `datasets/` quando cambia uno schema riusato

## State machine operativa

Ogni lezione attraversa:

```text
planned -> researching -> evidence_review -> writing -> lab_build
-> technical_review -> learner_review -> done
```

Regole:

- `planned`: la lezione esiste in `course/course.yaml`.
- `researching`: esiste un branch o PR dedicata al research pack.
- `evidence_review`: `knowledge/<lesson-id>/evidence.yaml` e' completo.
- `writing`: il research pack e' `READY_FOR_WRITING`.
- `lab_build`: notebook, esempio, test ed esercizio sono in sviluppo.
- `technical_review`: tutti i gate locali sono stati eseguiti almeno una volta.
- `learner_review`: i gate tecnici passano, ma manca prova umana.
- `done`: gate tecnici e learner review sono passati. La review deve usare
  `templates/learner-review.md`, essere compilata in
  `reports/reviews/<lesson-id>-learner-review.md` e contenere decisione umana
  PASS; in sua assenza la state machine non puo' avanzare.

Nessuna lezione puo' saltare stati. Se un gate fallisce, riportare lo stato alla
fase responsabile del problema.

## Branch e PR

Naming suggerito:

- `research/<lesson-id>`
- `lesson/<lesson-id>`
- `lab/<lesson-id>`
- `review/<lesson-id>`
- `infra/<topic>`

Ogni PR deve includere:

- scope;
- stato iniziale e finale in `course/progress.yaml`;
- file principali modificati;
- fonti aggiunte;
- comandi eseguiti;
- risultati sintetici;
- rischi residui;
- screenshot solo quando utile per il sito.

## Sequenza standard per una lezione

1. Leggere la riga della lezione in `course/course.yaml`.
2. Aprire o creare issue usando `.github/ISSUE_TEMPLATE/course-module.md`.
3. Creare `reports/<lesson-id>-plan.md` con gap analysis e patch sequence.
4. Creare research pack in `knowledge/<lesson-id>/`.
5. Eseguire evidence review.
6. Scrivere o aggiornare la lezione in `docs/modules/<lesson-id>.md`.
7. Implementare notebook, esempio, test, esercizio e soluzione.
8. Aggiornare `mkdocs.yml`, glossario e riferimenti.
9. Eseguire tutti i gate in `course/QUALITY_GATE_MATRIX.md`.
10. Scrivere `reports/reviews/<lesson-id>.md`.
11. Aggiornare `course/progress.yaml`.
12. Aprire PR piccola e leggibile.

## Definizione di ready per una lezione

Una lezione e' pronta per essere implementata quando:

- e' presente in `course/course.yaml`;
- ha prerequisiti e output atteso in `course/IMPLEMENTATION_ROADMAP.md`;
- il research pack e' approvato;
- le API principali sono verificate contro fonti primarie;
- i dataset necessari sono locali, sintetici o documentati;
- non richiede credenziali cloud per il percorso base.

## Definizione di done per una lezione

Una lezione e' `done` solo se:

- ha una pagina MkDocs;
- ha notebook eseguito;
- ha esercizio e soluzione separata;
- ogni esempio ha test;
- il research pack e' coerente con la lezione;
- `ruff`, `mypy`, `pytest`, notebook execution e MkDocs build passano;
- la learner review umana non segnala blocker;
- `course/progress.yaml` e' coerente.

## Escalation

Aprire una voce in `course/research_gaps.md` quando:

- una fonte primaria non chiarisce un claim;
- una API e' cambiata rispetto alla lezione;
- un preset modello non e' disponibile localmente;
- un costo cloud non e' stimabile;
- un risultato non e' riproducibile.

Non colmare lacune con testo plausibile.
