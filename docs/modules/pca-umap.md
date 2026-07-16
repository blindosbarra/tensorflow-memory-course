---
id: pca-umap
title: Visualizzazione (PCA/UMAP) e clustering
module: text-embeddings
status: learner_review
estimated_minutes: 30
prerequisites: [cosine-similarity]
deliverables: [notebooks/lezione-19-pca-umap.ipynb]
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
  - https://scikit-learn.org/stable/modules/decomposition.html#pca
  - https://umap-learn.readthedocs.io/en/latest/how_umap_works.html
---

# Visualizzazione (PCA/UMAP) e clustering

> **La lezione si segue nel notebook** `notebooks/lezione-19-pca-umap.ipynb`:
> teoria, dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> diciannovesimo passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 18.

## Cosa saprai fare

Ridurre embedding ad alta dimensionalita' a 2D con la PCA, leggere la
varianza spiegata per capire quanto fidarti di un grafico, e spiegare a
parole in cosa UMAP differisce dalla PCA e quando si preferisce in
pratica.

## Teoria essenziale

La **PCA** e' lineare e deterministica: proietta i dati lungo le direzioni
di massima varianza globale, e `explained_variance_ratio_` dichiara
onestamente quanta informazione resta nella proiezione — un numero da
leggere sempre insieme al grafico. **UMAP** e' non lineare, preserva le
relazioni di vicinato **locale** invece della varianza globale, e produce
tipicamente grappoli piu' netti — ma non garantisce che le distanze tra
grappoli nel grafico riflettano le distanze reali nello spazio originale,
ed e' stocastica (senza seed, layout leggermente diversi a ogni run).

!!! warning "UMAP resta teoria in questo modulo"
    `umap-learn` non si installa in questo ambiente (conflitto di versione
    con Python 3.11: una dipendenza a monte richiede Python `<3.10`). Il
    codice hands-on della lezione usa solo `PCA` (gia' disponibile via
    scikit-learn); UMAP e' spiegato concettualmente, senza codice eseguito
    ne' output inventato, rispettando il principio "niente descritto come
    eseguibile che non lo sia davvero".

## Nel progetto

Gli embedding delle memorie di validation (Lezioni 17-18) proiettati a 2D
con `PCA(n_components=2)`, colorati per `type`: nell'esecuzione di
riferimento le prime 2 componenti catturano circa il 98% della varianza,
quindi il grafico e' un riassunto fedele — un caso favorevole per un
dataset piccolo a 4 classi, non una garanzia generale.

## Errori comuni

- Guardare un grafico PCA senza controllare `explained_variance_ratio_`:
  con varianza spiegata bassa, la vicinanza visiva puo' essere fuorviante.
- Interpretare la distanza tra due grappoli in un grafico UMAP come
  distanza "reale" nello spazio originale.
- Confrontare risultati UMAP tra esecuzioni diverse senza fissare un seed,
  aspettandosi lo stesso layout.
- Descrivere codice UMAP come eseguito quando l'ambiente non lo permette:
  meglio dichiarare esplicitamente il limite (come fa questa lezione) che
  inventare un output mai prodotto.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- scikit-learn, `PCA`:
  https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- scikit-learn, *Decomposing signals in components (PCA)*:
  https://scikit-learn.org/stable/modules/decomposition.html#pca
- UMAP, documentazione ufficiale (citata per contesto teorico, pacchetto
  non installato in questo ambiente):
  https://umap-learn.readthedocs.io/en/latest/how_umap_works.html
