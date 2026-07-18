---
id: attention-intuition
title: L'attenzione come recupero morbido
module: transformers-gemma
status: learner_review
estimated_minutes: 25
prerequisites: [cosine-similarity, hybrid-retrieval]
deliverables: [notebooks/lezione-30-attention-intuition.ipynb]
sources:
  - https://arxiv.org/abs/1706.03762
  - https://numpy.org/doc/stable/reference/generated/numpy.exp.html
---

# L'attenzione come recupero morbido

> **La lezione si segue nel notebook**
> `notebooks/lezione-30-attention-intuition.ipynb`: teoria, implementazione
> eseguibile da zero in NumPy, esercizio con soluzione spiegata e il
> trentesimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto
> di riferimento. Prerequisiti: Lezioni 18 e 28. Apre la Fase 5 (Transformer
> e modello open).

## Cosa saprai fare

Implementare la **scaled dot-product attention** con sole operazioni NumPy e
usarla come forma *morbida* e differenziabile di recupero sulle memorie del
progetto: invece di scegliere le prime *k* memorie (Lezione 28), assegni a
ognuna un peso e restituisci la loro media pesata.

## Teoria essenziale

Nella Lezione 28 il retrieval era una scelta **netta** (top-*k* per
punteggio). L'attenzione fa lo stesso in modo **morbido**: ogni memoria
riceve un peso tra 0 e 1, i pesi sommano a 1, e l'output e' la media pesata
dei contenuti. Tre ruoli presi dall'information retrieval — **query** (cosa
cerco), **chiavi** (l'indice), **valori** (il contenuto) — legano questa
lezione direttamente al vocabolario delle Lezioni 18 e 28.

La formula (Vaswani et al., 2017, Sez. 3.2.1) e':

$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Il prodotto $QK^\top$ misura la somiglianza query–chiave (parente non
normalizzato del coseno della Lezione 18). La divisione per $\sqrt{d_k}$
evita che, con dimensioni grandi, i prodotti scalari crescano tanto da
spingere la softmax in una zona a gradiente quasi nullo. La softmax
trasforma i punteggi in pesi che sommano a 1.

## Cosa mostra il notebook

Con un embedding deterministico e riproducibile (hashing delle parole in un
vettore a 32 dimensioni — nessun modello esterno, cosi' il notebook gira
nell'ambiente `numpy`/`pandas` di base) e una banca di 6 memorie, la query
`"The user prefers morning sessions for the project."` produce questi pesi
di attenzione (output realmente eseguito):

| peso | memoria |
|------|---------|
| 0.180 | The user prefers morning sessions for il progetto TensorFlow. |
| 0.167 | The user likes walking meetings. |
| 0.162 | Elena visited Glasgow for the weekend. |

La memoria che condivide piu' parole con la query riceve il peso maggiore,
mentre le memorie di viaggio restano sullo sfondo. Con una query *episodica*
(`"Marco visited Glasgow..."`) la distribuzione diventa piu' piatta
(max 0.169): nessuna memoria della banca parla davvero di viaggi, quindi
l'attenzione non trova un forte aggancio — un comportamento onesto della
similarita' non normalizzata su embedding poveri, non un difetto da nascondere.

## Collegamento al progetto

Il passo 30 aggiunge `recupero_per_attenzione(query, banca)`: restituisce il
**vettore di contesto** (media pesata dei valori, norma ~0.73 sul campione) e
le memorie ordinate per peso. Un `assert` verifica che il contesto abbia la
dimensione attesa e che i pesi tornino ordinati — cosi' una lezione futura
che riusa questa funzione se ne accorge subito se qualcosa regredisce. E' la
stessa operazione che, ripetuta e addestrata, diventa il cuore del
Transformer (Lezione 32).

## Riepilogo

1. L'attenzione e' un recupero *morbido*: pesi in [0,1] che sommano a 1.
2. Query = cosa cerco, chiavi = indice, valori = contenuto.
3. Formula: $\text{softmax}(QK^\top/\sqrt{d_k})\,V$.
4. $QK^\top$ e' una similarita' non normalizzata (parente del coseno).
5. $\sqrt{d_k}$ tiene la softmax fuori dalla zona a gradiente nullo.
6. L'output e' la media pesata dei valori: un vettore di contesto.
7. E' il mattone elementare del Transformer.

## Fonti

- Vaswani et al., *Attention Is All You Need*, 2017 — <https://arxiv.org/abs/1706.03762>
- *numpy.exp* — <https://numpy.org/doc/stable/reference/generated/numpy.exp.html>
