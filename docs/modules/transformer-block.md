---
id: transformer-block
title: Il blocco Transformer
module: transformers-gemma
status: learner_review
estimated_minutes: 30
prerequisites: [self-attention-math]
deliverables: [notebooks/lezione-32-blocco-transformer.ipynb]
sources:
  - https://arxiv.org/abs/1706.03762
---

# Il blocco Transformer

> **La lezione si segue nel notebook**
> `notebooks/lezione-32-blocco-transformer.ipynb`: teoria, implementazione
> eseguibile in NumPy, esercizio e il trentaduesimo passo del progetto Memory
> AI Lab. Questa pagina e' il riassunto di riferimento. Prerequisito: Lezione
> 31.

## Cosa saprai fare

Assemblare un **blocco Transformer encoder** completo in NumPy — self-attention
+ connessione residua + layer normalization + rete feed-forward — e capire
perche' la forma della sequenza si conserva, cosi' i blocchi si possono
impilare.

## Teoria essenziale

La self-attention (Lezione 31) e' il cuore ma non basta. Il blocco la avvolge
in tre ingredienti (Vaswani et al., 2017, Sez. 3.1 e 3.3):

- **Connessione residua**: `x + Sublayer(x)`. Il gradiente fluisce meglio e lo
  strato impara una *correzione*, non tutto da capo. Richiede che il
  sotto-strato conservi `d_model`.
- **Layer normalization**: porta ogni vettore-token a media 0 e varianza 1
  sulle sue feature, stabilizzando l'addestramento.
- **FFN posizionale**: due trasformazioni lineari con una non-linearita' (ReLU)
  in mezzo, applicate **indipendentemente a ogni posizione**.

Struttura (variante *post-norm* dell'articolo originale):

```text
x -> [self-attention] -> +x -> LayerNorm -> [FFN] -> +. -> LayerNorm -> out
```

La forma entra `(n, d_model)` ed esce **identica**: per questo i blocchi si
impilano in un encoder profondo.

## Cosa mostra il notebook

La memoria `"The user prefers morning sessions"` (5 token) entra come `(5, 16)`
ed esce come `(5, 16)`. Dopo la layer norm finale ogni riga (token) ha media
~0 e deviazione standard ~1 (output realmente eseguito). Impilando 3 blocchi la
forma resta `(5, 16)` e la norma media per token resta 4.0 = $\sqrt{16}$ — cioe'
esattamente quello che la layer norm impone (vettori a varianza unitaria). E'
la proprieta' che rende praticabile impilare decine di blocchi identici.

## Collegamento al progetto

Il passo 32 aggiunge `encoder_memoria(frase, n_blocchi)`: una pila di blocchi
che trasforma una memoria in una sequenza di vettori contestualizzati piu' un
vettore-riassunto (media dei token) — l'analogo "Transformer" del
sentence-embedding della Lezione 17. Un `assert` verifica forma della sequenza
e dimensione del riassunto. E' l'architettura che modelli come **Gemma**
(Lezioni 34–35) ripetono molte volte, con pesi imparati su enormi corpora.

## Riepilogo

1. Blocco = self-attention + residua + layer norm + FFN.
2. Residua `x + Sublayer(x)`: gradiente fluido, si impara una correzione.
3. Layer norm: ogni token a media 0 / varianza 1.
4. FFN posizionale: due lineari + non-linearita', per posizione.
5. Forma conservata `(n, d_model)` → i blocchi si impilano.
6. Pooling finale → vettore-riassunto della memoria.

## Fonti

- Vaswani et al., *Attention Is All You Need*, 2017 — <https://arxiv.org/abs/1706.03762>
