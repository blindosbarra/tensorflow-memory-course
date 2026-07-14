# APIs: pmle-05-automate-orchestrate-ml-pipelines

Nessun notebook eseguibile per questo modulo (teoria pura, nessuna
credenziale cloud). I nomi sotto sono quelli usati testualmente dalla exam
guide ufficiale (fonte primaria, vedi evidence.yaml).

## Orchestrazione (5.1)

- **Gemini Enterprise Agent Platform Pipelines**: servizio gestito per
  orchestrare pipeline, stesso nome già visto nel Dominio 2/3. **Stato:
  verified** (nome testuale).
- **Managed Service for Apache Airflow**: servizio gestito per
  orchestrazione più generale (non specifico di ML). **Stato: verified**
  (nome testuale).
- **Ray on Gemini Enterprise Agent Platform**: citato come opzione per
  carichi distribuiti. **Stato: verified** che il nome compare nella
  guida; nessun dettaglio implementativo affermato oltre al nome,
  prodotto troppo recente per conoscenza pre-addestramento affidabile
  (vedi `course/research_gaps.md`).

## Dettaglio supplementare: come si scrive una pipeline, e quale motore scegliere

- **Definizione di una pipeline con l'SDK Kubeflow**: componenti scritti
  come funzioni decorate (`@dsl.component`), collegate in un grafo
  passando l'output di una come input della successiva
  (`@dsl.pipeline`); un passo condizionale (`dsl.If`) può bloccare il
  deploy se una metrica di valutazione non supera una soglia. Vedi
  esempio completo (validazione dati → estrazione feature → training →
  valutazione → deploy condizionale) nella pagina della lezione. **Stato:
  needs_reverification** (sintassi semplificata a scopo didattico, non
  testata contro una versione reale della libreria).
- **Kubeflow Pipelines su GKE vs Agent Platform Pipelines, criterio di
  scelta**: stessa sintassi di pipeline (SDK Kubeflow), motore di
  esecuzione diverso. Agent Platform Pipelines è gestito (nessun cluster
  da amministrare, integrazione nativa con Feature Store/Model
  Registry/Experiments) — scelta di default per un team già su Google
  Cloud. Kubeflow su GKE serve quando conta la portabilità multi-cloud/
  on-premise, il controllo fine sulla configurazione del cluster, o
  competenze Kubernetes già presenti in azienda. **Stato:
  needs_reverification** (ragionamento generale sul trade-off
  gestito-vs-self-managed, non verificato su documentazione live).

## Retraining automatico (5.2)

- **CI/CD/CT (continuous integration, continuous delivery, continuous
  training)**: acronimo citato dalla guida per pipeline che distribuiscono
  modelli. **Stato: verified** che il termine compare nella guida; la
  spiegazione concettuale in concepts.md è conoscenza MLOps generale, non
  specifica di prodotto — **needs_reverification** per dettagli
  implementativi Google Cloud specifici (vedi evidence.yaml).
- **Cloud Build**: citato come esempio di strumento per queste pipeline.
  **Stato: verified** (nome testuale, nessun dettaglio d'uso affermato).
