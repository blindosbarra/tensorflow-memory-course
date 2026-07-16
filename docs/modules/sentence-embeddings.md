---
id: sentence-embeddings
title: Sentence embeddings e similarita'
module: text-embeddings
status: learner_review
estimated_minutes: 30
prerequisites: [embedding-layer]
deliverables: [notebooks/lezione-17-sentence-embeddings.ipynb]
sources:
  - https://keras.io/api/layers/pooling_layers/global_max_pooling1d/
  - https://keras.io/guides/functional_api/
  - https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder
---

# Sentence embeddings e similarita'

> **La lezione si segue nel notebook**
> `notebooks/lezione-17-sentence-embeddings.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il diciassettesimo passo
> del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento. Prerequisito: Lezione 16.

## Cosa saprai fare

Distinguere un vettore-parola da un vettore-frase (sentence embedding),
confrontare mean pooling e max pooling, e costruire un incorporatore che
condivide i pesi di un classificatore ma restituisce il vettore-frase
invece della predizione.

## Teoria essenziale

Un sentence embedding e' un vettore di lunghezza fissa che rappresenta un
intero testo. La Lezione 16 ne aveva gia' costruito uno come passo
interno (`GlobalAveragePooling1D` prima del `Dense` finale); qui lo si
tratta come prodotto finale, riusabile per compiti diversi dalla
classificazione (similarita', clustering, retrieval — Lezioni 18-21).

Due strategie di pooling: **mean** (media dei vettori-parola, robusta ma
diluisce il segnale) e **max** (`GlobalMaxPooling1D`, prende il valore
massimo per dimensione, piu' sensibile al rumore). Nessuna delle due e'
oggettivamente migliore; l'**attention** (Transformer, Fase 5) e' la loro
evoluzione, pesando i token invece di mediarli o prenderne il massimo. In
produzione si usano spesso encoder di frase **pre-addestrati** (Universal
Sentence Encoder, Sentence-BERT) su corpora enormi — non usati in questo
ambiente per mancanza di credenziali Kaggle/HuggingFace e GPU; qui si
costruisce un sentence embedding "from scratch", piu' debole ma
completamente trasparente.

## Nel progetto

Un `keras.Model` (API funzionale) condivide i pesi di `Embedding`
(`mask_zero=True`, come nella Lezione 16 — senza, il pooling mediarebbe
anche il padding) con il classificatore della Lezione 16 ma si ferma al
layer di pooling, diventando un **incorporatore**:
`incorpora(testi) -> vettori`, con la stessa dimensione dell'embedding,
deterministico (stesso testo, stesso vettore). E' l'artefatto che le
prossime lezioni (similarita' coseno, clustering, metriche di retrieval)
riusano.

## Errori comuni

- Aspettarsi che mean e max pooling producano lo stesso vettore sulla
  stessa frase.
- Allenare l'incorporatore separatamente dal classificatore invece di
  farlo condividere gli stessi pesi appresi: senza un compito da
  imparare, `Embedding` resta inizializzato a caso.
- Confondere il vettore-frase (sentence embedding) con la matrice di
  vettori-parola da cui e' derivato: sono oggetti di forma diversa
  (`(dimensione,)` contro `(token, dimensione)`).
- Trattare un embedding "from scratch" su un dataset piccolo come
  equivalente a un encoder pre-addestrato su miliardi di frasi.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- Keras, `GlobalMaxPooling1D`:
  https://keras.io/api/layers/pooling_layers/global_max_pooling1d/
- Keras, *The Functional API*:
  https://keras.io/guides/functional_api/
- TensorFlow Hub, *Universal Sentence Encoder* (citato per contesto, non
  usato in questo notebook):
  https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder
