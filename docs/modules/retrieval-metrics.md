---
id: retrieval-metrics
title: Metriche di retrieval (Recall@K, MRR)
module: text-embeddings
status: learner_review
estimated_minutes: 30
prerequisites: [clustering-memories]
deliverables: [notebooks/lezione-21-retrieval-metrics.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
  - https://en.wikipedia.org/wiki/Mean_reciprocal_rank
---

# Metriche di retrieval (Recall@K, MRR)

> **La lezione si segue nel notebook**
> `notebooks/lezione-21-retrieval-metrics.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il ventunesimo (e ultimo
> della Fase 3) passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 20. Chiude la Fase 3.

## Cosa saprai fare

Definire e calcolare Precision@K, Recall@K e Mean Reciprocal Rank su un
ranking prodotto per similarita', e spiegare quando ciascuna metrica e'
quella giusta da guardare per un sistema di ricerca.

## Teoria essenziale

Il retrieval valuta un **ranking** ordinato, non una singola predizione;
serve una nozione dichiarata di "rilevante" (qui: stesso `type`, un proxy
misurabile ma esplicitamente imperfetto). **Precision@K**
(`rilevanti_in_top_K / K`) misura la pulizia dei primi K risultati.
**Recall@K** (`rilevanti_in_top_K / rilevanti_totali`) misura quanto del
materiale rilevante e' stato trovato — strutturalmente basso se gli
elementi rilevanti sono molti piu' di `K`, indipendentemente dalla
qualita' del ranking. **Mean Reciprocal Rank** e' la media di `1/rank`
della prima posizione rilevante per ogni query — misura quanto in fretta
si trova *almeno un* buon risultato. Le tre metriche vanno lette insieme,
non isolatamente: rispondono a domande diverse sullo stesso ranking.

## Nel progetto

Ogni memoria di validation come query, similarita' coseno
(incorporatore delle Lezioni 17-20) per il ranking, stesso `type` come
proxy di rilevanza — escludendo le query senza altri elementi rilevanti
nel pool (classi con una sola memoria). Nell'esecuzione di riferimento:
Precision@3 = 0.907 (alta), Recall@3 = 0.319 (bassa, per via della classe
`episodic` numerosa — aritmetica, non un difetto), MRR = 1.000 (il primo
risultato e' sempre rilevante). Chiude la Fase 3 del corso.

## Errori comuni

- Guardare una sola metrica di retrieval isolatamente, senza le altre due.
- Interpretare un Recall@K basso come "l'embedding non funziona" senza
  controllare quanti elementi rilevanti totali esistono rispetto a `K`.
- Includere query senza nessun altro elemento rilevante nel pool nel
  calcolo di Precision/Recall, producendo una divisione per zero o un
  numero senza senso.
- Trattare il proxy di rilevanza scelto (stesso `type`) come l'unica
  nozione corretta di rilevanza invece che come una scelta pratica
  dichiarata.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, `cosine_similarity` (gia' usata nella Lezione 18, riusata
  qui per il ranking):
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- Wikipedia, *Mean reciprocal rank*:
  https://en.wikipedia.org/wiki/Mean_reciprocal_rank
