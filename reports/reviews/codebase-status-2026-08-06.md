# Review: stato del codebase e prontezza del repository

Data: 2026-08-06
Tipo: review tecnica e di prontezza dell'intero repository
Ambito: quality gate eseguiti localmente, CI su GitHub, coerenza fra
`COURSE_FACTORY_SPEC.md`, `course/course.yaml`, `course/progress.yaml` e gli
artefatti realmente presenti.

## Decisione

**NON RILASCIABILE** secondo la definizione di completamento della spec
(sezione 2). Il repository e' pero' in buono stato come corso in costruzione:
le lezioni 1-30 sono utilizzabili da uno studente oggi.

Sintesi: 1 blocker tecnico (CI rossa da tre settimane, causa singola e
circoscritta), 1 blocker di copertura (17 lezioni dichiarate e mai scritte),
3 problemi major di qualita' e coerenza, 4 minori.

## Stato dei quality gate

Eseguiti in locale il 2026-08-06 con `uv sync --extra dev --extra ml`
(Python 3.11.15, keras-hub 0.29.1):

| Gate | Comando | Esito |
|---|---|---|
| Lint | `ruff check .` | PASS |
| Tipi | `mypy src` (strict) | PASS — 3 file |
| Test | `pytest` | PASS — 8 test |
| Notebook | `python scripts/execute_notebooks.py` | **FAIL — 5 su 61** |
| Sito | `mkdocs build --strict` | PASS |

CI su GitHub Actions (`ci.yml`), ultime esecuzioni su `master`:

- ultimo run verde: **2026-07-18**, commit "Add memory-representation module:
  Lessons 22-29";
- da allora **8 run consecutivi falliti**, incluso l'ultimo
  (run 31031135933, commit `aa4eade`, 2026-08-05);
- in tutti, lo step che fallisce e' `Execute notebooks`; `Build docs` viene
  di conseguenza saltato.

Tutti i moduli aggiunti dalla Lezione 31 in poi (Fasi 5-8, cioe' meta' del
corso) sono quindi stati integrati su `master` con la CI rossa. Questo viola
la regola di `AGENTS.md` "Non marcare `done` se un quality gate fallisce".

## Blocker

### B1. La guardia d'ambiente di Gemma testa la condizione sbagliata

Cinque notebook falliscono, sia in CI sia in locale, sempre per la stessa
causa:

- `notebooks/lezione-34-keras-hub.ipynb`
- `notebooks/lezione-35-inferenza-gemma.ipynb`
- `notebooks/lezione-36-output-strutturato.ipynb`
- `notebooks/lezione-41-gemma-lora.ipynb`
- `notebooks/lezione-56-capstone-gemma-lora.ipynb`

La guardia presente in ciascuno di essi e':

```python
GEMMA_AVAILABLE = False
try:
    import keras          # noqa: F401
    import keras_hub      # noqa: F401
    GEMMA_AVAILABLE = True
except Exception as exc:  # noqa: BLE001
    _motivo = f"{type(exc).__name__}: {exc}"
```

