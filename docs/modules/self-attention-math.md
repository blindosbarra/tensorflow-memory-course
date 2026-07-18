---
id: self-attention-math
title: Self-attention, la matematica
module: transformers-gemma
status: learner_review
estimated_minutes: 30
prerequisites: [attention-intuition]
deliverables: [notebooks/lezione-31-self-attention.ipynb]
sources:
  - https://arxiv.org/abs/1706.03762
---

# Self-attention, la matematica

> **La lezione si segue nel notebook**
> `notebooks/lezione-31-self-attention.ipynb`: teoria, implementazione
> eseguibile in NumPy, esercizio con soluzione e il trentunesimo passo del
> progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.
> Prerequisito: Lezione 30.

## Cosa saprai fare

Costruire la **self-attention** da zero in NumPy e leggere la matrice di
attenzione quadrata token-per-token: capire *da dove* vengono query, chiavi e
valori e perche' l'output e' una rappresentazione *contestualizzata* di ogni
token.

## Teoria essenziale

Nella Lezione 30 la query arrivava da fuori. Nella **self-attention** query,
chiavi e valori nascono tutti dalla *stessa* sequenza $X$, tramite tre matrici
imparate:

$$Q = XW_Q,\quad K = XW_K,\quad V = XW_V$$

e poi si applica la formula gia' nota:
$\text{softmax}(QK^\top/\sqrt{d_k})\,V$ (Vaswani et al., 2017, Sez. 3.2).

Conseguenze:

- La matrice di attenzione e' **quadrata** ($n\times n$, con $n$ = numero di
  token). L'elemento $A_{ij}$ dice quanto il token $i$ guarda il token $j$.
- Ogni token diventa una **media pesata di tutti i token, incluso se stesso**
  — da qui *self*.
- L'output ha una riga per token: rappresentazioni **contestualizzate** (ogni
  vettore ora "sa" degli altri token della frase).

## Cosa mostra il notebook

Data la frase-memoria `"Marco visited Glasgow with his son"` (6 token), la
sequenza $X$ ha forma `(6, 16)`, la matrice di attenzione ha forma `(6, 6)` e
ogni riga somma a 1 (verificato con `np.allclose`). Con matrici di proiezione
**casuali** (non imparate — servono solo a illustrare la meccanica) la matrice
risulta volutamente vicina all'uniforme (pesi ~0.14–0.19): senza addestramento
non c'e' motivo perche' un token preferisca fortemente un altro. E' un
risultato onesto — in un Transformer vero sono proprio $W_Q,W_K,W_V$, una
volta imparate, a rendere la matrice informativa (es. un pronome che si
concentra sul suo referente).

## Collegamento al progetto

Il passo 31 aggiunge `contestualizza(frase)`: restituisce, per ogni token di
una memoria, un vettore contestualizzato piu' la matrice di attenzione. Un
`assert` verifica che ci sia una rappresentazione per token e che l'attenzione
sia normalizzata e quadrata. E' il componente che la Lezione 32 inserira'
dentro un **blocco Transformer** completo (residual + layer norm + FFN).

## Riepilogo

1. Self-attention: $Q=XW_Q$, $K=XW_K$, $V=XW_V$ dalla stessa sequenza.
2. Matrice di attenzione **quadrata** $n\times n$; $A_{ij}$ = quanto $i$
   guarda $j$.
3. Ogni token → media pesata di tutti i token (incluso se stesso).
4. $W_Q,W_K,W_V$ sono imparate; qui sono casuali per illustrare.
5. Output: una rappresentazione contestualizzata per token.
6. Stessa formula della Lezione 30, cambia solo la provenienza di Q/K/V.

## Fonti

- Vaswani et al., *Attention Is All You Need*, 2017 — <https://arxiv.org/abs/1706.03762>
