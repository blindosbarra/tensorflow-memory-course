# Syllabus

Questa e' la mappa del corso. Non e' una lista di tecnologie da spuntare: e' il
percorso con cui costruirai, un pezzo alla volta, un piccolo sistema di memoria
AI.

L'idea e' semplice:

> prima impari a trattare dati piccoli e comprensibili, poi costruisci modelli,
> poi aggiungi retrieval, grafi, modelli linguistici e infine valutazione.

## Come studiare

Ogni lezione dovrebbe durare 15-30 minuti.

Per ogni lezione farai sempre almeno una cosa concreta:

- leggere un piccolo dataset;
- scrivere o capire poche righe di codice;
- eseguire un notebook;
- completare un esercizio;
- vedere un output.

Se una lezione sembra solo teoria o solo comandi, va migliorata.

## Fase 1: dati prima dei modelli

Prima di TensorFlow serve una base molto pratica: sapere cosa c'e' dentro una
tabella.

Vedrai:

1. **Missing values**
   - cosa sono i valori mancanti;
   - come leggerli con pandas;
   - quando scartare una riga;
   - quando riempire un valore.

2. **Duplicati, tipi e outlier**
   - righe ripetute;
   - numeri letti come testo;
   - valori troppo strani per essere ignorati.

3. **Train, validation e test**
   - perche' non si valuta un modello sui dati usati per costruirlo;
   - come dividere un dataset senza confondersi.

4. **Data leakage**
   - il modo piu' subdolo per ottenere risultati belli ma falsi;
   - esempi piccoli per riconoscerlo.

5. **Encoding e scaling**
   - come trasformare categorie e numeri in input adatti a un modello.

Risultato della fase: saprai preparare una tabella piccola senza barare e senza
perdere traccia delle decisioni.

## Fase 2: tensori, gradienti e Keras

Qui entri nel cuore del machine learning, ma senza saltare passaggi.

Vedrai:

1. **Array, vettori, matrici e tensori**
   - cosa cambia tra una lista, una matrice e un tensore;
   - perche' le forme dei dati contano.

2. **Loss function**
   - come misurare quanto un modello sta sbagliando.

3. **Gradienti**
   - l'idea dietro "aggiustare" un modello;
   - prima intuizione, poi codice.

4. **Dense layer e prima rete neurale**
   - cosa fa uno strato denso;
   - come Keras organizza input, output e training.

5. **Training ed evaluation**
   - cosa succede durante `fit`;
   - come leggere metriche semplici;
   - come evitare overfitting evidente.

Risultato della fase: avrai una piccola rete Keras che classifica record di
memoria sintetici.

## Fase 3: testo ed embedding

Una memoria e' soprattutto testo. A questo punto impari a trasformare frasi in
numeri confrontabili.

Vedrai:

1. **Tokenizzazione**
   - come il testo viene spezzato in unita' piu' piccole.

2. **Embedding**
   - come rappresentare parole o frasi come vettori.

3. **Similarita'**
   - come capire se due memorie sono vicine.

4. **Visualizzazione**
   - PCA o UMAP per vedere gruppi di memorie.

5. **Metriche retrieval**
   - Recall@K;
   - MRR;
   - perche' "sembra giusto" non basta.

Risultato della fase: potrai cercare memorie simili a una domanda o a un ricordo.

## Fase 4: rappresentare le memorie

Qui il progetto prende forma. Non stai piu' solo addestrando modelli: stai
decidendo come una memoria deve essere salvata.

Vedrai:

1. **Schema della memoria**
   - `memory_id`;
   - `text`;
   - `timestamp`;
   - `type`;
   - `entities`;
   - `importance`;
   - `relations`.

2. **Tipi di memoria**
   - episodic;
   - semantic;
   - preference.

3. **Importance scoring**
   - una baseline semplice per decidere cosa vale la pena conservare.

4. **Entita' e relazioni**
   - persone, luoghi, eventi e collegamenti.

5. **Grafo delle memorie**
   - non come decorazione;
   - come modo per fare domande utili.

Risultato della fase: avrai un piccolo Memory AI Lab locale con record
strutturati, ricerca e relazioni.

## Fase 5: Transformer, Gemma e output strutturato

Solo ora arrivano i modelli linguistici. Arrivano tardi apposta: prima devi
avere baseline e metriche.

Vedrai:

1. **Attention**
   - intuizione dell'attenzione;
   - perche' alcune parole contano piu' di altre.

2. **Transformer block**
   - i componenti principali, senza trasformarlo in un corso di algebra.

3. **KerasHub e Gemma**
   - come verificare quali preset sono disponibili;
   - come non inventare compatibilita'.

4. **Structured output**
   - estrarre JSON;
   - controllare se il JSON e' valido;
   - misurare errori e allucinazioni.

Risultato della fase: userai un modello open per aiutare a strutturare memorie,
ma con controlli e limiti chiari.

## Fase 6: LoRA e adattamento

Qui impari ad adattare un modello senza riaddestrarlo da zero.

Vedrai:

1. **Freezing**
   - cosa significa congelare pesi.

2. **LoRA**
   - intuizione;
   - cosa viene addestrato;
   - cosa resta fisso.

3. **Confronto baseline**
   - un adattamento serve solo se batte una baseline chiara.

4. **Packaging adapter**
   - come salvare e riusare l'adapter.

Risultato della fase: un piccolo esperimento LoRA documentato e confrontato.

## Fase 7: pipeline, deploy e monitoring

Questa fase porta ordine nel progetto.

Vedrai:

1. **Pipeline locale**
   - validare;
   - trasformare;
   - addestrare;
   - valutare;
   - salvare artifact.

2. **Vertex AI opzionale**
   - solo dopo una pipeline locale equivalente;
   - con costi, cleanup e credenziali documentati.

3. **Monitoring**
   - data quality;
   - drift;
   - errori di serving;
   - metriche proxy quando le label arrivano tardi.

Risultato della fase: saprai distinguere un notebook che funziona da un sistema
che puo' essere mantenuto.

## Fase 8: preference learning e progetto finale

La fase finale aggiunge feedback e rifinitura.

Vedrai:

1. **Feedback schema**
   - come rappresentare preferenze umane.

2. **Chosen / rejected**
   - coppie di esempi preferiti e non preferiti.

3. **Preference tuning**
   - intuizione;
   - rischi;
   - limiti.

4. **Capstone**
   - ingestion;
   - cleaning;
   - schema;
   - classification;
   - embeddings;
   - graph;
   - retrieval;
   - evaluation;
   - monitoring report.

Risultato finale: un Memory AI Lab locale, piccolo ma completo, che prende
memorie testuali e produce record strutturati, ricerca e report.

## Dove siamo ora

Stato attuale:

- prima lezione completata: **Missing values nei dati di memoria**;
- lezione in learner review: **Duplicati, tipi e outlier**;
- prossima lezione consigliata dopo review: **Train, validation e test**;
- regola: una lezione alla volta, con review umana prima di scalare.