L'intento e' corretto e documentato nel commento della cella ("in questo
ambiente non sono presenti, quindi le celle che usano il modello vengono
SALTATE"). L'implementazione pero' verifica **la presenza del pacchetto**,
non **la disponibilita' dei pesi**. La CI installa `--extra ml`, che include
`keras-hub`: l'import riesce, `GEMMA_AVAILABLE` diventa `True`, e la cella
successiva chiama davvero

```python
gemma = keras_hub.models.GemmaCausalLM.from_preset("gemma_2b_en")
```

che tenta un download autenticato da Kaggle e fallisce:

```
KaggleApiHTTPError: 403 Client Error.
You don't have permission to access resource at URL:
https://kaggle.com/models/keras/gemma/keras/gemma_2b_en/3.
```

I pesi Gemma richiedono autenticazione Kaggle e accettazione della licenza:
condizioni che un runner CI non soddisfa e non deve soddisfare.

Verificato in locale: `keras_hub` importa correttamente (0.29.1), quindi la
guardia si apre; il download fallisce poi per la stessa ragione (403 sul
proxy). 56 notebook su 61 passano; i 5 che falliscono sono esattamente quelli
sopra.

Direzione: la guardia deve testare la reale raggiungibilita' del preset, non
l'import. Per esempio subordinandola a una variabile d'ambiente esplicita
(`GEMMA_ENABLED`) o alla presenza delle credenziali (`KAGGLE_USERNAME` e
`KAGGLE_KEY`), e comunque avvolgendo `from_preset` in un `try/except` che
ricada sul ramo `[saltato]`. E' una correzione piccola e localizzata: sblocca
la CI e con essa l'intero sistema di quality gate.

### B2. 17 lezioni su 84 dichiarate in `course.yaml` non esistono

Non hanno pagina in `docs/modules/`, non hanno notebook e non sono nemmeno
tracciate in `course/progress.yaml`:

- **modulo `mlops` — 10 lezioni, interamente assente**:
  `reproducible-project`, `containers-artifacts`, `local-training-pipeline`,
  `vertex-ai-training`, `vertex-ai-pipelines`, `registry-deployment`,
  `batch-online-inference`, `model-evaluation`, `monitoring-drift`,
  `cost-cleanup-security`;
- **`data-engineering`**: `tfdata-performance`, `data-validation`;
- **`keras-dnn`**: `forward-pass`, `losses-optimizers`, `backprop-autodiff`,
  `sequential-functional-api`, `callbacks-checkpoints`.

Conseguenza diretta sulla spec sezione 2, che richiede "esiste almeno una
pipeline Vertex AI documentata e testabile": nel repository non esiste codice
Vertex AI o `google-cloud-aiplatform` di alcun tipo. Vertex AI e' trattato
solo come teoria d'esame nel modulo PMLE (`docs/modules/pmle-*.md`), che e'
dichiarato facoltativo e non sostituisce il Passo 5 del processo operativo.

Va presa una decisione esplicita: costruire il modulo `mlops`, oppure
rimuoverlo da `course.yaml` e dalla definizione di completamento. Oggi il
tracker promette un percorso che il repository non mantiene.

## Major

### M1. La seconda meta' del corso e' molto piu' sottile della prima

Misura sui notebook (parole di markdown e celle di codice, mediana):

| Intervallo | Parole di teoria | Celle di codice |
|---|---|---|
| Lezioni 1-30 | 1085 | 6 |
| Lezioni 31-60 | 355 | 3 |

Le lezioni 31-60 (30 notebook, Fasi 5-8: Transformer, Gemma, LoRA,
preference learning, capstone) sono circa **un terzo** della densita' delle
precedenti. Non e' solo una questione di volume:

- **nessuna delle 30 ha la sezione "Esercizio guidato"**;
- **nessuna delle 30 ha "Soluzione spiegata"**.

Le lezioni 1-30 le hanno entrambe (29 e 30 occorrenze rispettivamente), con
un buon impianto: cella starter con `pass` e commento del compito, poi
spiegazione, poi soluzione eseguibile con `assert`.

Questo contraddice due affermazioni pubblicate:

- `README.md`: "Ogni lezione e' **un notebook autosufficiente**: teoria,
  esempi eseguibili, esercizio guidato con soluzione spiegata, quiz [...]";
- `docs/index.md`: "ogni lezione e' accompagnata dal proprio notebook Jupyter
  autosufficiente con teoria, esempi di codice eseguibili, esercizio guidato
  e passo incrementale del Memory AI Lab".

Quiz e riepilogo, va detto, sono presenti in tutte e 60 le lezioni.

E' anche una regressione rispetto al report vincolante
`reports/reviews/course-content-review.md`, il cui blocker B1 era proprio
"lo studente non scrive mai codice": risolto per le lezioni 1-2 e poi esteso
fino alla 30, ma non applicato alla Fase 5 in avanti.

### M2. I research pack sono quasi tutti incompleti

La spec (sezione 5) prevede per ogni topic `knowledge/<topic>/` con
`concepts.md`, `apis.md`, `examples.md`, `pitfalls.md`, `evidence.yaml`,
`references.md`.

Su 67 directory: **9 complete**, **58 con il solo `evidence.yaml`**.

Le 9 complete sono `data-cleaning-01-missing-values`,
`duplicates-types-outliers` e i 7 pack `pmle-*`. Tutte le altre — comprese
tutte le lezioni 3-60 — hanno solo le evidenze.

Nonostante questo, `course/progress.yaml` marca `research: pass` nel blocco
`quality_gates` di ognuna di esse. Il Gate A dichiarato non corrisponde a
quello applicato.

### M3. Il tracker sovrastima lo stato reale

- Tutte le 60 lezioni principali sono `learner_review` con
  `quality_gates: code: pass`, mentre il gate notebook fallisce e la CI e'
  rossa da tre settimane.
- `course.yaml` ha statuti fermi: `foundations`, `data-engineering` e
  `keras-dnn` sono ancora `planned` benche' scritte e pubblicate; `mlops` e'
  `planned` ed e' effettivamente vuoto — stesso statuto per due situazioni
  opposte, quindi lo statuto non informa.
- `course_status: milestones_0_to_5_authored_ready_for_learner_review` e
  `current_milestone: milestone-5`, mentre il syllabus e il sito descrivono
  8 fasi piu' il capstone.
- Nessuna review umana di learner risulta depositata: la "direzione" del
  report di verifica del 2026-07-12 indicava la learner review umana come
  gate bloccante non delegabile, e in `reports/reviews/` non esiste alcun
  file `*-learner-review.md`.

## Minori

### m1. Path assoluto locale nella home page del sito

`docs/index.md:15` collega la spec cosi':

```
[`COURSE_FACTORY_SPEC.md`](file:///usr/local/google/home/sommacampagna/projects/tensorflow-memory-course/COURSE_FACTORY_SPEC.md)
```

E' un link rotto per chiunque legga il sito pubblicato, ed espone il percorso
locale e lo username dell'autore. Viola `AGENTS.md` ("Non utilizzare path
assoluti") e il Gate C ("nessun path locale assoluto"). `mkdocs --strict` non
lo intercetta perche' e' formalmente un URL esterno. E' l'unico path assoluto
del repository.

### m2. Glossario e riferimenti fermi alla Lezione 2

- `docs/glossary.md` contiene **2 voci**: "Imputazione" e "Missing value".
  Il corso copre embedding, attention, Transformer, LoRA, QLoRA, DPO, RLHF,
  retrieval ibrido, drift.
- `docs/references.md` contiene **6 link**, tutti relativi alle lezioni 1-2
  (pandas, scikit-learn, un tutorial TensorFlow).

Il Gate E richiede "glossario aggiornato". Le fonti per lezione esistono
comunque: tutte e 67 le pagine in `docs/modules/` hanno la sezione "Fonti".

### m3. Artefatti residui del vecchio impianto degli esercizi

Il commit `3fa5799` ("lessons become self-contained notebooks") ha eliminato
`exercises/*_starter.py` e `tests/exercises/`, cioe' l'infrastruttura di
esercizi verificati automaticamente che il report del 2026-07-12 registrava
come prova della risoluzione del blocker B1.

Restano pero' `exercises/*.md` e `solutions/*.md` (15 file ciascuno, solo per
le lezioni 1-15), ora superati dai notebook. Due pagine pubblicate
(`data-cleaning-01-missing-values.md`, `duplicates-types-outliers.md`)
rimandano ancora a `solutions/...md`, che non fanno parte di `docs/` e quindi
non sono raggiungibili dal sito.

