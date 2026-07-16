---
id: embedding-layer
title: Embedding layer
module: text-embeddings
status: learner_review
estimated_minutes: 30
prerequisites: [tokenization-vocabulary]
deliverables: [notebooks/lezione-16-embedding.ipynb]
sources:
  - https://keras.io/api/layers/core_layers/embedding/
  - https://keras.io/api/layers/pooling_layers/global_average_pooling1d/
  - https://www.tensorflow.org/text/guide/word_embeddings
---

# Embedding layer

> **La lezione si segue nel notebook** `notebooks/lezione-16-embedding.ipynb`:
> teoria, dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> sedicesimo passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 15.

## Cosa saprai fare

Sostituire il bag of words con vettori densi imparati dal modello
(`keras.layers.Embedding`), aggregare una sequenza di vettori-parola in un
vettore-frase con `GlobalAveragePooling1D`, e leggere criticamente cosa un
embedding addestrato da zero riesce (e non riesce) a imparare con pochi
dati.

## Teoria essenziale

Il bag of words (Lezione 15) rappresenta ogni parola come una colonna
indipendente in un vettore sparso: nessuna nozione di somiglianza tra
parole, dimensione pari al vocabolario. Un **embedding** e' invece una
tabella di lookup appresa, forma `(input_dim, output_dim)`: `input_dim`
righe (una per id di token, cioe' la dimensione del vocabolario),
`output_dim` colonne (la dimensione del vettore denso). I valori sono pesi
del modello, aggiornati dalla backpropagation come un `Dense` qualunque.

`Embedding` prende in input una sequenza di id (da `TextVectorization`
`output_mode='int'`, lunghezza fissata con `output_sequence_length`) e
restituisce una sequenza di vettori: una frase di `L` token diventa una
matrice `L x output_dim`, non un singolo vettore. `GlobalAveragePooling1D`
aggrega quella sequenza facendo la media lungo l'asse dei token,
producendo il vettore fisso che un `Dense` a valle puo' consumare.

Con frasi brevi in sequenze lunghe, il padding puo' essere la maggioranza
dei token: senza `mask_zero=True` su `Embedding`, il pooling media anche i
vettori del padding, diluendo il segnale. `mask_zero=True` propaga una
maschera ai layer successivi, che ignorano quelle posizioni invece di
includerle nell'aggregazione.

Con dataset piccoli, un embedding addestrato da zero organizza lo spazio
in modo imperfetto: serve molto testo perche' le co-occorrenze si
stabilizzino. Il limite e' dei dati disponibili, non della teoria — e il
motivo per cui in pratica si usano spesso embedding pre-addestrati (fuori
scope in questo ambiente: nessuna credenziale Kaggle/HuggingFace).

## Nel progetto

Il classificatore di memorie passa da bag of words multi-hot a
`Embedding(input_dim=300, output_dim=16)` + `GlobalAveragePooling1D`,
stessa rete a valle (`Dense(32, relu)` + `Dropout(0.3)` +
`Dense(4, softmax)`) della Lezione 15. L'accuratezza su validation resta
sullo stesso ordine di grandezza (~95%): il punto non e' "piu' accurato",
e' che il vettore prodotto e' denso e potenzialmente porta somiglianza
semantica — una proprieta' che la ricerca per similarita' (Lezioni 17-18)
sfrutta e che il bag of words non ha.

## Errori comuni

- Dare in input a `Embedding` una sequenza di lunghezza variabile invece di
  una sequenza padded a lunghezza fissa (`output_sequence_length`).
- Aspettarsi che l'embedding del padding (id 0) sia automaticamente zero:
  e' un vettore appreso come gli altri.
- Aggregare una sequenza con molto padding senza `mask_zero=True`: il
  vettore-frase risultante e' dominato dal vettore di padding ripetuto
  molte volte, non dal contenuto reale della frase.
- Interpretare le vicinanze tra parole di un embedding addestrato da zero
  su un dataset piccolo come "il modello ha capito il significato": con
  pochi dati la struttura appresa e' spesso rumorosa.
- Confondere `input_dim` (dimensione del vocabolario) con `output_dim`
  (dimensione del vettore per parola).

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- Keras, `Embedding` layer:
  https://keras.io/api/layers/core_layers/embedding/
- Keras, `GlobalAveragePooling1D`:
  https://keras.io/api/layers/pooling_layers/global_average_pooling1d/
- TensorFlow, *Word embeddings*:
  https://www.tensorflow.org/text/guide/word_embeddings
