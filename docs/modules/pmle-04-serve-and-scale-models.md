---
id: pmle-04-serve-and-scale-models
title: "Certificazione PMLE - Dominio 4: servire e scalare i modelli"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: [pmle-03-scale-prototypes-into-ml-models]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# Certificazione PMLE — Dominio 4: servire e scalare i modelli

!!! note "Stato: contenuto verificato su fonte primaria"
    Contenuto verificato parola per parola contro la exam guide ufficiale
    Google Cloud, fornita direttamente dallo studente. La distinzione tra
    A/B testing e canary deployment è spiegata con conoscenza generale di
    software deployment, non da documentazione di prodotto — segnalata
    dove compare.

## Cosa copre questo dominio

Il Dominio 4 ("Serving and scaling models", **~20% dell'esame**) copre
cosa succede **dopo** che un modello è addestrato: come renderlo
disponibile per fare predizioni, e come farlo scalare quando il traffico
cresce.

## Teoria essenziale

### 4.1 — Servire i modelli

Cinque considerazioni: distribuire per **inferenza batch** (predizioni su
grandi volumi, non in tempo reale) e **online** (predizioni su richiesta,
in tempo reale) con il servizio giusto (Agent Platform, Model Garden,
Cloud Run, GKE); pacchettizzare e servire modelli di framework diversi
(PyTorch, XGBoost) con container predefiniti o personalizzati;
organizzare e versionare i modelli in un registro centrale (Gemini
Enterprise Agent Platform Model Registry); implementare strategie di
**rollout** per confrontare versioni (A/B testing, canary deployment);
progettare pre/post-processing dell'inferenza.

Sulla differenza tra le due strategie di rollout (concetto generale, non
specifico di un prodotto): in un **canary deployment**, una piccola
percentuale di traffico va alla nuova versione, per limitare il danno se
qualcosa non va prima di un rollout completo. In un **A/B testing**, il
traffico viene diviso in modo più esteso tra due versioni per un
confronto statistico dei risultati.

### 4.2 — Scalare il serving online

Cinque considerazioni: gestire e servire feature con l'Agent Platform
Feature Store (lo stesso del Dominio 2, qui usato in fase di serving per
garantire coerenza con il training); distribuire modelli su endpoint
pubblici o privati; scegliere l'hardware giusto (CPU, GPU, TPU, o
**edge** — dispositivi periferici, non nel cloud); scalare il backend di
serving in base al throughput (Gemini Enterprise Agent Platform
Inference, containerized serving); ottimizzare i modelli sia per il
training sia per il serving in produzione.

### Il filo conduttore del dominio

Le due sottosezioni rispondono a: *come rendo disponibile il modello, in
modo sicuro e confrontabile con la versione precedente?* (4.1), *come lo
faccio scalare quando il traffico cresce?* (4.2). Un tema ricorrente è la
**separazione tra correttezza e scalabilità**: un modello che risponde
bene a una richiesta non è automaticamente pronto per migliaia di
richieste al secondo.

### Collegamento al corso principale

Il corso principale si ferma all'addestramento e alla valutazione di un
modello (Lezioni 10-13): il modello finale viene salvato
(`models/memory_type_classifier.keras`) ma non viene mai servito in
produzione. Il Dominio 4 copre esattamente il passo successivo: cosa
succede a quel file `.keras` una volta che deve rispondere a richieste
reali, con più utenti, con la necessità di aggiornarlo senza interrompere
il servizio.

## Scenari di ragionamento

(Dettagliati in `knowledge/pmle-04-serve-and-scale-models/examples.md`.)

- Un milione di documenti da classificare una volta al mese vs un
  documento appena caricato da classificare in tempo reale → inferenza
  batch nel primo caso, online nel secondo.
- Una nuova versione di un modello di raccomandazione da verificare senza
  rischiare tutto il traffico → canary deployment per limitare il danno,
  A/B testing per un confronto statistico più esteso.
- Feature calcolate diversamente tra training e un servizio online →
  training-serving skew; usare lo stesso Feature Store in entrambe le
  fasi evita l'incoerenza.

## Errori comuni

- Usare inferenza online per un carico che è in realtà batch: più
  costoso e più lento di un job batch dedicato.
- Rilasciare una nuova versione di modello a tutto il traffico in un
  colpo solo, senza una strategia di rollout progressiva.
- Ricalcolare le feature in modo diverso tra training e serving invece di
  usare la stessa fonte in entrambe le fasi: causa training-serving skew,
  difficile da diagnosticare perché il modello sembra corretto ma
  performa peggio in produzione.
- Scegliere l'hardware di serving in base a cosa è stato usato in
  training, invece che in base al throughput e alla latenza richiesti in
  produzione.

## Quiz

1. Un'azienda deve classificare un milione di documenti archiviati una
   volta al mese, e separatamente un documento appena caricato da un
   utente. Quale tipo di inferenza per ciascun caso, e perché?
2. Qual è la differenza tra canary deployment e A/B testing come
   strategie di rollout?
3. Un modello performa bene in fase di valutazione ma peggio in
   produzione, pur essendo la stessa architettura e gli stessi pesi. Quale
   problema descritto in questa lezione potrebbe spiegarlo, e quale
   strumento del Dominio 4 lo previene?

<details>
<summary><b>Apri le risposte</b></summary>

1. Per il milione di documenti archiviati, inferenza batch: non serve una
   risposta immediata, ed è più economica per grandi volumi. Per il
   documento appena caricato, inferenza online: serve una risposta in
   tempo reale a bassa latenza su una singola richiesta.
2. Nel canary deployment una piccola percentuale di traffico va alla
   nuova versione, per limitare il danno potenziale prima di un rollout
   completo. Nell'A/B testing il traffico è diviso in modo più esteso
   tra due versioni per un confronto statistico dei risultati.
3. Training-serving skew: le feature vengono calcolate in modo
   leggermente diverso tra training e serving. Usare lo stesso Feature
   Store (Agent Platform Feature Store) sia in training sia in serving,
   come descritto nella sottosezione 4.2, previene questo tipo di
   incoerenza.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