Conseguenza sostanziale: oggi `pytest` copre solo `src/memory_ai`, cioe' il
codice delle lezioni 1-2. Non esiste piu' alcuna verifica automatica del
lavoro dello studente; la correttezza degli esercizi delle lezioni 3-30 e'
affidata agli `assert` dentro le celle di soluzione.

### m4. Portabilita' e riproducibilita'

- `notebooks/consolidato-memoria-lezioni-01-15.ipynb` fa `import resource`
  senza guardia: modulo assente su Windows, quindi il notebook non parte —
  mentre il `README.md` da' istruzioni esplicite per PowerShell. Il commento
  della cella ("KB -> MB su Linux") segnala inoltre che il valore stampato
  sarebbe sbagliato su macOS, dove `ru_maxrss` e' in byte.
- **21 notebook** usano casualita', split o addestramento Keras senza fissare
  un seed. Fra questi `lezione-54-capstone-classificatore.ipynb`, che
  addestra e salva `models/memory_type_classifier.keras`, artefatto poi
  riutilizzato dalle lezioni successive. Il Gate C chiede "seed controllato
  dove possibile".

## Cosa funziona bene

Vale la pena registrarlo, perche' e' la base su cui poggiano le correzioni:

- **Igiene del codice**: `ruff`, `mypy --strict` e `pytest` sono puliti.
  `src/memory_ai/` e' piccolo ma scritto bene: tipizzato, docstring che
  spiegano le decisioni didattiche, report auditabili restituiti come
  dataclass, validazione esplicita delle colonne richieste.
