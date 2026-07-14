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
