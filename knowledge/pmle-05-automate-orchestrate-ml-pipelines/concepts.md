# Concepts: pmle-05-automate-orchestrate-ml-pipelines

Decisione research: contenuto `VERIFIED` contro il testo verbatim della
exam guide ufficiale (vedi evidence.yaml). Un solo concetto generale
(CI/CD/CT) è spiegato con conoscenza MLOps generale, non da
documentazione di prodotto.

## Concetti coperti

1. Il Dominio 5 ("Automating and orchestrating ML pipelines", **~18% del
   peso**) copre come rendere **ripetibile e automatico** l'intero
   percorso dati → training → serving, invece di eseguirlo a mano ogni
   volta.
2. Sottosezione 5.1 — **sviluppare pipeline end-to-end**: validare dati e
   modelli (controllare automaticamente che i nuovi dati e il nuovo
   modello rispettino certe soglie di qualità prima di procedere);
   costruire e orchestrare pipeline usando servizi gestiti o non gestiti,
   da template o soluzioni custom (Agent Platform Pipelines per
   orchestrazione gestita nativa, Managed Service for Apache Airflow per
   orchestrazione più generale, Ray on Gemini Enterprise Agent Platform
   per carichi di calcolo distribuito); garantire preprocessing dei dati
   **coerente** tra training e serving (lo stesso tema del training-
   serving skew visto nel Dominio 4, qui affrontato a livello di
   pipeline).
3. Sottosezione 5.2 — **automatizzare il retraining**: determinare una
   policy di retraining appropriata (quando ha senso riaddestrare: a
   intervalli fissi, quando arrivano abbastanza dati nuovi, quando le
   metriche di produzione peggiorano); distribuire modelli in pipeline
   CI/CD/CT (continuous integration, continuous delivery, continuous
   training), con Cloud Build citato come esempio.

## Il filo conduttore del dominio

Le due sottosezioni rispondono a: *come costruisco una pipeline che
esegue automaticamente l'intero percorso, in modo affidabile?* (5.1),
*come faccio in modo che quella pipeline si riattivi da sola quando serve,
senza intervento manuale?* (5.2). Il tema centrale è **automazione con
controllo**: non basta automatizzare, bisogna anche validare a ogni
passo, altrimenti si automatizza anche la propagazione di un errore.

## Collegamento al resto del corso

Il corso principale costruisce l'intero percorso dati → feature → modello
→ valutazione **manualmente**, un notebook per volta (Lezioni 1-15): ogni
passo viene eseguito ed esaminato dallo studente. Il Dominio 5 tratta
esattamente la trasformazione di quel percorso manuale in una pipeline
automatica e ripetibile — la stessa logica (split train/val/test,
controllo di leakage, valutazione prima di accettare un modello) deve
valere anche quando nessuno esegue i passi a mano.

## Limiti

Questa lezione non tratta la sintassi di Kubeflow Pipelines, Airflow o
Cloud Build: la exam guide elenca questi come **strumenti da saper
scegliere**, non fornisce dettagli implementativi. Il concetto di CI/CD/CT
è spiegato con conoscenza MLOps generale, non specifica di Google Cloud
(vedi evidence.yaml). "Ray on Gemini Enterprise Agent Platform" è citato
esattamente come lo nomina la guida, senza dettagli implementativi non
verificabili (prodotto troppo recente per conoscenza pre-addestramento
affidabile, vedi `course/research_gaps.md`).
