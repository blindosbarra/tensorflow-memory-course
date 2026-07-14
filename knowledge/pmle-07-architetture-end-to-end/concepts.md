# Concepts: pmle-07-architetture-end-to-end

Decisione research: questa lezione **non** è un dominio verbatim della
exam guide (vedi evidence.yaml, claim `pmle07-not-exam-domain`). È una
sintesi didattica aggiunta su richiesta esplicita dello studente per
collegare i concetti dei sei domini in architetture concrete complete,
con troubleshooting e un confronto MLOps tradizionale vs generativo.

## Concetti coperti

1. Quattro architetture end-to-end, ciascuna scelta per coprire un tipo
   di dato/problema/pattern di serving diverso: dati tabellari per una
   decisione di business interna (previsione acquisto entro 30 giorni,
   batch), serie temporali con feature esterne (previsione pioggia,
   batch), immagini con team senza competenze ML (classificazione fiori
   via AutoML, edge), e un'applicazione di AI generativa (assistente
   clienti con RAG, online — l'unica delle quattro in tempo reale).
2. Un diagramma Mermaid per ciascuna architettura, con un richiamo
   esplicito ai cinque pilastri del Google Cloud Architecture Framework
   (eccellenza operativa, sicurezza/privacy/conformità, affidabilità,
   ottimizzazione dei costi, ottimizzazione delle prestazioni) applicati
   alle decisioni già descritte nel testo.
3. Per la quarta architettura (RAG): perché non serve addestrare nulla
   da zero (scala di costo del Dominio 1), un guardrail contro prompt
   injection (Dominio 6), valutazione via AutoSxS invece di una metrica
   fissa (Dominio 2), e un problema di troubleshooting specifico del RAG
   (indice di retrieval non aggiornato) presentato come analogo al
   training-serving skew del ML tradizionale.
4. Per ciascuna architettura, le stesse sette domande applicate in
   sequenza: dati e feature, scelta del modello/strumento, training e
   troubleshooting, pipeline, deploy, monitoraggio.
5. Overfitting e underfitting mostrati con tabelle numeriche costruite
   (non dati reali) per ciascuna delle due firme diagnostiche, invece di
   solo definirle a parole.
6. Uno sbilanciamento di classi (rose vs orchidee rare) usato per
   mostrare perché l'accuratezza aggregata multi-classe può nascondere
   un problema serio su una classe minoritaria.
7. Una tabella di troubleshooting generale (sintomo → diagnosi → cause →
   rimedi) che consolida overfitting, underfitting, un possibile bug di
   split train/validation, training-serving skew, drift, indice RAG
   obsoleto, e fallimenti di validazione dati in pipeline.
8. Un confronto esplicito, punto per punto, tra il ciclo di vita MLOps
   del ML tradizionale e quello dell'AI generativa (LLMOps): cosa si
   addestra/adatta, come si valuta, cosa si versiona, quando si
   riaddestra, cosa si monitora — ora ancorato a un'architettura
   concreta (la 4) invece di restare solo teorico.

## Collegamento alle lezioni di dominio

Ogni architettura riusa esplicitamente concetti già introdotti: Dominio 1
(model_type, TRANSFORM, tuning ladder), Dominio 2 (Feature Store,
AutoSxS/LLM-as-a-judge), Dominio 3 (interpretabilità come vincolo di
progettazione), Dominio 4 (batch vs online, edge), Dominio 5 (pipeline a
componenti, validazione dati, CI/CD/CT), Dominio 6 (Model Monitoring,
tipi di drift, Model Armor). Nessun concetto nuovo di prodotto viene
introdotto qui che non sia già stato citato in una lezione precedente.

## Collegamento al corso principale

Il playbook di troubleshooting rimanda esplicitamente alla Lezione 12
(regolarizzazione/dropout/early stopping, per l'overfitting) e alla
Lezione 3 (split train/validation/test, per il caso anomalo di una
metrica di validation migliore di quella di training).

## Limiti

Tutte le tabelle numeriche (AUC per iterazione, MAE, precision/recall
per classe) sono esempi didattici costruiti per essere internamente
coerenti, non output reali di BigQuery ML o AutoML — dichiarato
esplicitamente nel testo della lezione. I meccanismi generali sottostanti
(discesa del gradiente, transfer learning, trade-off edge/cloud) sono
conoscenza ML/MLOps generale, `needs_reverification` come nelle altre
lezioni del modulo.
