---
id: pmle-01-architect-low-code-ai-solutions
title: "Certificazione PMLE - Dominio 1: architettare soluzioni AI low-code"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: []
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
  - https://cloud.google.com/bigquery/docs/bqml-introduction
---

# Certificazione PMLE — Dominio 1: architettare soluzioni AI low-code

!!! note "Stato: contenuto principale verificato su fonte primaria"
    Il contenuto di questa lezione (pesi dei domini, sottosezioni 1.1 e
    1.2, terminologia "Gemini Enterprise Agent Platform") è verificato
    parola per parola contro il testo della exam guide ufficiale Google
    Cloud, fornito direttamente dallo studente. Un solo dettaglio
    supplementare — la sintassi SQL esatta di BigQuery ML (`CREATE
    MODEL`, `ML.PREDICT`) — resta da riverificare sulla documentazione di
    prodotto corrente, non raggiungibile da questa sessione di lavoro; è
    segnalato dove compare. Dettaglio in `course/research_gaps.md`.

## Cosa copre questo modulo

Un blocco **supplementare e facoltativo**, fuori dalla progressione
obbligatoria del corso (che resta: dati → tensori → Keras → embedding →
memoria → Transformer → LoRA → pipeline → capstone). Copre la letteratura
ufficiale della certificazione *Professional Machine Learning Engineer*
(PMLE) di Google Cloud: teoria pura, **nessun notebook, nessuna
credenziale cloud**, coerente con il principio del corso di non richiedere
mai accesso a servizi a pagamento per progredire.

L'esame valuta sei domini (fonte: exam guide ufficiale, pesi verificati
verbatim):

1. **Architecting low-code AI solutions** (~13%) — questo modulo;
2. Collaborating within and across teams to manage data and models (~16%);
3. Scaling prototypes into ML models (~21%);
4. Serving and scaling models (~20%);
5. Automating and orchestrating ML pipelines (~18%);
6. Monitoring AI solutions (~13%).

## Teoria essenziale

### La domanda che il Dominio 1 valuta

Non "sai scrivere un modello?", ma **"sai riconoscere quando non serve
scriverlo?"**. Il corso principale di questo repository insegna a
costruire un classificatore da zero (prima con NumPy, poi con Keras)
proprio per capire cosa succede dentro un modello. Il Dominio 1 dell'esame
valuta la competenza complementare: scegliere lo strumento gestito giusto
quando il problema è già coperto da un servizio, per non spendere tempo di
sviluppo dove non serve.

### Sottosezione 1.1 — Sviluppare modelli con BigQuery ML o AutoML

La exam guide elenca cinque attività per questa sottosezione: costruire
modelli in BigQuery ML o Agent Platform AutoML (classificazione,
regressione, forecasting, clustering) in base al problema di business;
fare feature engineering o selezione con BigQuery ML; generare predizioni
con BigQuery ML; addestrare modelli con Agent Platform AutoML; fare
fine-tuning di modelli Gemini con BigQuery.

Il filo conduttore: **BigQuery ML** addestra e serve modelli con
istruzioni SQL, dentro lo stesso data warehouse dove i dati già vivono —
senza spostarli in un notebook o in una pipeline separata. Indicato
quando i dati sono già in BigQuery, il problema è tabellare o una serie
storica, e il team ha competenze SQL più che Python. Il vantaggio non è
"meno matematica", è **meno movimento di dati e meno infrastruttura da
gestire**.

**AutoML** (su Agent Platform) addestra modelli su dati tabellari,
immagini, testo o video senza che tu definisca l'architettura: il
servizio gestisce ricerca dell'architettura e tuning degli iperparametri.
Indicato quando serve un modello di produzione e il team non ha (o non
vuole investire) competenze specialistiche di deep learning per quel
compito specifico. È il punto esatto in cui il Dominio 1 tocca ciò che il
corso principale insegna a mano: le Lezioni 6-15 costruiscono un
classificatore Keras passo per passo per capire *come* funziona un
modello; qui la domanda è *quando* quella costruzione manuale non è la
scelta giusta per il contesto aziendale.

### Sottosezione 1.2 — Soluzioni AI con API o modelli fondazionali

