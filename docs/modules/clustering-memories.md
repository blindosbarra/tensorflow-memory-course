---
id: clustering-memories
title: Clustering delle memorie
module: text-embeddings
status: learner_review
estimated_minutes: 25
prerequisites: [pca-umap]
deliverables: [notebooks/lezione-20-clustering.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
  - https://scikit-learn.org/stable/modules/clustering.html#k-means
  - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html
---

# Clustering delle memorie

> **La lezione si segue nel notebook** `notebooks/lezione-20-clustering.ipynb`:
> teoria, dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> ventesimo passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 19.

## Cosa saprai fare

Applicare `KMeans` per raggruppare embedding senza etichette, spiegare
perche' le etichette di cluster sono arbitrarie, e valutare un clustering
onestamente con una tabella di contingenza e l'Adjusted Rand Index.

## Teoria essenziale

**K-Means** alterna due passi fino a convergenza: assegna ogni punto al
centroide piu' vicino, poi sposta ogni centroide alla media dei punti
assegnati — minimizzando l'**inerzia** (somma delle distanze al quadrato).
`k` va scelto prima (non viene imparato). Le etichette di cluster
(`0, 1, 2...`) sono **numeri arbitrari**, senza corrispondenza garantita
con etichette vere: confrontarle direttamente non ha senso. Una tabella
di contingenza (`pd.crosstab`) o l'**Adjusted Rand Index**
(`sklearn.metrics.adjusted_rand_score`, invariante alla permutazione delle
etichette: `1.0` accordo perfetto, `0.0` livello del caso) sono i modi
onesti di valutare.

## Nel progetto

`KMeans(n_clusters=4)` sui 16 numeri dell'embedding delle memorie di
validation (non sulla proiezione PCA, solo per il grafico). Con un
validation set sbilanciato (13 `episodic`, 5 `semantic`, 1 `unknown`, 1
`preference` nell'esecuzione di riferimento), K-Means tende a produrre
cluster di dimensioni simili tra loro: il cluster piu' numeroso viene
spezzato in due, le classi rare finiscono mescolate — Adjusted Rand Index
di 0.555 nell'esecuzione di riferimento, ne' perfetto ne' casuale, coerente
con questo limite noto, non un bug.

## Errori comuni

- Confrontare direttamente `cluster_assegnati == etichette_vere`: le
  etichette di cluster non hanno un ordine o un nome intrinseco.
- Aspettarsi un cluster "pulito" per ogni categoria quando le classi sono
  sbilanciate: K-Means minimizza l'inerzia, non rispetta i conteggi reali.
- Fare clustering sulla proiezione PCA a 2D invece che sui dati originali
  (la PCA e' per visualizzare, non per ridurre i dati prima del
  clustering, a meno di una scelta esplicita e motivata).
- Scegliere `k` senza nessuna euristica (metodo del gomito, conoscenza del
  dominio) quando le etichette vere non sono note in anticipo.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, `KMeans`:
  https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
- scikit-learn, *Clustering*:
  https://scikit-learn.org/stable/modules/clustering.html#k-means
- scikit-learn, `adjusted_rand_score`:
  https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html
