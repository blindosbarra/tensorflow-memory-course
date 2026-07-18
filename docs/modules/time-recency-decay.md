---
id: time-recency-decay
title: Decadimento temporale (recency)
module: memory-representation
status: learner_review
estimated_minutes: 25
prerequisites: [episodic-semantic-preference]
deliverables: [notebooks/lezione-24-recency-decay.ipynb]
sources:
  - https://en.wikipedia.org/wiki/Exponential_decay
  - https://en.wikipedia.org/wiki/Half-life
  - https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html
---

# Decadimento temporale (recency)

> **La lezione si segue nel notebook** `notebooks/lezione-24-recency-decay.ipynb`:
> teoria, dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> ventiquattresimo passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 23.

## Cosa saprai fare

Implementare il decadimento esponenziale con half-life
(`recency = 0.5 ** (eta / half_life)`), spiegare perche' un riferimento
temporale fisso e dichiarato e' necessario per la riproducibilita', e
calcolare la recency di ogni memoria usando l'half-life per type della
Lezione 23.

## Teoria essenziale

Il decadimento esponenziale garantisce, per costruzione, che
`recency(eta = half_life) = 0.5`: non e' un'osservazione empirica, e' una
conseguenza diretta della formula. `recency` non scende mai sotto zero e
non si azzera mai del tutto, a differenza di un decadimento lineare. Il
riferimento temporale (`ORA_RIFERIMENTO`) va **fissato e dichiarato**
invece di usare `datetime.now()`, per lo stesso motivo per cui le lezioni
con reti neurali fissano un seed: senza un valore fisso, due esecuzioni
dello stesso notebook non sono confrontabili e un `assert` non puo'
restare valido nel tempo.

## Nel progetto

`recency_score(timestamp, half_life_giorni)` applicato a tutto il train
set con l'half-life per type della Lezione 23. Nell'esecuzione di
riferimento, a parita' di eta' anagrafica (~74 giorni medi), le memorie
`episodic` (half-life 30gg) hanno recency media 0.209 mentre le `semantic`
(half-life 365gg) restano a 0.871 — la stessa distanza temporale, punteggi
molto diversi, perche' l'half-life e' diverso per type.

## Errori comuni

- Usare `datetime.now()` invece di un riferimento temporale fisso e
  dichiarato, rompendo la riproducibilita' del notebook.
- Applicare lo stesso half-life a tutti i type, vanificando la
  differenziazione della Lezione 23.
- Usare un decadimento lineare senza gestire il troncamento a zero,
  invece del decadimento esponenziale che resta sempre positivo.
- Confondere l'eta' anagrafica di una memoria con la sua recency: sono
  collegate ma non equivalenti, perche' l'half-life le mette in relazione
  in modo diverso per ogni type.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- Wikipedia, *Exponential decay*:
  https://en.wikipedia.org/wiki/Exponential_decay
- Wikipedia, *Half-life*:
  https://en.wikipedia.org/wiki/Half-life
- pandas, `Timestamp`:
  https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html
