---
id: pmle-01-architect-low-code-ai-solutions
title: "Certificazione PMLE - Dominio 1: architettare soluzioni AI low-code"
module: gcp-ml-certification
status: writing
estimated_minutes: 45
prerequisites: []
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
  - https://cloud.google.com/bigquery/docs/bqml-introduction
---

# Certificazione PMLE — Dominio 1: architettare soluzioni AI low-code

!!! note "Cosa è verificato, cosa è spiegazione"
    I pesi dei domini, le sottosezioni 1.1/1.2 e la terminologia "Gemini
    Enterprise Agent Platform" sono verificati parola per parola contro
    la exam guide ufficiale, fornita dallo studente. La exam guide però
    elenca **attività** ("generating predictions using BigQuery ML"), non
    spiega **come** funzionano gli strumenti. I meccanismi spiegati sotto
    (sintassi `CREATE MODEL`, clausola `TRANSFORM`, normalizzazione delle
    feature con numeri d'esempio, metriche di `ML.EVALUATE` calcolate su
    una matrice di confusione costruita, ricerca architetturale di
    AutoML, framework prompting/tuning) sono conoscenza generale, non
    riverificata sulla documentazione live in questa sessione: marcati
    esplicitamente dove compaiono, con i numeri usati negli esempi
    dichiarati come didattici e non come dati reali. Dettaglio in
    `course/research_gaps.md`.

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

**Come funziona BigQuery ML, concretamente.** Un'unica istruzione SQL
addestra il modello sui risultati di una query:

```
CREATE MODEL nordica.previsione_domanda
OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='settimana',
        time_series_data_col='unita_vendute', time_series_id_col='sku')
AS SELECT settimana, sku, unita_vendute FROM nordica.storico_ordini;
```

`model_type` sceglie l'algoritmo: `ARIMA_PLUS` per serie storiche come
questa, ma anche `LINEAR_REG`/`LOGISTIC_REG` per regressione o
classificazione lineare, `BOOSTED_TREE_REGRESSOR`/`_CLASSIFIER` per
alberi con boosting del gradiente, `KMEANS` per clustering,
`DNN_CLASSIFIER`/`_REGRESSOR` per reti dense — Nordica userà alcune di
queste altre opzioni più avanti in questa stessa lezione.

!!! info "Cosa sono questi modelli, in pratica (non dare per scontato di conoscerli)"
    - **`LINEAR_REG`**: traccia una retta (o iperpiano) tra le feature e
      un numero da prevedere — es. "quanto venderemo", un valore
      continuo. È il modello di regressione più semplice: veloce da
      addestrare, facile da interpretare, ma cattura solo relazioni
      lineari tra le feature e il target.
    - **`LOGISTIC_REG`**: come sopra ma per prevedere una categoria (tipicamente
      sì/no, es. "questo cliente rinnoverà il contratto?"). Nonostante il
      nome "regressione" è un modello di **classificazione**: restituisce
      una probabilità tra 0 e 1.
    - **`BOOSTED_TREE_REGRESSOR`/`_CLASSIFIER`** (gradient-boosted trees,
      la stessa famiglia di algoritmi di XGBoost): costruisce molti
      alberi decisionali piccoli in sequenza, dove ogni nuovo albero
      corregge gli errori di quelli precedenti. Cattura relazioni non
      lineari tra le feature (a differenza di `LINEAR_REG`/`LOGISTIC_REG`)
      ed è spesso la scelta con le migliori prestazioni su dati tabellari
      strutturati, al costo di essere meno immediato da interpretare di
      una singola retta.
    - **`KMEANS`**: **clustering**, non predizione — non c'è un target da
      indovinare. Raggruppa le righe in un numero di gruppi (cluster)
      scelto in anticipo, mettendo insieme i punti che si somigliano di
      più secondo le feature date. Utile per segmentazione clienti o
      rilevare pattern quando non si ha già un'etichetta "corretta" da
      imparare.
    - **`DNN_CLASSIFIER`/`_REGRESSOR`** (rete neurale densa, le stesse
      reti feed-forward viste nelle Lezioni 5-7 del corso principale):
      utile quando le relazioni tra le feature sono complesse e non
      catturate bene da una retta o da alberi, ma richiede più dati e più
      tempo di addestramento dei modelli sopra per dare un vantaggio
      reale.
    - **`ARIMA_PLUS`** (usato da Nordica qui sopra): pensato
      specificamente per **serie storiche** — prevedere un valore futuro
      a partire dal suo stesso andamento passato nel tempo (stagionalità,
      trend), non da feature indipendenti come gli altri modelli di
      questa lista.

    In breve: prima si decide il **tipo di problema** (ho un'etichetta da
    prevedere? è un numero o una categoria? ho invece solo dati da
    raggruppare? il tempo è la variabile chiave?), e quella scelta
    determina quale famiglia di `model_type` è pertinente — non il
    contrario.

