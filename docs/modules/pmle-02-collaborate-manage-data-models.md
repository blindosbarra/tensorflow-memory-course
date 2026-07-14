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
    Google Cloud, fornita direttamente dallo studente. Alcuni dettagli
    supplementari — meccanica del Feature Store (entity type, lettura
    online/offline, correttezza point-in-time) e meccanica di un
    confronto SxS (AutoSxS come esempio concreto di "LLM-as-a-judge",
    inclusa la calibrazione autorater-umano) — sono stati aggiunti su
    richiesta dello studente con conoscenza generale pre-addestramento,
    non dalla guida stessa: restano da riverificare, segnalati dove
    compaiono.

## Cosa copre questo dominio

Il Dominio 2 ("Collaborating within and across teams to manage data and
models", **~16% dell'esame**) copre il lavoro che precede l'addestramento
su larga scala, in tre fasi: preparare i dati, prototipare in notebook,
tracciare gli esperimenti. È il dominio con il focus più esplicito sulla
**collaborazione tra ruoli** (data engineer, ML engineer, altri team) dei
sei.

## Teoria essenziale

### Nordica Commerce, di nuovo — ora servono dati puliti, un prototipo e una memoria condivisa

Riprendiamo "Nordica Commerce" dal Dominio 1: i due analisti hanno già in
produzione il modello di previsione domanda (BigQuery ML) e il
classificatore di foto difettose (AutoML). Ora il team cresce a cinque
persone e affronta un problema più grande: un modello che predica quali
clienti business rischiano di non rinnovare il contratto, usando anche il
testo dei ticket di assistenza. Le tre sottosezioni del Dominio 2 sono
esattamente le tre fasi che il team attraversa per arrivarci.

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

**Nordica, concretamente.** I ticket di assistenza (lo stesso testo che il
modello di riassunto del Dominio 1 elabora) sono 2 TB di log testuali su
tre anni — non stanno in memoria su una singola macchina. Provare a
caricarli in un notebook con pandas fallirebbe con un errore di memoria
esaurita molto prima di arrivare al training. La scelta secondo 2.1 è uno
strumento di elaborazione **distribuita** come Dataflow o Apache Spark,
che processa i dati a pezzi su più macchine invece di caricarli tutti
insieme: la scala del problema, non l'abitudine del team, determina lo
strumento. In più, quei ticket contengono nomi e indirizzi email dei
clienti — la fase di preprocessing è anche il punto in cui va applicata
la gestione delle informazioni sensibili (PII), non un passo da rimandare
a dopo l'addestramento.

!!! info "Come funziona davvero un Feature Store, concretamente (non solo il nome)"
    La guida nomina il Feature Store come luogo dove "creare e consolidare
    feature riutilizzabili", senza spiegare la meccanica. Ecco cosa
    significa in pratica, usando le feature del modello di rinnovo
    contratti già viste nel Dominio 1 (`spesa_mensile_eur`,
    `ticket_aperti_90gg`, `mesi_da_attivazione`):

    1. **Entity type**: la "cosa" a cui le feature si riferiscono — qui
       `cliente_b2b`, identificato da un ID cliente univoco. Ogni feature
       nel Feature Store appartiene a un entity type.
    2. **Feature**: un attributo nominato e tipizzato di un entity type,
       calcolato da una pipeline separata (es. un job giornaliero che
       conta i ticket aperti negli ultimi 90 giorni per ciascun cliente) e
       scritto nel Feature Store con un timestamp — non calcolato al volo
       ogni volta che serve.
    3. **Due percorsi di lettura, per due scopi diversi**: lettura
       **online**, a bassa latenza, per una singola entità alla volta —
       usata in fase di serving (Dominio 4) quando arriva una richiesta di
       predizione in tempo reale; lettura **offline/batch**, per
       costruire un intero dataset di training unendo le feature storiche
       di molti clienti insieme alle rispettive etichette.

    **Il punto tecnico che la guida non spiega ma è la ragione d'essere
    del Feature Store**: la lettura offline deve essere *point-in-time
    correct*. Se Nordica addestra il modello su un'etichetta "rinnovato/
    non rinnovato" registrata sei mesi fa, il valore di
    `ticket_aperti_90gg` usato per quella riga di training deve essere
    quello **calcolato a quella data**, non il valore odierno (che
    includerebbe ticket aperti nei sei mesi successivi — informazione che
    il modello non avrebbe mai potuto conoscere al momento della
    predizione reale). Usare il valore odierno per errore è una forma
    concreta di data leakage, la stessa categoria di errore vista nella
    Lezione 4 del corso principale, qui applicata a un sistema con
    feature che cambiano nel tempo invece che a uno split train/test
    statico. Il Feature Store risolve questo tenendo traccia dei valori
    storici con timestamp, non solo del valore corrente. **Stato:
    needs_reverification** (meccanica generale di un feature store,
    inclusa la distinzione online/offline e la correttezza point-in-time;
    non riverificata su documentazione live del prodotto specifico in
    questa sessione).

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

**Nordica, concretamente.** Prima di impegnare settimane su una pipeline
di training completa per il modello di rinnovo contratti, un data
scientist vuole sapere in mezza giornata se un modello già pronto (da
Model Garden) è anche solo ragionevolmente preciso su questo problema. La
risposta della sottosezione 2.2 è: prototipa in un notebook **condiviso**
(Workbench o Colab Enterprise), non in un file locale sul proprio laptop
— così un collega può riprendere il lavoro, rivedere il codice, e nessuna
credenziale finisce salvata solo sulla macchina di una persona. Se il
prototipo è promettente, si passa a una pipeline strutturata; se non lo
è, il team ha perso mezza giornata invece di due settimane.

### 2.3 — Tracciare ed eseguire esperimenti

Tre attività: scegliere l'ambiente giusto per sviluppo/sperimentazione in
base al framework usato (Experiments su Agent Platform, Agent Platform
Pipelines, Kubeflow Pipelines); valutare soluzioni predittive e generative
con metriche appropriate — incluso "LLM-as-a-judge", una tecnica per
valutare output generativi difficili da misurare con metriche numeriche
classiche; tracciare e confrontare artefatti, versioni e lineage dei
modelli (Experiments su Agent Platform, Agent Platform ML Metadata).

**Nordica, concretamente (parte 1 — tracking).** Due dei cinque membri del
team provano, in giorni diversi e senza coordinarsi, due configurazioni
diverse di iperparametri per il modello di rinnovo contratti. Una
settimana dopo nessuno dei due ricorda con certezza quale run ha usato
quali dati, quali parametri, quale versione del preprocessing. Senza un
sistema di tracking (Experiments, ML Metadata) questo confronto è
impossibile da fare con certezza — bisogna ri-eseguire tutto da capo per
saperlo. Tracciare artefatti, versioni e lineage non è un passo opzionale
di documentazione: è la condizione per poter dire "il modello B batte il
modello A" con dati alla mano.

**Nordica, concretamente (parte 2 — valutare l'output generativo).** Il
modello di riassunto ticket del Dominio 1 (Problema 3) genera testo, non
un numero o una categoria: non esiste un "accuracy" da calcolare come per
un classificatore. Qui entra "LLM-as-a-judge", nominato genericamente
dalla guida. Un esempio concreto di come funziona (**non nominato dalla
exam guide**, aggiunto qui come dettaglio supplementare da riverificare)
è **AutoSxS** ("Auto side-by-side"): si generano due riassunti dello
stesso ticket con due versioni del modello (es. prima e dopo un tuning),
si passano entrambi a un modello valutatore ("autorater") insieme al
ticket originale, e l'autorater sceglie quale dei due riassunti è
migliore — ripetuto su molti ticket produce una metrica di win-rate
("la versione B è preferita nel 68% dei casi") senza che una persona
debba leggere e giudicare ogni singolo confronto a mano.

!!! info "Cosa serve davvero per impostare un confronto SxS, e perché fidarsene"
    Un confronto side-by-side non è un singolo pulsante: ha tre
    ingredienti, e capire cosa sono aiuta a capire anche i suoi limiti.

    1. **Un dataset di valutazione**: un insieme di input rappresentativi
       (qui, ticket di assistenza reali, non inventati) su cui generare le
       risposte da confrontare — se il dataset non copre i casi che
       contano (es. ticket molto tecnici vs ticket generici), il risultato
       del confronto non generalizza a quei casi.
    2. **Le due risposte da confrontare**: tipicamente l'output del
       modello attuale in produzione (baseline) contro l'output di un
       candidato (es. dopo un tuning con LoRA, vedi Dominio 1) sugli
       stessi identici input — la coppia deve condividere l'input, non
       basta confrontare metriche aggregate calcolate separatamente.
    3. **Un template di valutazione per l'autorater**: le istruzioni che
       dicono al modello valutatore *su cosa* giudicare — per il
       riassunto ticket, potrebbe essere "quale dei due riassunti è più
       accurato rispetto al ticket originale e più conciso, a parità di
       informazione importante conservata". Cambiare questo template
       cambia cosa "vince" il confronto: un template che pesa solo la
       concisione premierebbe un riassunto troppo breve che perde
       dettagli importanti.

    **Perché fidarsi (con cautela) del giudizio automatico.** L'autorater
    è a sua volta un modello, quindi può sbagliare o avere bias sistematici
    (es. preferire risposte più lunghe a prescindere dalla qualità). La
    pratica di allineamento è calibrare l'autorater su un piccolo campione
    di confronti **giudicati anche da persone**, e verificare che
    l'accordo autorater-umano sia alto prima di fidarsi del risultato su
    larga scala — un confronto SxS senza questo passo di calibrazione è
    un giudizio automatico non verificato, non una metrica affidabile.
    **Stato: needs_reverification** (meccanica generale di valutazione
    pairwise con autorater, inclusa la pratica di calibrazione
    umano-autorater; nomi di prodotto specifici e dettagli di
    configurazione non riverificati su documentazione live in questa
    sessione).

Il filo conduttore delle tre sottosezioni segue l'ordine reale del
progetto di Nordica: preparare i dati (2.1), prototipare velocemente
(2.2), tenere traccia di cosa è stato provato e di come si misura se ha
funzionato (2.3) — così un collega, o lo stesso team tra sei mesi, può
ripetere o confrontare un esperimento senza rifare tutto da capo.

### Collegamento al corso principale

Le Lezioni 1-5 del corso principale (missing values, duplicati, split
train/val/test, leakage, encoding) sono esattamente il tipo di lavoro
descritto nella sottosezione 2.1, fatto con pandas invece che con BigQuery
o Dataflow: lo stesso ragionamento su qualità dei dati e separazione
train/val/test si applica indipendentemente dallo strumento — cambia la
scala, non il principio.

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
4. Cos'è AutoSxS, e perché non è materiale garantito dalla exam guide
   nello stesso modo degli altri concetti di questa lezione?

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
4. AutoSxS è uno strumento che confronta automaticamente gli output di
   due modelli usando un autorater (LLM-as-a-judge) per produrre metriche
   tipo win-rate. Non è materiale garantito dalla guida come gli altri
   concetti perché il nome "AutoSxS" non compare nel testo verbatim della
   exam guide: è stato aggiunto come esempio concreto della tecnica
   "LLM-as-a-judge" che la guida nomina genericamente, usando conoscenza
   generale pre-addestramento non riverificata in questa sessione.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
