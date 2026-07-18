---
id: hybrid-retrieval
title: Retrieval ibrido
module: memory-representation
status: learner_review
estimated_minutes: 30
prerequisites: [graph-memory-networkx]
deliverables: [notebooks/lezione-28-retrieval-ibrido.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
  - https://networkx.org/documentation/stable/reference/classes/graph.html
---

# Retrieval ibrido

> **La lezione si segue nel notebook**
> `notebooks/lezione-28-retrieval-ibrido.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il ventottesimo passo del
> progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.
> Prerequisito: Lezione 27. Sintesi didattica: nessuna nuova API esterna,
> combina Lezioni 18, 21, 25 e 27 — vedi nota sulla fonte piu' sotto.

## Cosa saprai fare

Costruire un punteggio di retrieval ibrido (similarita' per embedding +
segnale di grafo + importanza composita, pesi dichiarati), misurarlo con
le metriche della Lezione 21, e leggere onestamente un risultato misto
invece di uno a senso unico.

## Teoria essenziale

`ibrido = w1*similarita + w2*segnale_grafo + w3*importanza_candidato`
(qui `0.5/0.3/0.2`, pesi dichiarati come nella Lezione 25). Non c'e'
garanzia che l'ibrido migliori **tutte** le metriche rispetto al solo
embedding: il proxy di rilevanza "stesso type" (Lezione 21) e'
dichiaratamente imperfetto, e il segnale di grafo ottimizza per una
nozione di rilevanza diversa (stessa entita' esplicita) che quella
metrica non premia sempre.

## Nel progetto

Confronto su validation: Precision@3 0.907→0.963 e Recall@3 0.319→0.361
migliorano con l'ibrido, ma MRR peggiora leggermente (1.000→0.972)
nell'esecuzione di riferimento. Caso concreto: per la query "Lucia works
on la riunione settimanale." l'ibrido promuove in cima "Lucia works on il
colloquio." (type diverso, ma stessa persona) al posto di un risultato
dello stesso type — "sbagliato" secondo il proxy, ragionevole nella
pratica.

## Errori comuni

- Aspettarsi che un segnale aggiuntivo migliori sempre ogni metrica
  contemporaneamente.
- Interpretare un peggioramento di una metrica come un bug, senza
  guardare dentro ai casi concreti per capire il perche'.
- Trattare il proxy "stesso type" come l'unica definizione valida di
  rilevanza, invece che come un'approssimazione dichiarata (Lezione 21).
- Aumentare il peso di un segnale senza rifare la valutazione per vedere
  l'effetto reale sui risultati.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

Lezione di sintesi: combina segnali e metriche gia' documentati e citati
nelle Lezioni 18 (similarita' coseno), 21 (metriche di retrieval), 25
(importanza composita) e 27 (grafo). Nessuna nuova API esterna introdotta,
oltre a quelle gia' usate in quelle lezioni e rilistate qui per comodita':

- scikit-learn, `cosine_similarity`:
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- NetworkX, `Graph`:
  https://networkx.org/documentation/stable/reference/classes/graph.html
