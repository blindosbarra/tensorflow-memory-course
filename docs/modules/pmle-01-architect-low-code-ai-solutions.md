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
    Pesi dei domini, sottosezioni 1.1/1.2 e terminologia "Gemini
    Enterprise Agent Platform" sono verificati parola per parola contro
    la exam guide ufficiale, fornita dallo studente. Un solo dettaglio —
    la sintassi SQL esatta di BigQuery ML (`CREATE MODEL`, `ML.PREDICT`)
    — resta da riverificare sulla documentazione di prodotto corrente,
    non raggiungibile da questa sessione; è segnalato dove compare.
    Dettaglio in `course/research_gaps.md`.

## Cosa copre questo modulo

Un blocco supplementare e facoltativo, fuori dalla progressione
obbligatoria del corso (che resta: dati → tensori → Keras → embedding →
memoria → Transformer → LoRA → pipeline → capstone). Copre la letteratura
ufficiale della certificazione *Professional Machine Learning Engineer*
di Google Cloud: teoria pura, nessun notebook, nessuna credenziale cloud.

L'esame valuta sei domini, con pesi ufficiali dalla exam guide: Architect
low-code AI solutions (~13%, questo modulo), Collaborate within and
across teams to manage data and models (~16%), Scale prototypes into ML
models (~21%), Serve and scale models (~20%), Automate and orchestrate
ML pipelines (~18%), Monitor AI solutions (~13%).

## Teoria essenziale

### Un'azienda, tre problemi

Immagina "Nordica Commerce", un e-commerce di medie dimensioni con due
analisti dati (bravi in SQL, non in deep learning) e nessun team ML
dedicato. In un trimestre affronta tre problemi diversi, che insieme
coprono l'intero Dominio 1.

### Problema 1: prevedere la domanda per prodotto

Lo storico ordini vive già in BigQuery — tre anni di dati, per SKU, per
settimana. Nordica vuole prevedere le vendite del prossimo trimestre per
decidere quanto riordinare.

L'alternativa "fai da te" sarebbe esportare quei dati verso un notebook,
allenare un modello ARIMA con pandas e statsmodels, e ripetere l'export a
mano ogni settimana quando arrivano nuovi ordini. Questo significa
costruire e mantenere una pipeline di export, tenere in piedi un ambiente
notebook aggiornato, e accettare che le previsioni siano vecchie di
qualche giorno rispetto ai dati più recenti.

BigQuery ML elimina tutti e tre questi costi: un `CREATE MODEL` di tipo
`ARIMA_PLUS` addestra direttamente sui dati che già vivono nel warehouse,
i due analisti lavorano nello stesso SQL che già conoscono, e le
previsioni sono aggiornate quanto la tabella sorgente. Questo è
esattamente ciò che la sottosezione 1.1 della exam guide chiama
"generating predictions using BigQuery ML" e "performing feature
engineering or selection using BigQuery ML": il vantaggio non è
matematico (BigQuery ML non fa niente che pandas non potrebbe fare), è
che i dati restano fermi e il team lavora con lo strumento che già
padroneggia.

### Problema 2: riconoscere prodotti difettosi dalle foto

Il magazzino fotografa ogni reso e vuole segnalare automaticamente i pezzi
danneggiati. Esiste già un pilota con qualche migliaio di foto etichettate
a mano. Nessuno in azienda ha mai progettato una rete convoluzionale.

Costruire quella rete da zero — le Lezioni 6-15 di questo corso insegnano
esattamente questo percorso, con NumPy prima e Keras poi — richiederebbe
capire architetture, augmentation, transfer learning: settimane di lavoro
per un'azienda il cui prodotto non è il machine learning. Agent Platform
AutoML assorbe quella complessità: il servizio cerca l'architettura e
regola gli iperparametri, il team fornisce solo le foto etichettate.
Questa è la sottosezione 1.1 di nuovo, ma la sua metà "AutoML" invece
della metà "BigQuery ML": stesso principio — minimo codice per il
problema dato — applicato a un tipo di dato diverso.

### Problema 3: riassumere i ticket di assistenza

Il supporto clienti riceve circa duemila richieste al giorno e vuole un
riassunto di una riga per ogni ticket, da mostrare all'operatore umano.
Riassumere testo in linguaggio naturale è una capacità che un modello
fondazionale già possiede: non serve raccogliere dati etichettati né
addestrare nulla. Qui la scelta a minimo codice è integrare un modello
esistente da Gemini Enterprise Agent Platform Model Garden tramite API —
la sottosezione 1.2 della guida.