- **Navigazione del sito coerente al 100%**: nessuna voce di `mkdocs.yml`
  punta a un file mancante, e nessuna pagina in `docs/` e' orfana rispetto
  alla nav. 67 pagine, tutte raggiungibili.
- **Riproducibilita' degli artefatti**: dopo l'esecuzione completa dei 61
  notebook, `git status` e' pulito. I CSV e gli `.npy` in
  `datasets/processed/` vengono rigenerati identici a quelli versionati. Gli
  script generatori in `scripts/` sono tutti seedati.
- **Il degrado su Gemma e' progettato**: il ramo `else` di ogni cella stampa
  `[saltato]` e spiega cosa avrebbe fatto il modello. L'idea e' giusta,
  sbagliata e' solo la sonda di disponibilita' (B1).
- **Disciplina sulle evidenze**: `course/research_gaps.md` documenta
  onestamente cio' che non e' stato verificato, con marcatori
  `needs_reverification`; la review del 2026-07-12 ha intercettato e corretto
  un DOI errato marcato `verified`. E' un processo che sta funzionando.
- **Nessun segreto** nel repository; un solo path assoluto (m1).
- **Il modulo PMLE e' sostanzioso e bilingue**: 7 unita' in italiano e
  inglese, pagine da 12-40 KB, con research pack completi — di gran lunga il
  materiale piu' approfondito del repository.

## Prontezza per fascia

| Fascia | Stato |
|---|---|
| Lezioni 1-30 (Fasi 0-4) | **Utilizzabili oggi.** Teoria, esercizio, soluzione, quiz, notebook eseguibile. |
| Lezioni 31-60 (Fasi 5-8) | **Bozze eseguibili ma sottili.** Nessun esercizio, nessuna soluzione, teoria ridotta a un terzo. 5 non eseguibili senza credenziali Kaggle. |
| Modulo `mlops` (10 lezioni) | **Inesistente.** |
| Modulo PMLE (7 unita', facoltativo) | **Il piu' completo del repository.** |

In proporzione alle 84 lezioni dichiarate: circa il 45% e' alla qualita'
promessa, il 35% e' scheletro, il 20% non esiste.

## Ordine di intervento suggerito

1. **B1 — guardia Gemma.** Correzione piccola, sblocca la CI e restituisce
   valore a tutti gli altri gate. Da fare per prima.
2. **M3 — riallineare `progress.yaml` e `course.yaml` alla realta'.** Finche'
   il tracker dice il falso, ogni decisione successiva parte da dati
   sbagliati.
3. **M1 — esercizi e soluzioni per le lezioni 31-60**, oppure correggere
   `README.md` e `docs/index.md` per non promettere cio' che non c'e'.
4. **B2 — decidere sul modulo `mlops`**: costruirlo (e con esso la pipeline
   Vertex AI richiesta dalla spec) o rimuoverlo dalle dichiarazioni.
5. **m1, m2 — path assoluto, glossario, riferimenti.** Interventi brevi, alta
   visibilita' sul sito pubblicato.
6. **M2 — research pack**: completarli per le lezioni gia' scritte, oppure
   emendare la spec se il solo `evidence.yaml` e' ritenuto sufficiente.
7. **m3, m4 — pulizia dei residui, seed, portabilita' Windows.**