Una volta
addestrato, `ML.PREDICT(MODEL nordica.previsione_domanda, (SELECT ...))`
genera le previsioni, e `ML.EVALUATE(MODEL nordica.previsione_domanda)`
restituisce le metriche di errore sul modello — per un problema di
regressione/forecasting, tipicamente errore assoluto medio ed errore
quadratico medio; per un problema di classificazione (che Nordica
incontrerà più sotto, nella sezione "Prova tu, risolto") invece
precision, recall, accuracy, F1 e ROC AUC, gli stessi concetti che la
Lezione 13 del corso principale tratta con codice eseguito riga per riga.

!!! info "Perché (e quando) normalizzare le feature — con numeri veri"
    Immagina che invece del solo `ARIMA_PLUS`, Nordica costruisca anche il
    modello di rischio-rinnovo B2B (lo stesso della sezione "Prova tu" più
    sotto) con `LOGISTIC_REG`, usando tre feature: `spesa_mensile_eur`
    (range realistico 50–50.000), `mesi_da_attivazione` (range 1–120) e
    `ticket_aperti_90gg` (range 0–30). Sono su scale radicalmente diverse.

    **Perché è un problema per `LOGISTIC_REG` (e per `DNN_CLASSIFIER`).**
    Questi due `model_type` imparano per discesa del gradiente: a ogni
    passo, il peso di ciascuna feature viene aggiornato in proporzione al
    valore della feature stessa. Con `spesa_mensile_eur` che arriva fino a
    50.000 e `ticket_aperti_90gg` che arriva al massimo a 30, il gradiente
    calcolato sulla prima feature domina completamente quello calcolato
    sulla seconda: il modello impara quasi solo dalla spesa e converge
    lentamente (o male) sul peso da dare ai ticket, non perché i ticket
    contino davvero meno per prevedere il rinnovo, ma solo per un
    artefatto della scala numerica.

    **La correzione: standardizzazione (z-score).** Si trasforma ogni
    valore con `z = (x - media) / deviazione_standard`, calcolati sui dati
    di training. Con `spesa_mensile_eur` che ha media 5.000€ e deviazione
    standard 8.000€ sui clienti di Nordica: un cliente che spende
    50.000€/mese diventa `z = (50000 - 5000) / 8000 = 5,6`; un cliente che
    spende 50€/mese diventa `z = (50 - 5000) / 8000 = -0,62`. Applicando
    la stessa trasformazione a `mesi_da_attivazione`, tutte e due le
    feature finiscono nello stesso ordine di grandezza (tipicamente tra
    -3 e +3), e il gradiente non è più dominato da quale delle due ha i
    numeri più grandi in valore assoluto.

    **In BigQuery ML, con `TRANSFORM`:**

    ```sql
    CREATE MODEL nordica.rischio_rinnovo
    TRANSFORM(
      ML.STANDARD_SCALER(spesa_mensile_eur) OVER() AS spesa_norm,
      ML.STANDARD_SCALER(mesi_da_attivazione) OVER() AS mesi_norm,
      ticket_aperti_90gg,
      rinnova
    )
    OPTIONS(model_type='LOGISTIC_REG', input_label_cols=['rinnova'])
    AS SELECT spesa_mensile_eur, mesi_da_attivazione, ticket_aperti_90gg,
              rinnova
    FROM nordica.clienti_b2b;
    ```

    La media e la deviazione standard usate da `ML.STANDARD_SCALER`
    vengono calcolate una volta sui dati di training e **salvate dentro il
    modello**: ogni chiamata successiva a `ML.PREDICT` riapplica esattamente
    quegli stessi due numeri ai nuovi clienti, invece di ricalcolarli sul
    nuovo batch di dati (che avrebbe una media leggermente diversa) — è lo
    stesso motivo tecnico, applicato alla normalizzazione, per cui
    `TRANSFORM` evita il training-serving skew descritto più sotto.

    **Quando invece non serve.** `BOOSTED_TREE_CLASSIFIER` (e gli alberi in
    generale) non ne ha bisogno: un albero decide dove tagliare ogni
    feature guardando solo l'ordine dei valori ("spesa maggiore di 12.000€?
    sì/no"), non la loro grandezza assoluta, quindi il gradiente non è mai
    coinvolto e la scala delle feature non altera l'addestramento. È una
    ragione tecnica in più (oltre a quelle già viste sopra) per cui i due
    `model_type` non sono intercambiabili senza conseguenze.

    **Stato: needs_reverification** — meccanismo di ottimizzazione basato
    su gradiente e formula dello z-score sono conoscenza ML generale;
    `ML.STANDARD_SCALER` come nome di funzione BigQuery ML specifico non è
    riverificato su documentazione live in questa sessione. I numeri di
    Nordica (media, deviazione standard, range) sono un esempio didattico
    costruito per illustrare il meccanismo, non dati reali.