Il punto su cui la guida insiste esplicitamente è il costo di quella
scelta, non solo la sua correttezza tecnica. Se Nordica chiama il modello
più potente disponibile per ognuno dei duemila ticket giornalieri, la
spesa annuale cresce in proporzione, e la latenza di un modello grande può
rallentare lo strumento che l'operatore usa in tempo reale. Un modello più
piccolo del Model Garden, scelto o messo a punto per questo compito
specifico, può raggiungere la stessa qualità di riassunto a una frazione
del costo e del tempo di risposta. Questa è la sottosezione 1.2 sotto
un'altra voce: "optimizing Gemini-based applications for cost, latency,
and availability".

### Il filo che lega i tre problemi

In ciascuno dei tre casi la domanda non era "quale modello è più
accurato", ma "quale strumento risolve questo problema con il minimo
sforzo di sviluppo, dati i vincoli reali": dove vivono i dati, che
competenze ha il team, quanto costa servire la soluzione in produzione.
La exam guide chiama questo il Dominio 1 perché è la prima decisione da
prendere, prima ancora di scrivere una riga di codice: BigQuery ML,
AutoML o un'API già pronta, in base al problema che si ha davanti — non
per abitudine o per preferenza personale.

### Una nota sulla terminologia

La exam guide usa sistematicamente "Gemini Enterprise Agent Platform"
(spesso abbreviato "Agent Platform" nei bullet) per la piattaforma gestita
che in edizioni precedenti della guida si chiamava "Vertex AI". Questa
lezione usa la terminologia della guida attuale. Il rapporto storico
preciso tra i due nomi non è affermato dalla guida stessa, quindi non
viene affermato qui.

## Prova tu

Nordica apre un nuovo canale B2B e vuole stimare, per ogni cliente
business, la probabilità che rinnovi il contratto annuale. I dati (storico
ordini, ticket di supporto, data dell'ultimo contatto commerciale) vivono
in tre tabelle BigQuery diverse, già collegate da una chiave cliente.
Nessuno in azienda ha esperienza di deep learning, e serve un primo
modello funzionante entro una settimana.

Prima di leggere le risposte del quiz sotto, prova a rispondere: quale
strumento useresti, e perché — con quali vincoli specifici di questo
scenario la tua scelta si allinea?

## Errori comuni

- Scegliere sempre la soluzione custom per abitudine: nel Problema 2 di
  Nordica, costruire una CNN da zero avrebbe richiesto settimane per un
  guadagno di accuratezza che l'azienda non aveva chiesto.
- Confondere "basso codice" con "nessuna competenza richiesta": scegliere
  tra BigQuery ML, AutoML e un modello fondazionale richiede comunque
  capire il tipo di problema e i vincoli di costo/latenza — è una
  decisione, non un default.
- Trattare la sintassi SQL esatta di BigQuery ML come materiale d'esame
  verificato: la guida valuta l'attività svolta ("generating predictions
  using BigQuery ML"), non i nomi di istruzione precisi (vedi riquadro in
  cima alla pagina).

## Quiz

1. Perché BigQuery ML, nel Problema 1 di Nordica, è più economico di un
   modello ARIMA allenato in un notebook — anche se il modello sottostante
   è lo stesso tipo di algoritmo?
2. Nel Problema 3, perché la scelta del modello fondazionale non si ferma
   a "questo modello sa riassumere bene i ticket"?
3. Nello scenario B2B di "Prova tu", quale strumento risponde meglio ai
   vincoli (dati già in BigQuery, nessuna competenza di deep learning,
   una settimana di tempo)?

<details>
<summary><b>Apri le risposte</b></summary>

1. Non per la matematica del modello (ARIMA resta ARIMA), ma perché
   evita tre costi nascosti: una pipeline di export dati da mantenere, un
   ambiente notebook da tenere aggiornato, e previsioni che invecchiano
   tra un export e l'altro. BigQuery ML addestra dove i dati già vivono.
2. Perché la sottosezione 1.2 valuta esplicitamente costo, latenza e
   disponibilità come vincoli di progettazione. Un modello che riassume
   bene ma costa troppo per duemila chiamate al giorno, o risponde troppo
   lentamente per lo strumento dell'operatore, non è la scelta giusta
   anche se tecnicamente funziona.
3. BigQuery ML: i dati sono già collegati in tre tabelle dello stesso
   warehouse (nessun export da costruire), il problema è di
   classificazione tabellare (probabilità di rinnovo), e un `CREATE
   MODEL` di tipo `LOGISTIC_REG` o `BOOSTED_TREE_CLASSIFIER` è alla
   portata di un team senza competenze di deep learning in molto meno di
   una settimana.

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
