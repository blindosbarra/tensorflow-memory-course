# Research gaps

## gcp-ml-certification — RISOLTO 2026-07-13

Il gap precedente (PDF ufficiale irraggiungibile dalla sandbox) e' stato
chiuso: l'utente ha caricato direttamente il PDF ufficiale
`professional_machine_learning_engineer_exam_guide_english.pdf` (Google
Cloud, edizione con "Gemini Enterprise Agent Platform" - l'aggiornamento
post 1 giugno 2026 di cui si parlava). Testo letto per intero, 5 pagine, 6
sezioni complete con tutti i bullet.

Confermato dal testo primario:

- "Gemini Enterprise Agent Platform" e' reale, e' il nome usato nella exam
  guide per l'ambito che prima era "Vertex AI"; spesso abbreviato "Agent
  Platform" nei bullet (es. "Agent Platform AutoML", "Agent Platform
  Pipelines", "Agent Platform custom training", "Agent Platform Feature
  Store", "Agent Platform Workbench").
- I sei domini, con pesi ufficiali: Section 1 Architecting low-code AI
  solutions (~13%), Section 2 Collaborating within and across teams to
  manage data and models (~16%), Section 3 Scaling prototypes into ML
  models (~21%), Section 4 Serving and scaling models (~20%), Section 5
  Automating and orchestrating ML pipelines (~18%), Section 6 Monitoring
  AI solutions (~13%).
- Ogni sezione ha sotto-sezioni numerate con bullet "Considerations
  include" - questo e' il testo usato per costruire le lezioni
  `pmle-01`...`pmle-06`, riassunto e spiegato con parole proprie (mai
  copiato verbatim nel corpo della lezione, per la regola 3.1 dello spec),
  con citazione precisa a sezione/sottosezione.

Il PDF caricato dall'utente e' trattato come fonte primaria unica per il
contenuto della exam guide in tutte le lezioni `pmle-0X-*`.

## Aggiunto su richiesta dello studente: AutoSxS (pmle-02)

Lo studente ha chiesto esplicitamente se concetti come "AutoSxS" fossero
coperti. Il nome non compare nel testo verbatim della exam guide (la
guida nomina solo "LLM-as-a-judge" genericamente, sottosezione 2.3).
Aggiunto in `knowledge/pmle-02-collaborate-manage-data-models/apis.md`
come dettaglio supplementare esplicitamente marcato
`needs_reverification`, con conoscenza generale pre-addestramento sulla
famiglia di prodotti Vertex AI, non verificata su `docs.cloud.google.com`
(bloccato in questa sessione). Nessun URL di documentazione prodotto
generato per questo dettaglio, per evitare di citare un link non
verificato.

## Residuo aperto: dettagli di sintassi prodotto non nella exam guide

