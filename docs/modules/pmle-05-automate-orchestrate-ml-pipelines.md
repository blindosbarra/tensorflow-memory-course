---
id: pmle-05-automate-orchestrate-ml-pipelines
title: "Certificazione PMLE - Dominio 5: automatizzare e orchestrare pipeline ML"
module: gcp-ml-certification
status: writing
estimated_minutes: 35
prerequisites: [pmle-04-serve-and-scale-models]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# Certificazione PMLE — Dominio 5: automatizzare e orchestrare pipeline ML

!!! note "Stato: contenuto verificato su fonte primaria"
    Contenuto verificato parola per parola contro la exam guide ufficiale
    Google Cloud, fornita direttamente dallo studente. Il concetto di
    CI/CD/CT, un esempio concreto di definizione di pipeline con l'SDK
    Kubeflow, i criteri di scelta tra Kubeflow Pipelines su GKE e Agent
    Platform Pipelines, e i dettagli implementativi di compilazione/
    sottomissione/trigger di una pipeline e di CI/CD con Cloud Build sono
    spiegati con conoscenza MLOps generale, non da documentazione di
    prodotto — segnalati dove compaiono.

## Cosa copre questo dominio

Il Dominio 5 ("Automating and orchestrating ML pipelines", **~18%
dell'esame**) copre come rendere **ripetibile e automatico** l'intero
percorso dati → training → serving, invece di eseguirlo a mano ogni
volta.

## Teoria essenziale

Finora Nordica ha eseguito ogni passo a mano: un analista lancia la query
di preprocessing, un altro avvia il training, un terzo controlla le
metriche prima di aggiornare l'endpoint. Il Dominio 5 tratta cosa succede
quando questo percorso deve ripetersi ogni settimana senza che nessuno lo
esegua manualmente.

### 5.1 — Sviluppare pipeline end-to-end

Tre considerazioni: **validare** dati e modelli — controllare
automaticamente che i nuovi dati e il nuovo modello rispettino certe
soglie di qualità prima di procedere; costruire e orchestrare pipeline
usando servizi gestiti o non gestiti, da template o soluzioni custom
(Gemini Enterprise Agent Platform Pipelines per orchestrazione gestita
nativa, Managed Service for Apache Airflow per orchestrazione più
generale, Ray on Gemini Enterprise Agent Platform per carichi
distribuiti); garantire preprocessing dei dati **coerente** tra training
e serving — lo stesso tema del training-serving skew visto nel Dominio 4,
qui affrontato a livello di pipeline.

**Nordica, concretamente.** La pipeline che riaddestra il modello di
rinnovo contratti ogni settimana è una sequenza di passi collegati (query
di preprocessing su BigQuery → training → valutazione → deploy), ognuno
rappresentato come un **componente** con input e output ben definiti —
questo è ciò che uno strumento come Agent Platform Pipelines o Kubeflow
Pipelines orchestra: esegue i componenti nell'ordine giusto, passa
l'output di uno come input al successivo, e riprende da dove si era
fermato se un passo fallisce, invece di dover far ripartire tutto a mano.
Una notte, la fonte a monte dei dati ordini invia un file corrotto (metà
delle righe con valori nulli dove non dovrebbero esserci). Senza un passo
di **validazione dati** prima del training, la pipeline procederebbe
comunque, addestrerebbe un modello su dati rotti, e lo distribuirebbe
automaticamente in produzione — l'automazione avrebbe propagato l'errore
invece di bloccarlo. Con un passo di validazione (soglie su percentuale
di valori nulli, range atteso dei valori), la pipeline si ferma prima e
avvisa il team.

!!! info "Come si scrive davvero una pipeline (con estrazione feature), e Kubeflow vs Agent Platform Pipelines"
    **La pipeline di Nordica, come componenti concreti.** Una pipeline
    non è un concetto astratto: è un grafo di funzioni, ciascuna con
    input/output tipizzati, scritte con l'SDK di Kubeflow Pipelines (che
    sia poi eseguita su Kubeflow su GKE o su Agent Platform Pipelines
    cambia solo il motore di esecuzione, non come si scrive la pipeline):

    ```python
    from kfp import dsl

    @dsl.component
    def valida_dati(dataset_raw: str) -> str:
        # controlla soglie: % nulli, range attesi; solleva errore se falliscono
        ...

    @dsl.component
    def estrai_feature(dataset_validato: str) -> str:
        # legge dal Feature Store (Dominio 2): spesa_mensile_eur,
        # ticket_aperti_90gg, mesi_da_attivazione, con lettura point-in-time
        # corretta rispetto alla data dell'etichetta
        ...

    @dsl.component
    def addestra(feature_table: str) -> str:
        # CREATE MODEL ... OPTIONS(model_type='BOOSTED_TREE_CLASSIFIER', ...)
        ...

    @dsl.component
    def valuta(modello: str) -> float:
        # ML.EVALUATE -> restituisce recall (metrica scelta nel Dominio 1
        # per l'asimmetria costo falsi positivi/negativi)
        ...

    @dsl.pipeline(name="rinnovo-contratti-settimanale")
    def pipeline_rinnovo(dataset_raw: str):
        dati_ok = valida_dati(dataset_raw=dataset_raw)
        feature = estrai_feature(dataset_validato=dati_ok.output)
        modello = addestra(feature_table=feature.output)
        metrica = valuta(modello=modello.output)
        with dsl.If(metrica.output > 0.65):
            # deploy solo se il recall supera la soglia di qualità
            ...
    ```

    Ogni funzione decorata `@dsl.component` è un nodo del grafo; il
    motore di orchestrazione legge le dipendenze dai parametri (es.
    `estrai_feature` dipende dall'output di `valida_dati`) e le esegue
    nell'ordine giusto, salvando ogni output come artefatto tracciabile —
    questo è anche ciò che rende possibile il tracking del Dominio 2
    (Experiments, ML Metadata): ogni run della pipeline produce una
    lineage completa di quali dati, quale codice, quale modello.

    **Kubeflow Pipelines (su GKE) vs Agent Platform Pipelines: quale
    scegliere.** Non sono alternative equivalenti, sono un trade-off tra
    controllo e gestione:

    - **Agent Platform Pipelines** (motore di esecuzione gestito
      nativamente da Google Cloud): nessun cluster da amministrare, si
      integra direttamente con gli altri servizi Agent Platform (Feature
      Store, Model Registry, Experiments) senza configurazione aggiuntiva,
      scala automaticamente. La scelta di default per un team come quello
      di Nordica, già interamente su Google Cloud, che non vuole gestire
      infrastruttura Kubernetes.
    - **Kubeflow Pipelines su GKE** (lo stesso SDK, ma eseguito su un
      cluster Kubernetes che il team gestisce): serve quando servono cose
      che un servizio gestito non offre — portabilità multi-cloud o
      on-premise (lo stesso codice di pipeline gira su GKE, su un altro
      cloud, o in un datacenter aziendale), controllo fine sulla
      configurazione del cluster (tipi di nodo, scheduling di GPU
      specifiche, policy di rete custom), o competenze Kubernetes già
      presenti in azienda che il team vuole sfruttare.

    In pratica: stessa sintassi delle pipeline (SDK Kubeflow), motore di
    esecuzione diverso. La domanda da farsi non è "quale strumento è
    migliore" ma "il mio team ha bisogno del controllo extra di gestire
    Kubernetes, o preferisce che Google lo gestisca al posto suo?".
    **Stato: needs_reverification** (sintassi SDK semplificata a scopo
    didattico, non testata contro una versione reale della libreria;
    criteri di scelta Kubeflow-vs-Agent-Platform-Pipelines sono
    ragionamento generale sul trade-off gestito-vs-self-managed, non
    affermazioni verificate su documentazione live in questa sessione).

!!! info "Come si esegue davvero una pipeline, e cosa la fa partire senza intervento umano"
    Scrivere la pipeline (sopra) è solo metà del lavoro: qualcosa deve
    **compilarla, sottometterla, e farla partire al momento giusto** —
    la guida nomina "orchestrare pipeline" ma non questi tre passi
    separati.

    **Compilazione e sottomissione.** Il codice Python della pipeline
    viene compilato in una definizione portabile (un file JSON/YAML che
    descrive il grafo di componenti, indipendente dal motore che poi lo
    esegue), che viene poi sottomessa specificando una **pipeline root**
    (un bucket Cloud Storage dove salvare gli artefatti intermedi tra un
    componente e il successivo — le tabelle di feature, il modello
    addestrato, le metriche) e i valori dei parametri di quella run
    specifica (es. quale `dataset_raw` usare questa settimana).

    **Cosa fa davvero partire la pipeline.** Una pipeline non si esegue
    da sola: serve un **trigger**, e ce ne sono di due tipi diversi a
    seconda della policy scelta (Dominio 5.2, sotto). Per un retraining a
    **intervallo fisso** (es. ogni lunedì alle 3:00), un job pianificato
    tipo cron avvia la pipeline a orari prestabiliti. Per un retraining
    **guidato da evento** (es. "appena arriva un nuovo file di dati
    grezzi"), un trigger event-driven osserva un evento specifico (es. un
    nuovo file caricato su un bucket Cloud Storage) e avvia
    automaticamente una nuova run della pipeline in risposta — utile
    quando i dati arrivano a intervalli irregolari e aspettare il
    prossimo slot pianificato sprecherebbe tempo.

    **Stato: needs_reverification** — meccanica generale di compilazione/
    sottomissione/trigger di una pipeline gestita, conoscenza MLOps
    generale non specifica di un prodotto Google Cloud; nomi esatti di
    servizi e parametri non riverificati su documentazione live in questa
    sessione.

### 5.2 — Automatizzare il retraining

Due considerazioni: determinare una **policy di retraining** appropriata
— quando ha senso riaddestrare: a intervalli fissi, quando arrivano
abbastanza dati nuovi, o quando le metriche di produzione peggiorano
sotto una soglia; distribuire modelli in pipeline **CI/CD/CT**
(continuous integration, continuous delivery, continuous training), con
Cloud Build citato come esempio di strumento.

Sul termine CI/CD/CT (concetto MLOps generale, non specifico di un
prodotto): estende il CI/CD tradizionale del software (testare e
integrare automaticamente le modifiche al codice, poi distribuirle) con
una terza fase specifica di ML, il *continuous training*: riaddestrare
automaticamente un modello quando arrivano nuovi dati o si verifica una
condizione che lo giustifica.

**Nordica, concretamente.** Riaddestrare ogni notte è uno spreco: il
comportamento dei clienti business non cambia così in fretta, e ogni run
di training ha un costo di calcolo. Riaddestrare una volta al trimestre a
intervallo fisso rischia l'opposto: se l'accuratezza del modello crolla
dopo un cambiamento improvviso nel mercato (es. una nuova politica di
sconti dei concorrenti), il team lo scoprirebbe solo mesi dopo. La policy
che la sottosezione 5.2 chiede di scegliere è quindi basata su una soglia
di calo delle metriche in produzione (es. "riaddestra se l'AUC scende
sotto 0.75"), non su un calendario arbitrario: il *quando* riaddestrare è
una decisione a sé, distinta dal meccanismo tecnico di *come* farlo. Una
volta deciso che serve un nuovo training, la pipeline CI/CD/CT lo
esegue, valuta il nuovo modello, e lo distribuisce automaticamente solo
se supera le soglie di qualità del passo di validazione (5.1) — la "CT"
in più rispetto al CI/CD tradizionale del software.

!!! info "CI/CD/CT con Cloud Build, concretamente"
    La guida cita Cloud Build come esempio, senza mostrare come una
    pipeline di build si collega davvero al retraining automatico.

    **La sequenza di passi, concreta.** Un file di configurazione build
    definisce una sequenza di step eseguiti in un container: (1)
    eseguire i test automatici sul codice dei componenti della pipeline
    (lo stesso principio delle Lezioni 1-15 del corso principale, qui
    applicato al codice invece che ai dati); (2) ricompilare la
    definizione della pipeline (vedi sopra); (3) sottomettere/avviare la
    pipeline compilata. Questa sequenza si attiva **automaticamente**
    quando qualcuno modifica il codice della pipeline in un repository
    Git e fa push — chiudendo il cerchio tra "un data scientist cambia lo
    script di training o la logica di validazione" e "una nuova run di
    pipeline verifica quella modifica end-to-end", senza che nessuno
    debba ricordarsi di eseguirla a mano.

    **Cosa distingue questo dal "CT" della policy di retraining.** Sono
    due trigger diversi per due motivi diversi: un push di codice
    (CI/CD, questo riquadro) verifica che una *modifica al codice* non
    rompa la pipeline; una soglia di degrado delle metriche o un nuovo
    volume di dati (CT, sopra) verifica che il *modello* vada
    riaddestrato anche se il codice non è cambiato. Una pipeline matura
    ha bisogno di entrambi i trigger, non solo di uno.

    **Stato: needs_reverification** — sequenza generale di build/test/
    deploy applicata a una pipeline ML, conoscenza CI/CD/MLOps generale;
    nome e sintassi esatta del file di configurazione non riverificati su
    documentazione live in questa sessione.

### Il filo conduttore del dominio

Le due sottosezioni rispondono a: *come costruisco una pipeline che
esegue automaticamente l'intero percorso, in modo affidabile?* (5.1),
*come faccio in modo che quella pipeline si riattivi da sola quando
serve, senza intervento manuale?* (5.2). Il tema centrale è **automazione
con controllo**: non basta automatizzare, bisogna anche validare a ogni
passo, altrimenti si automatizza anche la propagazione di un errore.

### Collegamento al corso principale

Il corso principale costruisce l'intero percorso dati → feature → modello
→ valutazione **manualmente**, un notebook per volta (Lezioni 1-15): ogni
passo viene eseguito ed esaminato dallo studente. Il Dominio 5 tratta
esattamente la trasformazione di quel percorso manuale in una pipeline
automatica e ripetibile — la stessa logica (split train/val/test,
controllo di leakage, valutazione prima di accettare un modello) deve
valere anche quando nessuno esegue i passi a mano.

## Errori comuni

- Automatizzare l'intera pipeline senza un passo di validazione prima di
  procedere: un errore a monte si propaga automaticamente invece di
  essere bloccato.
- Riaddestrare a un intervallo fisso arbitrario senza una policy motivata:
  spreca calcolo se il modello non ne ha bisogno, o lo lascia obsoleto se
  l'intervallo è troppo lungo.
- Scrivere il preprocessing due volte (training e serving) invece di
  condividere la stessa logica: causa comune di training-serving skew a
  livello di pipeline.
- Confondere CI/CD tradizionale con CI/CD/CT: la componente "CT"
  (continuous training) è specifica di ML e riguarda il modello stesso,
  non solo il codice che lo produce.
- Affidarsi a un solo tipo di trigger: solo un trigger pianificato (cron)
  non reagisce a un evento imprevisto (nuovi dati arrivati fuori
  programma); solo un trigger event-driven senza policy sulla soglia di
  degrado delle metriche non intercetta un modello che peggiora senza un
  evento esplicito ad avvisare.
- Trattare il trigger CI/CD (push di codice) e il trigger CT (soglia di
  degrado del modello) come lo stesso meccanismo: verificano cose
  diverse — che il codice non rompa la pipeline, e che il modello vada
  riaddestrato — e servono entrambi in una pipeline matura.

## Quiz

1. Una pipeline automatica riaddestra un modello ogni notte su nuovi
   dati. Un giorno i dati in ingresso sono corrotti. Cosa dovrebbe
   impedire alla pipeline di distribuire comunque un modello addestrato
   su quei dati?
2. Perché "quando riaddestrare" è una competenza distinta da "come
   riaddestrare", secondo la sottosezione 5.2?
3. Cosa aggiunge "CT" (continuous training) rispetto al CI/CD tradizionale
   del software?
4. Nordica vuole riaddestrare il modello ogni volta che arrivano abbastanza
   dati nuovi, non a un orario fisso. Che tipo di trigger serve, e perché
   un trigger pianificato (cron) non basterebbe?
5. Un data scientist corregge un bug nella logica di validazione dati
   della pipeline e fa push su Git. Cosa dovrebbe succedere
   automaticamente, e perché non basta aspettare il prossimo retraining
   pianificato per scoprire se la correzione funziona?

<details>
<summary><b>Apri le risposte</b></summary>

1. Un passo di validazione dei dati (e del modello) prima di procedere,
   come descritto nella sottosezione 5.1: la pipeline deve controllare la
   qualità dei dati/modello prima di distribuire, non solo eseguire i
   passi in sequenza.
2. Perché riaddestrare ha un costo (calcolo, tempo) che va giustificato:
   una policy di retraining (basata su una soglia di calo delle metriche
   o su volume di nuovi dati) decide *quando* ha senso farlo, mentre il
   meccanismo tecnico decide *come* farlo una volta deciso.
3. Il continuous training riaddestra automaticamente il modello stesso
   quando i dati o le condizioni lo richiedono; il CI/CD tradizionale
   testa e distribuisce solo modifiche al codice, non la componente
   "modello" che cambia con nuovi dati.
4. Serve un trigger event-driven, che osserva l'arrivo di nuovi dati (es.
   un nuovo file su Cloud Storage) e avvia la pipeline in risposta. Un
   trigger pianificato non basterebbe perché i dati arrivano a intervalli
   irregolari: aspettare il prossimo orario fisso sprecherebbe tempo se i
   dati sono già pronti, o riaddestrerebbe inutilmente se non lo sono
   ancora.
5. Dovrebbe attivarsi automaticamente una pipeline CI/CD che esegue i
   test sul codice, ricompila la pipeline e la sottomette — verificando
   la correzione end-to-end subito. Non basta aspettare il prossimo
   retraining pianificato perché quel trigger (CT, basato su soglie di
   degrado del modello o volume di dati) verifica una cosa diversa: se il
   *modello* va riaddestrato, non se una *modifica al codice* funziona
   correttamente.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
