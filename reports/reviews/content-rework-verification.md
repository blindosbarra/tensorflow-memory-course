# Review di verifica: content rework (secondo giro)

Data: 2026-07-12
Tipo: review indipendente del rework registrato in
`reports/reviews/content-rework.md`, eseguita contro il report vincolante
`reports/reviews/course-content-review.md` (che il rework non aveva potuto
leggere: era su un branch non ancora mergiato).

## Decisione

**PASS con correzioni applicate in questo stesso commit.**
Il rework risolve nella sostanza tutti i blocker (B1-B4) e i major (M1-M5).
La verifica ha pero' trovato sei difetti nuovi, di cui uno sulle fonti
(DOI errato marcato "verified") che per il processo di questo repository e'
grave. Tutti i difetti oggettivi sono corretti in questo commit; le due
lezioni restano in `learner_review` in attesa del learner umano.

## Verifica dei finding originali

| Finding | Esito | Prova eseguita |
|---|---|---|
| B1 codice dello studente | RISOLTO | Starter con TODO; `pytest tests/exercises` fallisce con gli starter vuoti (2 failed) e passa sostituendo le soluzioni ufficiali (2 passed). Test bidirezionale eseguito. |
| B2 teoria assente | RISOLTO | Meccanismi di Rubin, media/mediana (NIST), effetti distributivi di imputazione e clipping, IQR vs contratto di dominio, near-duplicates/record linkage. Quiz rispondibile dal testo, risposte motivate in `solutions/`. |
| B3 syllabus incoerente | RISOLTO | 10 fasi mappano 1:1 i 10 moduli yaml; `foundations` reintegrato come Fase 0 (scelta conservativa, da validare dal learner); percorso minimo, assessment e ore per fase; totale 38,5 h. |
| B4 dominio invertito | RISOLTO | Lezioni, esempi, notebook ed esercizi partono dalla telemetria ambientale; il Memory AI Lab e' solo trasferimento finale motivato (timeout ingestion, retry, estrazione parziale). |
| M1-M5 | RISOLTI | Sezione TF esplicita sul "quando e perche'"; dataset challenge 120 righe seedati e non anticipati (rigenerati: identici al byte); quiz con risposte; rubrica `templates/learner-review.md`; esercizio ≠ esempio guidato. |
| Gate tecnici | PASS | pytest 9 passed; ruff pulito; mypy pulito; entrambi i notebook eseguiti (celle `learner-exercise` escluse dalla copia di esecuzione, con unit test dedicato); `mkdocs build --strict` ok. |

## Difetti nuovi trovati (corretti in questo commit)

1. **DOI errato marcato "verified"** (grave per il processo). La fonte
   Chaudhuri et al. 2003 era citata come `10.1145/1008992.1009037` nella
   lezione e in `knowledge/duplicates-types-outliers/evidence.yaml`; il DOI
   corretto e' `10.1145/872757.872796` (ACM SIGMOD 2003, verificato il
   2026-07-12). Un claim `status: verified` con identificatore non
   verificato viola la regola "nessuna invenzione" della spec.
2. **Fonte inesistente in evidence.yaml**: il claim sul dominio di
   `importance` citava `course/DATA_AND_ARTIFACT_POLICY.md`, file mai
   esistito nel repository. Corretto puntando a `COURSE_FACTORY_SPEC.md`.
3. **Runbook con riferimenti fantasma**: `course/TEAM_RUNBOOK.md` elencava
   cinque documenti "autoritativi" mai creati (IMPLEMENTATION_ROADMAP,
   RESEARCH_AND_EVIDENCE_PROTOCOL, DATA_AND_ARTIFACT_POLICY,
   CLOUD_AND_COST_POLICY, docs/architecture/MEMORY_AI_LAB_ARCHITECTURE).
   Lista ridotta ai file esistenti, con nota.
4. **Research pack in contraddizione con le lezioni**: i `concepts.md`
   descrivevano ancora le lezioni vecchie sul dominio memoria; quello di
   missing-values affermava "questa lezione non tratta MCAR/MAR/MNAR"
   mentre la lezione riscritta li tratta. Entrambi riscritti; `apis.md`,
   `examples.md` e `pitfalls.md` restano da riallineare (vedi direzione).
5. **README fermo alla vertical slice originale** (esempio e test vecchi
   come artefatti della lezione). Aggiornato al flusso attuale
   (starter + test dedicati + soluzioni + rubrica).
6. **`docs/modules/index.md` incoerente col syllabus**: titoli vecchi
   ("dati di memoria") e Fase 0 elencata dopo la fase dati. Corretto.

Nota di tracciabilita': la tabella di mappatura in `content-rework.md` usa
etichette proprie (il suo B3/M1-M5 non coincide con i B3/M1-M5 del report
vincolante) perche' e' stata ricostruita dal prompt. La sostanza coincide;
questa verifica, condotta sul report originale, la sostituisce come
riferimento.

## Direzione di sviluppo (in ordine)

1. **Learner review umana** (gate bloccante, non delegabile): completare la
   lezione missing-values da studente — leggere la pagina, completare
   `exercises/data-cleaning-01-missing-values_starter.py`, far passare
   `uv run pytest -o norecursedirs= tests/exercises/...`, rispondere al
   quiz — e compilare `templates/learner-review.md` in
   `reports/reviews/data-cleaning-01-missing-values-learner-review.md`.
   Poi lo stesso per duplicates-types-outliers. Solo un PASS umano
   autorizza `done`.
2. **Validare la scelta Fase 0**: il rework ha reintegrato `foundations`
   come prima fase (scelta conservativa). Se il learner la conferma, la
   prossima lezione da produrre e' `python-numpy-refresh`, non
   `train-validation-test`. Se la respinge, aggiornare course.yaml,
   syllabus e spec nello stesso commit.
3. **Produzione della prossima lezione** (solo dopo il PASS al punto 1):
   una lezione alla volta, con la state machine completa e il template
   nuovo. Regola aggiuntiva appresa da questo giro: nessun claim
   `verified` senza aver risolto DOI/URL, e nessun riferimento a file
   inesistenti (il gate A fallisce in entrambi i casi).
4. **Debito residuo, non bloccante**: riallineare `apis.md`,
   `examples.md`, `pitfalls.md` dei due knowledge pack al dominio sensori;
   decidere il destino di `datasets/processed/` e
   `reports/evaluation/*.json` (output della pipeline memoria di
   riferimento: vanno rigenerati o dichiarati artefatti del capstone);
   aggiornare `reviewed_at` degli evidence.yaml al prossimo giro di
   research.

## Comandi eseguiti in questa verifica

```bash
uv run pytest                       # 9 passed
uv run pytest tests/exercises -q    # 2 failed con starter vuoti (atteso)
# con le soluzioni copiate negli starter: 2 passed (poi ripristinati)
uv run ruff check .                 # All checks passed!
uv run mypy src                     # Success
uv run python scripts/execute_notebooks.py   # entrambi eseguiti
uv run mkdocs build --strict        # ok
uv run python scripts/generate_missing_values_challenge.py
uv run python scripts/generate_quality_challenge.py
git diff datasets/                  # nessuna differenza: riproducibili
```
