---
id: capstone-embedding-graph
title: Embedding, retrieval e grafo
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-classifier, cosine-similarity, graph-memory-networkx]
deliverables: [notebooks/lezione-55-capstone-embedding-grafo.ipynb]
sources:
  - https://arxiv.org/abs/1706.03762
---

# Embedding, retrieval e grafo

> **La lezione si segue nel notebook**
> `notebooks/lezione-55-capstone-embedding-grafo.ipynb`: teoria, codice eseguibile, esercizio e il 55esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Assemblare embedding, ricerca per similarita', estrazione entita' e grafo in NumPy e Python puro (senza dipendenze pesanti).

## Teoria essenziale

Riuso: embedding deterministico (Lezioni 30-31), similarita' coseno (Lezione 18), estrazione entita' a regole (Lezione 26). Il grafo e' una **lista di adiacenza** in Python puro (niente `networkx`), cosi' il capstone gira ovunque.

## Cosa mostra il notebook

Indice di embedding (30, 48); la ricerca restituisce le memorie piu' simili (coseno) e il grafo collega memorie ed entita' — le entita' piu' connesse (es. Elena con grado 5) sono i nodi centrali della conoscenza. Output reali.

## Collegamento al progetto

Il passo 55 fornisce `rappresenta(testo)` (embedding_dim + entities) per la pipeline.

## Fonti

- Vaswani et al., 2017, *Attention Is All You Need* — <https://arxiv.org/abs/1706.03762>
