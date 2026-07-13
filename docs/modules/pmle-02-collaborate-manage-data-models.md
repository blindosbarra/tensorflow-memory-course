---
id: pmle-02-collaborate-manage-data-models
title: "Certificazione PMLE - Dominio 2: collaborare per gestire dati e modelli"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: [pmle-01-architect-low-code-ai-solutions]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# Certificazione PMLE — Dominio 2: collaborare per gestire dati e modelli

!!! note "Stato: contenuto verificato su fonte primaria"
    Contenuto verificato parola per parola contro la exam guide ufficiale
    Google Cloud, fornita direttamente dallo studente. Nessun claim
    supplementare non verificato in questa lezione — a differenza del
    Dominio 1, qui non sono stati aggiunti dettagli di sintassi di
    prodotto oltre a quanto la guida stessa afferma.

## Cosa copre questo dominio

Il Dominio 2 ("Collaborating within and across teams to manage data and
models", **~16% dell'esame**) copre il lavoro che precede l'addestramento
su larga scala, in tre fasi: preparare i dati, prototipare in notebook,
tracciare gli esperimenti. È il dominio con il focus più esplicito sulla
**collaborazione tra ruoli** (data engineer, ML engineer, altri team) dei
sei.

## Teoria essenziale

### 2.1 — Esplorare e preprocessare i dati

Quattro attività: organizzare tipi di dato diversi (tabellare, testo,
immagini) per experimenting/training/serving efficienti; scegliere lo
strumento di preprocessing in base a **scala e complessità** dei dati
(BigQuery/SQL quando i dati sono già in un warehouse, Dataflow o Apache
Spark per pipeline distribuite più grandi, framework Python in-memoria
quando il dataset sta in RAM); creare e consolidare feature riutilizzabili
nel Feature Store di Gemini Enterprise Agent Platform; garantire privacy
dei dati e gestione delle informazioni sensibili (PII).

Il criterio esplicito della guida è la **scala**: lo stesso problema di
preprocessing richiede uno strumento diverso a seconda di quanti dati ci
sono e di dove vivono già. Non esiste uno strumento "sempre giusto".

### 2.2 — Prototipare modelli in notebook

Prima di investire in una pipeline di training strutturata, si prototipa:
applicando pratiche di collaborazione e sicurezza nella configurazione
dell'ambiente notebook (Gemini Enterprise Agent Platform Workbench o
Colab Enterprise); sviluppando con framework comuni (PyTorch, sklearn,
JAX); usando modelli fondazionali o open-source già disponibili in Model
Garden per creare un prototipo veloce, prima di scalare.

Nota l'ordine delle considerazioni nella guida: la sicurezza e la
collaborazione vengono **prima** della scelta del framework. Un notebook
prototipale condiviso male (credenziali nel codice, ambiente non isolato)
è un rischio anche in fase di semplice esplorazione.

### 2.3 — Tracciare ed eseguire esperimenti

Tre attività: scegliere l'ambiente giusto per sviluppo/sperimentazione in
base al framework usato (Experiments su Agent Platform, Agent Platform
Pipelines, Kubeflow Pipelines); valutare soluzioni predittive e generative
con metriche appropriate — incluso "LLM-as-a-judge", una tecnica per
valutare output generativi difficili da misurare con metriche numeriche
classiche; tracciare e confrontare artefatti, versioni e lineage dei
modelli (Experiments su Agent Platform, Agent Platform ML Metadata).

Il filo conduttore delle tre sottosezioni segue l'ordine reale di un
progetto: prepari i dati (2.1), prototipi velocemente (2.2), tieni
traccia di cosa hai provato (2.3) — così un collega, o tu stesso tra sei
mesi, può ripetere o confrontare un esperimento senza rifare tutto da
capo.

### Collegamento al corso principale

Le Lezioni 1-5 del corso principale (missing values, duplicati, split
train/val/test, leakage, encoding) sono esattamente il tipo di lavoro
descritto nella sottosezione 2.1, fatto con pandas invece che con BigQuery
o Dataflow: lo stesso ragionamento su qualità dei dati e separazione
train/val/test si applica indipendentemente dallo strumento — cambia la
scala, non il principio.

## Scenari di ragionamento

(Dettagliati in `knowledge/pmle-02-collaborate-manage-data-models/examples.md`.)

- 2 TB di log testuali da trasformare in feature, dati che non stanno in
  memoria su una macchina → uno strumento distribuito (Dataflow o Apache
  Spark), non un framework Python in-memoria: la scelta segue scala e
  complessità, non abitudine.
- Verificare in mezza giornata se un modello open-source da Model Garden è
  ragionevolmente preciso, prima di investire settimane in una pipeline
  completa → prototipo in notebook condiviso (Workbench o Colab
  Enterprise).
- Due membri del team hanno provato due configurazioni di iperparametri
  diverse senza coordinarsi → senza tracking (Experiments, ML Metadata)
  non si può confrontare in modo affidabile quale modello ha usato quali
  dati e parametri.

## Errori comuni

- Scegliere uno strumento di preprocessing per abitudine invece che in
  base a scala e complessità dei dati.
- Prototipare in notebook senza pratiche di collaborazione e sicurezza:
  la guida le elenca prima ancora dei framework usati.
- Saltare il tracking degli esperimenti perché "si ricorda a mente" quale
  configurazione ha dato quale risultato — non scala oltre un singolo
  esperimento.
- Trattare la gestione delle informazioni sensibili (PII) come un passo
  successivo, anziché parte della fase di esplorazione dati stessa.

## Quiz

1. Un team deve preprocessare 2 TB di log testuali che non stanno in
   memoria su una singola macchina. Quale criterio della guida determina
   lo strumento giusto, e cosa sceglierebbe?
2. Perché la guida elenca le pratiche di sicurezza e collaborazione prima
   ancora dei framework, nella sottosezione sulla prototipazione in
   notebook?
3. Due esperimenti diversi hanno dato risultati diversi, ma nessuno dei
   due autori ricorda esattamente quale configurazione ha usato. Quale
   sottosezione del Dominio 2 indirizza direttamente questo problema, e
   come?

<details>
<summary><b>Apri le risposte</b></summary>

1. Il criterio è la **scala e complessità** dei dati. Con 2 TB che non
   stanno in memoria, la scelta è uno strumento distribuito come Dataflow
   o Apache Spark, non un framework Python in-memoria.
2. Perché un ambiente di prototipazione mal configurato (credenziali nel
   codice, ambiente condiviso senza isolamento) è un rischio già in fase
   di esplorazione, prima ancora che il modello esista: la sicurezza non
   è un dettaglio da aggiungere dopo.
3. La sottosezione 2.3 (tracciare ed eseguire esperimenti): tracciare e
   confrontare artefatti, versioni e lineage dei modelli (con strumenti
   come Experiments o ML Metadata) è la condizione per poter confrontare
   due esperimenti in modo affidabile, invece di affidarsi alla memoria.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
