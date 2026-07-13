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
