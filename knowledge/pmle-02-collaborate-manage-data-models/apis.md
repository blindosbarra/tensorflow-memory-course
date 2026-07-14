# APIs: pmle-02-collaborate-manage-data-models

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud — vedi `course.yaml`, nota del modulo). I nomi sotto
sono quelli usati testualmente dalla exam guide ufficiale (fonte primaria,
vedi evidence.yaml).

## Strumenti di preprocessing (2.1)

- **BigQuery (SQL)**: preprocessing dentro il data warehouse, per dati
  già tabellari e già in BigQuery. **Stato: verified** (nome testuale).
- **Dataflow**: servizio gestito per pipeline di elaborazione dati su
  larga scala. **Stato: verified** (nome testuale, nessun dettaglio di
  sintassi affermato).
- **Apache Spark**: framework distribuito per elaborazione dati su
  larga scala. **Stato: verified** (nome testuale).
- **Framework Python in-memoria**: citati genericamente dalla guida
  (es. pandas), per dataset che stanno in memoria. **Stato: verified**
  (categoria testuale, nessun nome di libreria specifico affermato dalla
  guida oltre "in-memory Python frameworks").
- **Gemini Enterprise Agent Platform Feature Store**: repository per
  creare e consolidare feature riutilizzabili tra training e serving.
  **Stato: verified** (nome testuale).

## Ambienti di prototipazione (2.2)

- **Gemini Enterprise Agent Platform Workbench**: ambiente notebook
  gestito. **Stato: verified** (nome testuale).
- **Colab Enterprise**: ambiente notebook gestito, alternativa a
  Workbench citata dalla guida. **Stato: verified** (nome testuale).
- **Framework citati per lo sviluppo in notebook**: PyTorch, sklearn,
  JAX. **Stato: verified** (nomi testuali, nessun dettaglio d'uso
  affermato).
- **Model Garden**: catalogo di modelli fondazionali e open-source
  usabile per creare prototipi in notebook. **Stato: verified** (nome
  testuale, stesso Model Garden citato nella Sezione 1).

## Ambienti per esperimenti (2.3)

- **Experiments su Gemini Enterprise Agent Platform**: ambiente per
  tracciare esperimenti. **Stato: verified** (nome testuale).
- **Gemini Enterprise Agent Platform Pipelines**: ambiente gestito per
  pipeline. **Stato: verified** (nome testuale).
- **Kubeflow Pipelines**: alternativa citata per orchestrare pipeline,
  scelta in base al framework usato. **Stato: verified** (nome testuale).
- **Gemini Enterprise Agent Platform ML Metadata**: sistema per tracciare
  artefatti, versioni e lineage dei modelli. **Stato: verified** (nome
  testuale).
- **"LLM-as-a-judge"**: tecnica citata dalla guida per valutare soluzioni
  generative, oltre alle metriche di valutazione classiche. **Stato:
  verified** (termine testuale, nessun dettaglio implementativo affermato
  dalla guida oltre al nome).

## Dettaglio supplementare (non nella exam guide)

- **Feature Store, meccanica reale**: organizza le feature per "entity
  type" (es. `cliente_b2b`); ogni feature è calcolata da una pipeline
  separata e scritta con un timestamp, non calcolata al volo. Due
  percorsi di lettura: online (bassa latenza, una entità alla volta, per
  il serving) e offline/batch (per costruire dataset di training). La
  lettura offline deve essere **point-in-time correct**: per
  un'etichetta registrata al tempo T, va usato il valore della feature
  come era al tempo T, non il valore corrente — altrimenti si introduce
  data leakage (stessa categoria di errore della Lezione 4 del corso
  principale, applicata a feature che cambiano nel tempo). **Stato:
  needs_reverification** (meccanica generale di un feature store, non
  riverificata su documentazione live del prodotto specifico).
- **AutoSxS, come si imposta**: tre ingredienti — un dataset di
  valutazione rappresentativo, due risposte generate sugli stessi input
  (baseline vs candidato), un template che dice all'autorater su cosa
  giudicare (es. accuratezza e concisione). L'autorater è a sua volta un
  modello e può avere bias sistematici (es. preferire risposte più
  lunghe); la pratica è calibrarlo su un campione giudicato anche da
  persone prima di fidarsi del risultato su larga scala. **Stato:
  needs_reverification** (pratica generale di valutazione pairwise con
  autorater, non riverificata su documentazione live).
- **AutoSxS ("Auto side-by-side")**: strumento di valutazione di Vertex AI
  / Gemini Enterprise Agent Platform che confronta automaticamente gli
  output di due modelli (o due versioni dello stesso modello) sugli stessi
  prompt, usando un autorater (un LLM-as-a-judge) per scegliere la
  risposta preferita e produrre metriche tipo win-rate — senza bisogno di
  un valutatore umano per ogni esempio. È un esempio concreto della
  tecnica "LLM-as-a-judge" che la guida nomina genericamente in 2.3, ma il
  nome "AutoSxS" **non compare** nel testo della exam guide stessa.
  **Stato: needs_reverification** — conoscenza generale pre-addestramento
  sulla famiglia di prodotti Vertex AI, non verificata su
  `docs.cloud.google.com` in questa sessione (bloccato, vedi
  `course/research_gaps.md`); nome, disponibilità o meccanica esatta
  potrebbero essere cambiati.
