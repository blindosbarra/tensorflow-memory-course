# Concepts: pmle-04-serve-and-scale-models

Decisione research: contenuto `VERIFIED` contro il testo verbatim della
exam guide ufficiale (vedi evidence.yaml). Un solo concetto generale
(A/B testing vs canary deployment) è spiegato con conoscenza generale di
deployment software, non da documentazione di prodotto.

## Concetti coperti

1. Il Dominio 4 ("Serving and scaling models", **~20% del peso**) copre
   cosa succede **dopo** che un modello è addestrato: come renderlo
   disponibile per fare predizioni, e come farlo scalare quando il
   traffico cresce.
2. Sottosezione 4.1 — **servire i modelli**: distribuire per inferenza
   batch (predizioni su grandi volumi, non in tempo reale) e online
   (predizioni su richiesta, in tempo reale) con il servizio giusto
   (Agent Platform, Model Garden, Cloud Run, GKE); pacchettizzare e
   servire modelli di framework diversi (PyTorch, XGBoost) con container
   predefiniti o personalizzati; organizzare e versionare i modelli in un
   registro centrale (Model Registry); implementare strategie di rollout
   per confrontare versioni (A/B testing, canary deployment); progettare
   pre/post-processing dell'inferenza (trasformare l'input prima della
   predizione, l'output dopo).
3. Sottosezione 4.2 — **scalare il serving online**: gestire e servire
   feature con il Feature Store (lo stesso del Dominio 2, qui usato in
   fase di serving per garantire coerenza con il training); distribuire
   modelli su endpoint pubblici o privati; scegliere l'hardware giusto
   (CPU, GPU, TPU, o edge — dispositivi periferici, non nel cloud);
   scalare il backend di serving in base al throughput; ottimizzare i
   modelli sia per il training sia per il serving in produzione.

## Il filo conduttore del dominio

Le due sottosezioni rispondono a: *come rendo disponibile il modello, in
modo sicuro e confrontabile con la versione precedente?* (4.1), *come
faccio scalare quel servizio quando il traffico cresce, senza sprecare
hardware?* (4.2). Un tema ricorrente è la **separazione tra correttezza e
scalabilità**: un modello che risponde bene a una richiesta non è
automaticamente pronto per migliaia di richieste al secondo.

## Collegamento al resto del corso

Il corso principale si ferma all'addestramento e alla valutazione di un
modello (Lezioni 10-13): il modello finale viene salvato
(`models/memory_type_classifier.keras`) ma non viene mai servito in
produzione. Il Dominio 4 copre esattamente il passo successivo che il
corso principale non tratta: cosa succede a quel file `.keras` una volta
che deve rispondere a richieste reali, con più utenti, con la necessità
di aggiornarlo senza interrompere il servizio.

## Limiti

Questa lezione non tratta la configurazione pratica di un endpoint, la
sintassi per pacchettizzare un container personalizzato, o i dettagli di
Model Registry: la exam guide elenca queste come **attività da saper
riconoscere**, non fornisce dettagli implementativi. La distinzione tra
A/B testing e canary deployment è spiegata con conoscenza generale di
software deployment, non specifica di Google Cloud (vedi evidence.yaml).