La exam guide elenca **argomenti** (es. "Generating predictions using
BigQuery ML"), non sintassi SQL o dettagli implementativi. Per i dettagli
supplementari aggiunti nelle lezioni (es. nomi esatti di istruzioni SQL
BigQuery ML) resta valido il gap precedente: `docs.cloud.google.com`
restituisce 403 al fetch automatico in questa sessione, quindi quei
dettagli sono meccaniche stabili e note ma non riverificate live. Marcati
`needs_reverification` in ciascun `evidence.yaml`, non bloccanti per il
Gate A del contenuto principale (che ora ha fonte primaria verificata),
ma da chiudere prima di uno studio d'esame definitivo.

## Non affermato: dettagli tecnici di prodotti non ancora documentati alla data del training

Prodotti/funzionalita' citati nella exam guide su cui l'assistente non ha
conoscenza affidabile pre-addestramento (nomi troppo recenti, es. "Gemini
Enterprise Agent Platform Inference", "Ray on Gemini Enterprise Agent
Platform", "Model Armor"): le lezioni li citano **esattamente come li
nomina la exam guide**, senza aggiungere dettagli implementativi non
verificabili. Se lo studio d'esame richiede il dettaglio, va cercato dallo
studente sulla documentazione prodotto corrente.

## Nuovo gap: lezione pmle-07, sintesi non verbatim exam guide

`pmle-07-architetture-end-to-end` (aggiunta 2026-07-14 su richiesta
esplicita dello studente) non è mappata su alcuna sezione della exam
guide: è una sintesi didattica che applica concetti già verificati (o
già marcati `needs_reverification`) nelle lezioni pmle-01..06 a tre
architetture costruite (previsione acquisto, previsione meteo,
classificazione fiori con AutoML), con tabelle numeriche di
overfitting/underfitting/matrice di confusione multi-classe costruite
per essere didatticamente coerenti, non output reali. Nessun nome di
prodotto nuovo introdotto rispetto a quelli già citati nelle lezioni di
dominio. Gate A (research) è `not_applicable` per questa lezione, non
`pass`, proprio perché non c'è un testo primario da verificare — vedi
`course/progress.yaml` e `knowledge/pmle-07-architetture-end-to-end/evidence.yaml`.

## Nuovo gap: rendering live dei diagrammi Mermaid e struttura esatta del Well-Architected Framework

I quattro diagrammi Mermaid aggiunti a `pmle-07-architetture-end-to-end`
non sono stati verificati visivamente in questa sessione: Material for
MkDocs recupera `mermaid.js` da `unpkg.com` a runtime nel browser, e
quella richiesta esce bloccata dal proxy di questa sandbox
(`ERR_TUNNEL_CONNECTION_FAILED`), la stessa classe di restrizione che ha
bloccato altri fetch esterni in questa sessione. `mkdocs build --strict`
passa e i blocchi `pre.mermaid` sono presenti nell'HTML generato con la
sintassi corretta (verificata manualmente); il rendering visivo va
controllato dallo studente sul sito pubblicato. La struttura a cinque
pilastri del Google Cloud Architecture Framework citata nella stessa
lezione è conoscenza generale pre-addestramento, non riverificata contro
`cloud.google.com/architecture/framework` in questa sessione.

## Nuovo gap: modulo text-embeddings (Lezioni 16-21), rete bloccata e dipendenza UMAP non installabile

Aggiunta 2026-07-16, costruzione delle Lezioni 16-21 (modulo
`text-embeddings`: embedding layer, sentence embeddings, similarità
coseno, PCA/UMAP, clustering, metriche di retrieval), su richiesta
esplicita dello studente ("please build all" seguito da "Continue from
where you left off" dopo un fallimento del tool di chiarimento scope).

- **Rete bloccata**: `keras.io`, `www.tensorflow.org`, `scikit-learn.org`
  ed `en.wikipedia.org` restituiscono tutti 403 dal proxy di
  organizzazione in questa sessione (stessa restrizione già loggata per
  `docs.cloud.google.com` nel modulo PMLE). Tutte le claim tecniche nei
  nuovi `knowledge/<lezione>/evidence.yaml` (embedding-layer,
  sentence-embeddings, cosine-similarity, pca-umap, clustering-memories,
  retrieval-metrics) sono marcate `needs_reverification`: provengono da
  conoscenza generale pre-addestramento su API consolidate e ben
  documentate (Keras `Embedding`/`GlobalAveragePooling1D`/
  `GlobalMaxPooling1D`, scikit-learn `PCA`/`KMeans`/`cosine_similarity`/
  `adjusted_rand_score`, la definizione standard di Mean Reciprocal Rank),
  non verificate live in questa sessione.
- **`umap-learn` non installabile**: `uv add --optional ml umap-learn` ha
  fallito con `RuntimeError: Cannot install on Python version 3.11.15;
  only versions >=3.6,<3.10 are supported` (una dipendenza a monte,
  verosimilmente `numba`/`llvmlite` risolta da una vecchia versione di
  `umap-learn`, richiede Python `<3.10`). Nessuna versione alternativa è
  stata forzata. Decisione: la Lezione 19 (`pca-umap`) copre UMAP solo
  concettualmente (nessun codice eseguito, nessun output inventato); la
  parte hands-on usa solo `PCA` di scikit-learn, già disponibile come
  dipendenza core del corso. `umap-learn` **non** è stato aggiunto a
  `pyproject.toml`.
- **Citazione scartata invece di inventata**: per la Lezione 21
  (`retrieval-metrics`) era stata considerata una citazione al libro di
  testo *Introduction to Information Retrieval* (Manning/Raghavan/
  Schütze, `nlp.stanford.edu/IR-book`), ma l'URL esatto del capitolo non
  è verificabile in questa sessione (rete bloccata) — scartata invece di
  essere inclusa non verificata, in linea con il principio "nessuna
  invenzione" (§3.2). La sezione Fonti della lezione cita solo le due URL
  di pattern verificabile (scikit-learn, Wikipedia).
- Tutti i numeri quantitativi citati nelle pagine docs e nei notebook
  (accuratezza, varianza spiegata dalla PCA, Adjusted Rand Index,
  Precision@K/Recall@K/MRR) sono stati **misurati per davvero** eseguendo
  i notebook in questa sessione (`uv run` + `nbclient`), non stimati o
  inventati — vedi `course/progress.yaml` per il dettaglio per lezione.

## transformers-gemma (Fase 5, Lezioni 30-37) — 2026-07-18

- **Lezioni 30-33 (attention-intuition, self-attention-math, transformer-block,
  tokenizer-generation)**: costruite da zero in **NumPy** ed eseguite davvero
  in questa sessione (`uv run` + `nbclient`). Tutti i numeri nelle pagine docs
  (pesi di attenzione, forme, media/std dopo layer norm, dimensione vocabolario
  66, stringhe generate dal bigram) sono output reali, non inventati. Le claim
  teoriche citano *Attention Is All You Need* (Vaswani et al., 2017,
  arXiv:1706.03762) e sono marcate `needs_reverification` perche' l'egress di
  rete verso arxiv.org/keras.io/numpy.org non e' testato live in questo sandbox
  (stesso pattern gia' loggato sopra).
- **Lezioni 34-37 (keras-hub, gemma-inference, structured-output,
  evaluation-generative)**: richiedono il modello open **Gemma** via KerasHub.
  Il pacchetto `keras-hub` e' un extra opzionale (`ml`) e i pesi Gemma sono un
  download **autenticato di diversi GB** non ottenibile attraverso il proxy di
  questo ambiente. Decisione (coerente con §3.2 "nessuna invenzione" e §3.3
  "esecuzione prima della pubblicazione"): i notebook usano una **guardia di
  ambiente** che salta le celle del modello quando KerasHub/Gemma non sono
  presenti, cosi' i notebook **restano eseguibili in CI** (verificato in questa
  sessione) senza inventare output del modello. Il codice mostrato e' l'API
  reale di KerasHub (`GemmaCausalLM.from_preset`, `.generate`,
  `compile(sampler=...)`), marcata `needs_reverification`: NON eseguita contro
  i pesi reali in questa sessione. Le parti di **progetto** di ognuna di queste
  lezioni sono invece pienamente eseguibili senza modello (registro dei preset,
  estrattore a regole di fallback, validatore JSON contro lo schema della
  Lezione 22, metriche precision/recall/F1 a livello di entita' con guardia di
  regressione) e girano davvero. Quando i pesi Gemma saranno disponibili in un
  ambiente con GPU, le celle guardate vanno eseguite e le claim relative
  ri-verificate prima di marcare `done` le Lezioni 34-37.

## lora (Fase 6, Lezioni 38-44) — 2026-07-18

- **Lezioni 38-40, 42-44**: costruite da zero in **NumPy** ed **eseguite davvero**
  in questa sessione. Tutti i numeri nelle docs (conteggi parametri, errori di
  ricostruzione SVD, discesa della perdita dell'adapter, errore di
  quantizzazione int8, tabella full-vs-LoRA, dimensione dell'adapter su disco)
  sono output reali, non inventati. Le claim teoriche citano *LoRA* (Hu et al.,
  2021, arXiv:2106.09685) e *QLoRA* (Dettmers et al., 2023, arXiv:2305.14314) e
  sono marcate `needs_reverification` perche' l'egress di rete non e' testato
  live in questo sandbox.
- **Lezione 41 (gemma-lora)**: richiede i pesi Gemma. Come le Lezioni 34-37, le
  celle del modello (`backbone.enable_lora(rank=...)`) sono **guardate** e saltate
  quando KerasHub/Gemma non sono presenti, cosi' il notebook resta eseguibile in
  CI. L'API mostrata e' reale, `needs_reverification`, non eseguita contro i pesi
  reali. La cella di progetto (stima del risparmio di parametri) e' pienamente
  eseguibile e gira davvero.
- **Nota di onesta' didattica (Lezione 43)**: la prima stesura del confronto
  full-vs-LoRA usava un aggiornamento a rango pieno, dove LoRA non puo' per
  costruzione eguagliare il full fine-tuning: sarebbe stato fuorviante. Corretto
  a un aggiornamento di rango basso (la premessa esplicita di LoRA, Lezione 39),
  cosi' la tabella mostra onestamente che a rango sufficiente LoRA eguaglia il
  full FT con una frazione dei parametri.