**Perché conviene rispetto al notebook.** Non per la matematica — un
`ARIMA_PLUS` in BigQuery ML e un ARIMA allenato con statsmodels
implementano la stessa famiglia di modelli statistici. Conviene perché
elimina tre costi nascosti: la pipeline di export dati, l'ambiente
notebook da tenere aggiornato, lo scarto temporale tra un export e
l'altro. I dati restano fermi, e i due analisti lavorano nello stesso SQL
che già conoscono.

### Problema 2: riconoscere prodotti difettosi dalle foto

Il magazzino fotografa ogni reso e vuole segnalare automaticamente i
pezzi danneggiati. Esiste già un pilota con qualche migliaio di foto
etichettate a mano. Nessuno in azienda ha mai progettato una rete
convoluzionale.

Costruire quella rete da zero — le Lezioni 6-15 di questo corso insegnano
esattamente questo percorso, con NumPy prima e Keras poi — richiederebbe
scegliere un'architettura, capire l'augmentation, decidere se e come fare
transfer learning: settimane di lavoro per un'azienda il cui prodotto non
è il machine learning.

**Come funziona AutoML, concretamente.** AutoML non prova "un" modello:
dentro un budget di calcolo/tempo che Nordica imposta, cerca molte
combinazioni candidate di architettura e iperparametri in parallelo — per
le immagini, spesso partendo da backbone già pre-addestrati invece che da
pesi casuali — e alla fine seleziona la combinazione con la performance
migliore su uno split di validazione tenuto da parte. È lo stesso
processo di ricerca per tentativi che un ingegnere ML farebbe a mano
(provare un'architettura, misurarla, aggiustare, riprovare), automatizzato
e parallelizzato su molti candidati contemporaneamente invece che uno
alla volta. Nordica fornisce solo le foto etichettate; AutoML restituisce
un modello pronto da valutare con le stesse metriche di classificazione
di prima (precision, recall, F1).

Questa è ancora la sottosezione 1.1 della exam guide, ma la sua metà
"AutoML" invece della metà "BigQuery ML": stesso principio — minimo
codice per il problema dato — applicato a un tipo di dato diverso e a un
meccanismo di training diverso (ricerca automatica invece di un algoritmo
fissato).

### Problema 3: riassumere i ticket di assistenza

Il supporto clienti riceve circa duemila richieste al giorno e vuole un
riassunto di una riga per ogni ticket, da mostrare all'operatore umano.
Riassumere testo in linguaggio naturale è una capacità che un modello
fondazionale già possiede: non serve raccogliere dati etichettati né
addestrare nulla da zero. Qui la scelta a minimo codice è integrare un
modello esistente da Gemini Enterprise Agent Platform Model Garden
tramite API — la sottosezione 1.2 della guida.

**Tre livelli di intervento, non uno solo.** Se il riassunto generico non
basta (per esempio Nordica vuole che il modello segua sempre lo stesso
formato interno con priorità/categoria/riassunto), la domanda successiva
è *quanto* intervenire sul modello, e qui c'è un ordine di costo
crescente da rispettare:

1. **Prompting** (istruzioni nel testo della richiesta, eventualmente con
   esempi) o **RAG** (recuperare contesto pertinente prima di generare):
   nessun peso del modello viene aggiornato, è il modo più veloce ed
   economico di iterare, e va provato per primo.
2. **Tuning efficiente in parametri** (es. LoRA): si allenano poche
   matrici di adattamento aggiuntive invece di tutti i pesi del modello,
   ottenendo un comportamento più specifico del solo prompting a una
   frazione del costo del fine-tuning completo.
3. **Fine-tuning completo**: si aggiornano tutti i pesi su un dataset
   etichettato specifico per il compito. È l'opzione più costosa, e la
   exam guide la nomina esplicitamente ("fine-tuning Gemini models using
   BigQuery" in 1.1): si sceglie quando i primi due livelli non bastano a
   ottenere il comportamento richiesto, non come prima opzione.

**Il vincolo che la guida rende esplicito.** Se Nordica chiama il modello
più potente disponibile per ognuno dei duemila ticket giornalieri, la
spesa annuale cresce in proporzione, e la latenza di un modello grande
può rallentare lo strumento che l'operatore usa in tempo reale. Un
modello più piccolo del Model Garden — scelto direttamente, o con
prompting/tuning invece di fine-tuning completo — può raggiungere la
stessa qualità percepita a una frazione del costo e del tempo di
risposta. Questa è la sottosezione 1.2 sotto la voce "optimizing
Gemini-based applications for cost, latency, and availability": il
vincolo di progettazione non è solo "il riassunto è buono?", è anche
"quanto costa produrlo duemila volte al giorno, e quanto tempo impiega?".

### Il filo che lega i tre problemi

In ciascuno dei tre casi la domanda guida era la stessa: quale strumento
risolve questo problema con il minimo sforzo di sviluppo, dati i vincoli
reali — dove vivono i dati, che competenze ha il team, quanto costa
servire la soluzione in produzione. La exam guide chiama questo il
Dominio 1 perché è la prima decisione da prendere, prima ancora di
scrivere una riga di codice: BigQuery ML, AutoML o un modello già pronto,
in base al problema che si ha davanti.

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
strumento useresti, quale `model_type` sceglieresti se fosse BigQuery ML,
e quali metriche guarderesti su `ML.EVALUATE` per giudicare se il modello
è abbastanza buono da usare?

## Prova tu, risolto: leggere `ML.EVALUATE` con numeri veri

La risposta rapida ("BigQuery ML, `LOGISTIC_REG` o
`BOOSTED_TREE_CLASSIFIER`, guarda precision/recall/F1/ROC AUC") è
corretta ma da sola non dice se il modello è **buono abbastanza da
usare**. Serve leggere i numeri veri. Nordica addestra il modello sui
dati storici e lo valuta su un trimestre tenuto da parte: 200 clienti
B2B, di cui 40 non hanno rinnovato (classe positiva = "non rinnova",
perché è il caso su cui il team vuole agire) e 160 hanno rinnovato.

`ML.CONFUSION_MATRIX(MODEL nordica.rischio_rinnovo)` restituisce una
tabella che incrociamo così (numeri costruiti per l'esempio, non dati
reali):

| | Predetto: non rinnova | Predetto: rinnova |
|---|---|---|
| **Reale: non rinnova** (40) | 28 (TP) | 12 (FN) |
| **Reale: rinnova** (160) | 18 (FP) | 142 (TN) |

Da questa tabella, `ML.EVALUATE` calcola:

- **Precision** = TP / (TP + FP) = 28 / (28 + 18) = 28/46 ≈ **0,61**. Su
  100 clienti che il modello segnala come "a rischio", circa 61
  rinunciano davvero; gli altri 39 avrebbero rinnovato comunque — sono
  falsi allarmi.
- **Recall** = TP / (TP + FN) = 28 / (28 + 12) = 28/40 = **0,70**. Il
  modello intercetta il 70% dei clienti che davvero non rinnoveranno; il
  restante 30% (12 clienti su 40) sfugge senza che nessuno se ne accorga
  in tempo.
- **F1** = 2 × (precision × recall) / (precision + recall) = 2 × (0,61 ×
  0,70) / (0,61 + 0,70) ≈ **0,65**. Una singola cifra che pesa precision
  e recall insieme — utile per confrontare due modelli, ma da sola non
  dice quale dei due errori (falsi allarmi o clienti persi) pesa di più
  per Nordica.
- **Accuracy** = (TP + TN) / totale = (28 + 142) / 200 = **0,85**. Qui è
  un numero fuorviante da solo: un modello che dicesse sempre "rinnova"
  otterrebbe comunque l'80% di accuracy (160 clienti su 200 rinnovano
  davvero), senza intercettare un solo cliente a rischio. L'accuracy alta
  nasconde un problema quando le classi sono sbilanciate, come qui (20%
  di abbandono contro 80% di rinnovo) — è il motivo per cui `ML.EVALUATE`
  restituisce anche precision/recall/F1 e non solo accuracy.

**Quale numero conta di più, per Nordica.** Un falso negativo (un
cliente che sta per abbandonare e il modello non lo segnala) costa a
Nordica l'intero valore del contratto annuale perso, senza nessun
tentativo di trattenerlo. Un falso positivo (un cliente segnalato "a
rischio" che in realtà avrebbe rinnovato comunque) costa solo lo sconto
di un'offerta di fidelizzazione inviata inutilmente. Con questa
asimmetria di costo, Nordica preferisce un modello con **recall più
alto anche a scapito della precision**: `ML.PREDICT` restituisce una
probabilità continua, non solo un'etichetta sì/no, quindi il team può
abbassare la soglia di decisione (es. da 0,5 a 0,3: "segnala come
a rischio chiunque abbia probabilità di abbandono sopra il 30%, non solo
sopra il 50%") per intercettare più clienti a rischio, accettando più
falsi allarmi in cambio.

**ROC AUC**, l'ultima metrica citata dalla guida per la classificazione,
misura la qualità del modello **indipendentemente dalla soglia
scelta**: è la probabilità che, presi a caso un cliente che non
rinnoverà e uno che rinnoverà, il modello assegni al primo una
probabilità di abbandono più alta. Un ROC AUC di 0,5 equivale a
indovinare a caso; 1,0 è una separazione perfetta tra le due classi. È
la metrica giusta per confrontare due modelli **prima** di decidere dove
mettere la soglia di decisione, mentre precision/recall/F1 dipendono
dalla soglia scelta.

**Stato: needs_reverification** — le formule di precision/recall/F1/
accuracy/ROC AUC sono definizioni matematiche standard (conoscenza ML
generale, le stesse della Lezione 13 del corso principale); la tabella
di confusione e tutti i numeri di Nordica sono un esempio didattico
costruito per questa lezione, non un output reale di `ML.EVALUATE`.

## Errori comuni

- Scegliere sempre la soluzione custom per abitudine: nel Problema 2 di
  Nordica, costruire una CNN da zero avrebbe richiesto settimane per un
  guadagno di accuratezza che l'azienda non aveva chiesto.
- Confondere "basso codice" con "nessuna competenza richiesta": scegliere
  tra BigQuery ML, AutoML e un modello fondazionale richiede comunque
  capire il tipo di problema e i vincoli di costo/latenza — è una
  decisione, non un default.
- Dimenticare la clausola `TRANSFORM` in BigQuery ML e riscrivere a mano
  la stessa logica di preprocessing sia prima del training sia prima di
  ogni `ML.PREDICT`: causa lo stesso training-serving skew che il Dominio
  4/5 tratta più avanti nel corso.
- Scegliere il fine-tuning completo come prima opzione per un modello
  fondazionale, saltando prompting/RAG e il tuning efficiente in
  parametri: è l'opzione più costosa delle tre, non la prima da provare.
- Trattare la sintassi SQL esatta e i dettagli di AutoML come materiale
  d'esame verificato al 100%: sono spiegazioni di meccanismo aggiunte per
  chiarezza, marcate `needs_reverification` (vedi riquadro in cima alla
  pagina) perché non riverificate sulla documentazione live in questa
  sessione.

## Quiz

1. Nel Problema 1 di Nordica, `ML.EVALUATE` su un modello `ARIMA_PLUS`
   restituisce metriche di errore diverse da quelle che restituirebbe su
   un modello `LOGISTIC_REG`. Perché, e cosa cambia?
2. Cosa fa concretamente AutoML durante il training che un `CREATE MODEL`
   con un `model_type` fissato non fa?
3. Nel Problema 3, perché il fine-tuning completo di un modello
   fondazionale è l'ultima opzione da considerare, non la prima?
4. Nello scenario B2B di "Prova tu", quale strumento risponde meglio ai
   vincoli, e quali metriche di `ML.EVALUATE` giudicherebbero il modello?

<details>
<summary><b>Apri le risposte</b></summary>

1. Perché sono due problemi diversi: `ARIMA_PLUS` fa forecasting su una
   serie storica (l'errore si misura come distanza numerica tra
   previsione e valore reale, es. errore assoluto medio), mentre
   `LOGISTIC_REG` fa classificazione (l'errore si misura come quante
   predizioni erano nella classe giusta, es. precision/recall/F1).
   `ML.EVALUATE` adatta le metriche restituite al tipo di modello.
2. Cerca automaticamente, dentro un budget di calcolo/tempo, molte
   combinazioni di architettura e iperparametri in parallelo (spesso
   partendo da backbone pre-addestrati per immagini/testo) e sceglie la
   migliore su uno split di validazione. Un `model_type` fissato in
   BigQuery ML, invece, usa un algoritmo scelto in anticipo, senza questa
   ricerca.
3. Perché è l'opzione più costosa delle tre: aggiorna tutti i pesi del
   modello su un dataset etichettato specifico, mentre prompting/RAG
   (nessun peso aggiornato) e il tuning efficiente in parametri come LoRA
   (poche matrici aggiuntive) spesso bastano a ottenere il comportamento
   desiderato a un costo molto minore. Si sale di livello solo quando il
   livello precedente non basta.
4. BigQuery ML: i dati sono già collegati in tre tabelle dello stesso
   warehouse, il problema è di classificazione tabellare (probabilità di
   rinnovo), quindi un `model_type` come `LOGISTIC_REG` o
   `BOOSTED_TREE_CLASSIFIER` è alla portata di un team senza competenze
   di deep learning in molto meno di una settimana. Le metriche da
   guardare su `ML.EVALUATE` sono quelle di classificazione: precision,
   recall, F1 e ROC AUC — non errore quadratico medio, che è per la
   regressione.

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
  dettagli di sintassi/meccanismo, vedi riquadro in cima alla pagina):
  https://cloud.google.com/bigquery/docs/bqml-introduction
