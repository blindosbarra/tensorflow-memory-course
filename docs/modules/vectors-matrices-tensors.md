---
id: vectors-matrices-tensors
title: Vettori, matrici e tensori
module: foundations
status: learner_review
estimated_minutes: 30
prerequisites: [python-numpy-refresh]
deliverables: [notebooks/lezione-07-tensori.ipynb]
sources:
  - https://numpy.org/doc/stable/user/basics.broadcasting.html
  - https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
---

# Vettori, matrici e tensori

> **La lezione si segue nel notebook** `notebooks/lezione-07-tensori.ipynb`.
> Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Leggere e prevedere le forme dei dati: vettori, matrici e tensori; il
prodotto scalare come somma pesata (un neurone e' questo); la regola
`(n, k) @ (k, m) -> (n, m)`; il broadcasting.

## Nel progetto

Il gesto fondamentale: `X @ W` produce i punteggi delle 4 classi per tutte
le memorie in una moltiplicazione. Con pesi casuali l'accuratezza e' da
baseline — l'asticella che le lezioni successive imparano a superare.

## Fonti

- NumPy, *Broadcasting*:
  https://numpy.org/doc/stable/user/basics.broadcasting.html
- NumPy, `matmul`:
  https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