Quattro attività verificate: valutare e scegliere il modello giusto da
**Gemini Enterprise Agent Platform Model Garden**; costruire applicazioni
con API di settore (Document AI, Vision, Translate); costruire soluzioni
e fare tuning di modelli per casi d'uso specifici (Gemini, Imagen, Veo, o
modelli come servizio in Model Garden); ottimizzare applicazioni basate
su Gemini per **costo, latenza e disponibilità**.

Quando il compito rientra in capacità generiche già coperte da un modello
esistente (comprensione del linguaggio, visione, generazione), la scelta
a minimo codice è integrare, non addestrare. Qui il vincolo di
progettazione non è più solo "funziona?", ma costo, latenza e
disponibilità: un'integrazione che chiama un modello enorme per un
compito semplice può essere corretta funzionalmente e sbagliata
economicamente. L'esame valuta esplicitamente questo trade-off, non solo
la correttezza dell'integrazione.

### Una nota sulla terminologia

La exam guide usa sistematicamente "Gemini Enterprise Agent Platform"
(spesso abbreviato "Agent Platform" nei singoli bullet) come nome della
piattaforma gestita — il nome usato in edizioni precedenti della guida per
lo stesso ambito era "Vertex AI". Questa lezione usa la terminologia
esatta della guida attuale. Il rapporto storico preciso tra i due nomi non
è affermato dalla guida stessa e non viene quindi affermato qui.

### Il criterio di scelta, in una frase

Per ogni scenario del Dominio 1, la domanda guida è: *qual è lo strumento
con il minimo codice sufficiente a risolvere questo specifico problema,
dati i vincoli di dove stanno i dati, che competenze ha il team, e quanto
costa servirlo?* Non esiste una risposta universale — esiste il criterio
per arrivarci.

## Scenari di ragionamento

(Dettagliati in `knowledge/pmle-01-architect-low-code-ai-solutions/examples.md`.)

- Storico vendite già in BigQuery, previsione trimestrale per prodotto →
  BigQuery ML con un modello di forecasting, non l'esportazione dei dati.
- Classificazione di immagini prodotto (difettoso/integro), nessun team
  di computer vision, poche migliaia di immagini etichettate → AutoML per
  immagini, non una rete convoluzionale scritta da zero.
- Riassunto di ticket di supporto, compito generico di linguaggio →
  integrazione di un modello fondazionale esistente da Model Garden,
  valutando costo/latenza, non addestramento dedicato.

## Errori comuni

- Scegliere sempre la soluzione custom per abitudine, anche quando uno
  strumento gestito basta e costa meno tempo.
- Confondere "basso codice" con "nessuna competenza richiesta": scegliere
  bene richiede comunque capire il tipo di problema e i vincoli di
  costo/latenza.
- Trattare la sintassi SQL esatta di BigQuery ML come materiale d'esame
  verificato: la guida valuta l'attività svolta, non i nomi di istruzione
  precisi (vedi riquadro in cima alla pagina).

## Quiz

1. Un'azienda ha dati di vendita tabellari già in BigQuery e vuole un
   modello di forecasting. Quale strumento ha il minor costo di sviluppo,
   e perché?
2. Perché "basso codice" non significa "nessuna competenza richiesta"?
3. Un'integrazione con un modello fondazionale esistente è funzionalmente
   corretta ma molto costosa per un compito semplice. È comunque la scelta
   giusta secondo i criteri di questo dominio?

<details>
<summary><b>Apri le risposte</b></summary>

1. BigQuery ML: i dati non devono uscire dal warehouse, e il problema
   (serie storica tabellare) è esattamente il caso d'uso elencato nella
   sottosezione 1.1 della exam guide.
2. Perché scegliere tra BigQuery ML, AutoML e un modello fondazionale
   richiede comunque capire il tipo di problema (classificazione vs
   forecasting vs compito generico di linguaggio) e i vincoli operativi
   (dove sono i dati, costo, latenza): il "basso codice" riduce lo sforzo
   di implementazione, non la necessità di capire il problema.
3. No: la sottosezione 1.2 valuta esplicitamente costo, latenza e
   disponibilità come vincoli di progettazione, non solo la correttezza
   funzionale. Una soluzione che funziona ma costa troppo per il compito
   non è la scelta giusta.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
- Google Cloud, *BigQuery ML introduction* (da riverificare per i
  dettagli di sintassi supplementari, vedi riquadro in cima alla pagina):
  https://cloud.google.com/bigquery/docs/bqml-introduction
