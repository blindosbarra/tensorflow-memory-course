# Content rework review

Data: 2026-07-12
Decisione tecnica: **PASS**  
Decisione learner: **PENDING**

## Limite della sorgente

`reports/reviews/course-content-review.md`, indicato come report vincolante, non
era presente nel workspace ne' nella cronologia Git disponibile. Non ne e' stato
inventato il contenuto. La mappatura B1-B4/M1-M5 usa la diagnosi vincolante
riportata nel task e deve essere validata contro il report originale quando
questo verra' ripristinato.

## Mappatura dei finding

| Finding | Causa confermata | Modifica corrispondente |
|---|---|---|
| B1 | Il learner legge codice gia' scritto | Starter Python con TODO reali e test learner rossi fino all'implementazione; l'esempio guidato usa un caso diverso. |
| B2 | Teoria ridotta a descrizione di API | Lezioni e template separano concetti/trade-off dalle API; aggiunti missingness, media/mediana, effetti distributivi, outlier statistici/di dominio, clipping e near-duplicates con evidenze primarie. |
| B3 | Quiz senza risposte verificabili | Ogni quiz ha risposte motivate in `solutions/<lesson-id>.md`; le domande usano solo concetti insegnati e non copiano il riepilogo. |
| B4 | Dominio degli esempi invertito | Teoria, esempio, notebook ed esercizio partono da letture di sensori, dove buchi, retry, tipi errati e misure fuori scala nascono naturalmente. Il Memory AI Lab compare solo nel trasferimento finale, con mapping a timeout di ingestion, retry ed estrazione parziale. |
| M1 | Syllabus incoerente con manifest | `foundations` e' reintegrato conservativamente come Fase 0; le dieci fasi mappano 1:1 i dieci moduli YAML. |
| M2 | Obiettivi e assessment vaghi | Ogni fase dichiara obiettivi misurabili, assessment concreto e ore totali; aggiunto percorso minimo con criteri di taglio. |
| M3 | Dataset didattici anticipano la diagnosi | Aggiunti due challenge ambientali da 120 righe, generati con seed `20260711`; le lezioni non elencano problemi, quantita' o posizioni. |
| M4 | Notebook ed esercizi sono copie dell'esempio | Celle finali “Prova tu” con TODO e assert inizialmente rossi; sono marcate `learner-exercise`, cosi' il gate esegue le celle didattiche senza completare il lavoro del learner. Challenge, normalizzazione e fallback differiscono dall'esempio. Soluzioni Python complete separate. |
| M5 | Learner review/state machine non verificabile | Nuova rubrica obbligatoria con tempo, quiz, autonomia, risposta libera, chiarezza 1-5 e PASS/FAIL; runbook e gate impediscono l'avanzamento senza file umano completo. |

## Evidenza che il learner deve scrivere codice

Comando diagnostico:

```text
.venv-gates\Scripts\pytest.exe -q -o norecursedirs= tests/exercises/test_data_cleaning_01_missing_values.py tests/exercises/test_duplicates_types_outliers.py
```

Risultato atteso e osservato: **2 failed**. Entrambi falliscono in uno starter
con `NotImplementedError`. La suite predefinita li esclude tramite
`norecursedirs`, perche' un gate di repository non deve completare il lavoro al
posto del learner.

## Gate eseguiti

- `uv sync --extra dev`: PASS; 136 package risolti, 86 controllati.
- `ruff check .`: PASS, `All checks passed!`.
- `mypy src`: PASS, nessun problema in 3 file sorgente.
- `pytest`: un primo tentativo dopo l'aggiunta del test del notebook executor e'
  FALLITO in collection (`ModuleNotFoundError: scripts`); corretto il caricamento
  per percorso, il rerun e' PASS con 9 test raccolti e passati.
- `python scripts/execute_notebooks.py`: PASS, eseguiti entrambi i notebook;
  le sole celle incomplete marcate `learner-exercise` sono escluse dalla copia
  di esecuzione. Warning runtime Windows/ZeroMQ non bloccanti.
- `mkdocs build --strict`: PASS, build finale in 2,14 s; informativa non bloccante per
  una pagina architecture fuori nav e warning upstream Material/MkDocs 2.0.

## Stato finale

Entrambe le lezioni hanno ripercorso `writing -> lab_build -> technical_review`
e sono ferme a `learner_review: in_progress`. Nessuna lezione e' `done`.
`train-validation-test` non e' stata generata.

## Punto da validare dal learner umano

La scelta conservativa e' mantenere `foundations` e reintegrarlo come Fase 0,
coerentemente con la progressione obbligatoria della spec. Il learner deve
validare sia questa scelta curricolare sia le due lezioni compilando la nuova
rubrica; solo una decisione umana PASS puo' autorizzare `done`.
