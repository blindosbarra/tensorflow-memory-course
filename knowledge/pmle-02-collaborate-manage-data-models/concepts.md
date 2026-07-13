# Concepts: pmle-02-collaborate-manage-data-models

Decisione research: contenuto `VERIFIED` contro il testo verbatim della
exam guide ufficiale (vedi evidence.yaml). Un solo claim supplementare
(AutoSxS, aggiunto su richiesta esplicita dello studente come esempio
concreto di "LLM-as-a-judge") resta `needs_reverification`, vedi
apis.md.

## Concetti coperti

1. Il Dominio 2 ("Collaborating within and across teams to manage data
   and models", **~16% del peso, dato ufficiale**) valuta tre fasi del
   lavoro che precede l'addestramento su larga scala: preparare i dati,
   prototipare in notebook, tracciare gli esperimenti. E' il dominio con
   il focus più esplicito sulla **collaborazione tra ruoli** (data
   engineer, ML engineer, altri team) dei sei.
2. Sottosezione 2.1 — **esplorare e preprocessare i dati**: organizzare
   tipi di dato diversi (tabellare, testo, immagini) per experimenting,
   training e serving efficienti; scegliere lo strumento di preprocessing
   in base a scala e complessità (BigQuery/SQL per dati che stanno in un
   warehouse, Dataflow o Apache Spark per pipeline distribuite più grandi,
   framework Python in-memoria per dataset che stanno in RAM); creare e
   consolidare feature nel Feature Store di Gemini Enterprise Agent
   Platform; garantire privacy dei dati e gestione delle informazioni
   sensibili (PII).
3. Sottosezione 2.2 — **prototipare modelli in notebook**: applicare
   buone pratiche di collaborazione e sicurezza nel configurare ambienti
   notebook condivisi (Agent Platform Workbench, Colab Enterprise);
   sviluppare modelli con framework comuni (PyTorch, sklearn, JAX);
   usare modelli fondazionali o open-source da Model Garden per
   prototipare direttamente nel notebook, prima di scalare.
4. Sottosezione 2.3 — **tracciare ed eseguire esperimenti**: scegliere
   l'ambiente giusto per sviluppo/sperimentazione in base al framework
   usato (Experiments su Agent Platform, Agent Platform Pipelines,
   Kubeflow Pipelines); valutare soluzioni predittive e generative con
   metriche appropriate (incluso "LLM-as-a-judge" per output generativi
   difficili da valutare con metriche numeriche classiche — **AutoSxS** è
   un esempio concreto di strumento che implementa questa tecnica, non
   nominato dalla guida stessa, vedi apis.md); tracciare e confrontare
   artefatti, versioni e lineage dei modelli.

## Il filo conduttore del dominio

Le tre sottosezioni seguono l'ordine reale di un progetto: prima capisci
e prepari i dati (2.1), poi prototipi velocemente in un notebook
condiviso (2.2), poi tieni traccia di cosa hai provato e con che risultato
(2.3) — così un collega (o tu stesso tra sei mesi) può ripetere o
confrontare un esperimento senza dover rifare tutto da capo. Il tema
comune non è "come si scrive il codice", ma **come si rende il lavoro
riproducibile e condivisibile in un team**.

## Collegamento al resto del corso

Le Lezioni 1-5 del corso principale (missing values, duplicati, split
train/val/test, leakage, encoding) sono esattamente il tipo di lavoro
descritto nella sottosezione 2.1, fatto qui con pandas invece che con
BigQuery o Dataflow: lo stesso ragionamento su qualità dei dati e
separazione train/val/test si applica indipendentemente dallo strumento.
La differenza è di scala e di strumento, non di principio.

## Limiti

Questa lezione non tratta la configurazione pratica di un Feature Store,
la sintassi di Dataflow/Apache Spark, o i dettagli di un Workbench
notebook: la exam guide elenca queste come **attività da saper
riconoscere**, non fornisce dettagli implementativi da riportare qui (e
questo modulo non include notebook eseguibili né credenziali cloud, per
policy del corso). AutoSxS è spiegato con conoscenza generale
pre-addestramento sulla famiglia di prodotti Vertex AI, non verificata
contro documentazione live in questa sessione (vedi evidence.yaml).
