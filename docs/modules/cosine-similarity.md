---
id: cosine-similarity
title: Similarita' coseno
module: text-embeddings
status: learner_review
estimated_minutes: 25
prerequisites: [sentence-embeddings]
deliverables: [notebooks/lezione-18-cosine-similarity.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
  - https://scikit-learn.org/stable/modules/metrics.html
---

# Similarita' coseno

> **La lezione si segue nel notebook**
> `notebooks/lezione-18-cosine-similarity.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il diciottesimo passo del
> progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.
> Prerequisito: Lezione 17.

## Cosa saprai fare

Calcolare la similarita' coseno a mano e con `sklearn`, spiegare perche'
e' invariante alla scala a differenza della distanza euclidea, e usarla
per trovare le memorie piu' simili a una memoria data dentro un insieme.

## Teoria essenziale

La similarita' coseno confronta due vettori guardando solo la loro
**direzione**: `cos(a, b) = (a . b) / (||a|| * ||b||)`. Il denominatore
normalizza per le norme, cancellando l'effetto della lunghezza — a
differenza della distanza euclidea, che penalizza anche vettori che
puntano nella stessa direzione ma con norme diverse. Range `[-1, 1]`: `1`
stessa direzione, `0` ortogonali, `-1` direzioni opposte. Per embedding di
testo appresi, i valori tipici stanno quasi sempre tra `0` e `1`.
`sklearn.metrics.pairwise.cosine_similarity` calcola una matrice intera di
similarita' tra due insiemi di vettori in un colpo solo.

## Nel progetto

L'incorporatore (Lezione 17) produce i vettori delle memorie di
validation; `cosine_similarity` trova le piu' simili a una memoria data.
Verifica di sanita': la similarita' media tra memorie dello stesso `type`
e' nettamente piu' alta di quella tra memorie di type diversi (0.975
contro 0.058 nell'esecuzione di riferimento) — coerente con il fatto che
l'`Embedding` e' stato addestrato per classificare il type, letto pero'
come segnale statistico su un compito specifico, non come prova di
comprensione semantica generale.

## Errori comuni

- Confondere similarita' coseno e distanza euclidea: la prima e'
  invariante alla scala, la seconda no.
- Interpretare una similarita' media piu' alta come garanzia valida per
  ogni singola coppia, invece che come tendenza statistica.
- Dimenticare di escludere una memoria da se' stessa (similarita' `1.0`
  con se stessa) quando si cerca la "memoria piu' simile".
- Trattare un gap di similarita' intra/inter-type ottenuto su un compito
  di classificazione come prova generale di qualita' semantica
  dell'embedding.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, `cosine_similarity`:
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
- scikit-learn, *Pairwise metrics, Affinities and Kernels*:
  https://scikit-learn.org/stable/modules/metrics.html
