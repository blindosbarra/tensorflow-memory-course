---
id: pmle-01-architect-low-code-ai-solutions
title: "Certificazione PMLE - Dominio 1: architettare soluzioni AI low-code"
module: gcp-ml-certification
status: evidence_review
estimated_minutes: 25
prerequisites: []
deliverables: []
sources:
  - https://cloud.google.com/learn/certification/machine-learning-engineer
  - https://cloud.google.com/bigquery/docs/bqml-introduction
  - https://cloud.google.com/vertex-ai/docs/beginner/beginners-guide
---

# Certificazione PMLE — Dominio 1: architettare soluzioni AI low-code

!!! warning "Stato: evidence_review, non done"
    Questa lezione copre solo i claim verificati su fonte ufficiale in
    questa sessione di lavoro. Due claim tecnici (sintassi BigQuery ML,
    meccanica AutoML) sono marcati "da riverificare": sono meccaniche
    stabili e ben documentate storicamente, ma non riletti sulla
    documentazione live in questa sessione (un blocco di rete
    dell'ambiente ha impedito l'accesso a `docs.cloud.google.com`). Il
    dettaglio è in `course/research_gaps.md`. Non è materiale sufficiente
    per affrontare l'esame da solo: è un punto di partenza verificabile,
    non una guida completa.

## Cosa copre questo modulo

Un blocco **supplementare e facoltativo**, fuori dalla progressione
obbligatoria del corso (che resta: dati → tensori → Keras → embedding →
memoria → Transformer → LoRA → pipeline → capstone). Copre letteratura di
prodotto Google Cloud per la certificazione *Professional Machine Learning
Engineer* (PMLE): teoria pura, **nessun notebook, nessuna credenziale
cloud**, coerente con il principio del corso di non richiedere mai
accesso a servizi a pagamento per progredire.

L'esame valuta sei domini (fonte: pagina di certificazione ufficiale
Google Cloud):

1. **Architect low-code AI solutions** — questo modulo;
2. Collaborate within and across teams to manage data and models;
3. Scale prototypes into ML models;
4. Serve and scale models;
5. Automate and orchestrate ML pipelines;
6. Monitor AI solutions.

I domini 2-6 non sono ancora coperti in questo repository (vedi
`course.yaml`, stato `planned`).

## Teoria essenziale

### La domanda che il Dominio 1 valuta

Non "sai scrivere un modello?", ma **"sai riconoscere quando non serve
scriverlo?"**. Il corso principale di questo repository insegna a
costruire un classificatore da zero (prima con NumPy, poi con Keras)
proprio per capire cosa succede dentro un modello. Il Dominio 1 dell'esame
valuta la competenza complementare: scegliere lo strumento gestito giusto
quando il problema è già coperto da un servizio, per non spendere tempo di
sviluppo dove non serve.

Tre famiglie di strumenti, con criteri di scelta diversi:

**BigQuery ML.** Addestri e servi modelli con istruzioni SQL, dentro lo
stesso data warehouse dove i dati già vivono — senza spostarli in un
notebook o in una pipeline separata. Indicato quando: i dati sono già in
BigQuery, il problema è tabellare o una serie storica (classificazione,
regressione, forecasting, clustering), e il team ha competenze SQL più che
Python. Il vantaggio non è "meno matematica", è **meno movimento di
dati e meno infrastruttura da gestire**.

**AutoML.** Addestri modelli su dati tabellari, immagini, testo o video
senza definire tu l'architettura: il servizio gestisce ricerca
dell'architettura e tuning degli iperparametri. Indicato quando serve un
modello di produzione e il team non ha (o non vuole investire) competenze
specialistiche di deep learning per quel compito specifico. È il punto
esatto in cui il Dominio 1 tocca ciò che il corso principale insegna a
mano: le Lezioni 6-15 costruiscono un classificatore Keras passo per passo
per capire *come* funziona un modello; qui la domanda è *quando* quella
costruzione manuale non è la scelta giusta per il contesto aziendale.

**API o modelli fondazionali già pronti.** Quando il compito rientra in
capacità generiche già coperte da un modello esistente (comprensione del
linguaggio, visione, generazione), la scelta a minimo codice è integrare,
non addestrare. Qui il vincolo di progettazione non è più solo
"funziona?", ma **costo, latenza e disponibilità**: un'integrazione che
chiama un modello enorme per un compito semplice può essere corretta
funzionalmente e sbagliata economicamente. L'esame valuta esplicitamente
questo trade-off, non solo la correttezza dell'integrazione.

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
  integrazione di un modello fondazionale esistente, valutando
  costo/latenza, non addestramento dedicato.

## Errori comuni

- Scegliere sempre la soluzione custom per abitudine, anche quando uno
  strumento gestito basta e costa meno tempo.
- Confondere "basso codice" con "nessuna competenza richiesta": scegliere
  bene richiede comunque capire il tipo di problema e i vincoli di
  costo/latenza.
- Dare per scontata l'equivalenza tra nomi di prodotto non verificati (vedi
  il riquadro di avvertenza in cima alla pagina).

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
   (serie storica tabellare) è esattamente il caso d'uso per cui BigQuery
   ML è indicato.
2. Perché scegliere tra BigQuery ML, AutoML e un modello fondazionale
   richiede comunque capire il tipo di problema (classificazione vs
   forecasting vs compito generico di linguaggio) e i vincoli operativi
   (dove sono i dati, costo, latenza): il "basso codice" riduce lo sforzo
   di implementazione, non la necessità di capire il problema.
3. No: il Dominio 1 valuta esplicitamente costo, latenza e disponibilità
   come vincoli di progettazione, non solo la correttezza funzionale. Una
   soluzione che funziona ma costa troppo per il compito non è la scelta
   giusta.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification*:
  https://cloud.google.com/learn/certification/machine-learning-engineer
- Google Cloud, *BigQuery ML introduction* (da riverificare, vedi avviso
  in cima alla pagina): https://cloud.google.com/bigquery/docs/bqml-introduction
- Google Cloud, *Vertex AI beginner's guide* (da riverificare, vedi avviso
  in cima alla pagina): https://cloud.google.com/vertex-ai/docs/beginner/beginners-guide
