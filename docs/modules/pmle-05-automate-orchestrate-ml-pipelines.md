---
id: pmle-05-automate-orchestrate-ml-pipelines
title: "Certificazione PMLE - Dominio 5: automatizzare e orchestrare pipeline ML"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
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
    CI/CD/CT è spiegato con conoscenza MLOps generale, non da
    documentazione di prodotto — segnalato dove compare.

## Cosa copre questo dominio

Il Dominio 5 ("Automating and orchestrating ML pipelines", **~18%
dell'esame**) copre come rendere **ripetibile e automatico** l'intero
percorso dati → training → serving, invece di eseguirlo a mano ogni
volta.

## Teoria essenziale

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

## Scenari di ragionamento

(Dettagliati in `knowledge/pmle-05-automate-orchestrate-ml-pipelines/examples.md`.)

- Una pipeline notturna riceve dati corrotti da una fonte a monte → senza
  un passo di validazione dati prima del training, la pipeline
  addestrerebbe e distribuirebbe automaticamente un modello su dati
  rotti.
- Un modello di raccomandazione perde accuratezza gradualmente → una
  policy di retraining basata su una soglia di calo delle metriche, non
  solo su un intervallo fisso.
- Preprocessing scritto due volte (training e serving) con una media
  diversa per la normalizzazione → il modello riceve in produzione input
  sistematicamente diversi da quelli di training.

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

## Quiz

1. Una pipeline automatica riaddestra un modello ogni notte su nuovi
   dati. Un giorno i dati in ingresso sono corrotti. Cosa dovrebbe
   impedire alla pipeline di distribuire comunque un modello addestrato
   su quei dati?
2. Perché "quando riaddestrare" è una competenza distinta da "come
   riaddestrare", secondo la sottosezione 5.2?
3. Cosa aggiunge "CT" (continuous training) rispetto al CI/CD tradizionale
   del software?

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

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
