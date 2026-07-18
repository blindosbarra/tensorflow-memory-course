---
id: tokenizer-generation
title: Tokenizer e generazione
module: transformers-gemma
status: learner_review
estimated_minutes: 30
prerequisites: [tokenization-vocabulary, transformer-block]
deliverables: [notebooks/lezione-33-tokenizer-generazione.ipynb]
sources:
  - https://arxiv.org/abs/1706.03762
  - https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.choice.html
---

# Tokenizer e generazione

> **La lezione si segue nel notebook**
> `notebooks/lezione-33-tokenizer-generazione.ipynb`: teoria, tokenizer e
> generazione eseguibili, esercizio e il trentatreesimo passo del progetto
> Memory AI Lab. Questa pagina e' il riassunto di riferimento. Prerequisiti:
> Lezioni 15 e 32.

## Cosa saprai fare

Costruire un **tokenizer** (encode/decode con round-trip) dal corpus delle
memorie e un **ciclo di generazione autoregressiva** con un modellino bigram in
NumPy, per padroneggiare greedy vs sampling con temperatura *prima* di usare un
modello vero (Gemma, Lezione 35).

## Teoria essenziale

Un modello generativo non vede lettere ma **id di token**: servono le mappe
`token -> id` (encode) e `id -> token` (decode), piu' i token speciali `<bos>`
(inizio) e `<eos>` (fine). La generazione e' **autoregressiva** (Vaswani et
al., 2017, Sez. 3.1): parti da `<bos>`, predici il token successivo, lo
aggiungi, ripeti finche' esce `<eos>` o raggiungi un limite.

Dalla distribuzione del prossimo token:

- **greedy**: prendi sempre il piu' probabile → deterministico, ripetitivo;
- **temperatura T**: campioni con $p_i \propto \exp(\log p_i / T)$. $T<1$
  appuntisce (prudente), $T>1$ appiattisce (creativo), $T\to0$ tende al greedy.

## Cosa mostra il notebook

Dal corpus si costruisce un vocabolario di **66 token** (piu' `<bos>`/`<eos>`)
e una matrice di transizione bigram `(66, 66)` con add-one smoothing (ogni riga
somma a 1). Il modello **non e' un Transformer** — e' un bigram — ma il *ciclo*
di generazione e' identico a quello di un modello grande: cambia solo *come* si
stima il prossimo token. Output realmente eseguiti:

```text
greedy        : the user prefers short updates about il progetto tensorflow
temp T=0.7    : the user dislikes il colloquio long notifications
temp T=1.3    : elena works for lives in dislikes every torino at
```

Il greedy e' sempre identico (percorso piu' probabile); la temperatura varia le
frasi, e T alta rischia di piu' (frasi meno coerenti). E' esattamente il
pomello che regolerai su Gemma nella Lezione 35.

## Collegamento al progetto

Il passo 33 aggiunge un tokenizer riusabile con round-trip garantito
(`decode(encode(x)) == x`, verificato da un `assert`) e la funzione di
generazione. Il tokenizer e' il componente che alimentera' il modello open
della Lezione 35.

## Riepilogo

1. Il modello vede id di token: servono encode/decode.
2. `<bos>`/`<eos>` segnano inizio e fine.
3. Generazione **autoregressiva**: predici, aggiungi, ripeti.
4. Il ciclo e' identico tra bigram e Transformer.
5. Greedy = sempre il piu' probabile; temperatura = campionamento controllato.
6. $T\to0$ tende al greedy.

## Fonti

- Vaswani et al., *Attention Is All You Need*, 2017 — <https://arxiv.org/abs/1706.03762>
- *numpy.random.Generator.choice* — <https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.choice.html>
