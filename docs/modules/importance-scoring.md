---
id: importance-scoring
title: Un punteggio di importanza composito
module: memory-representation
status: learner_review
estimated_minutes: 25
prerequisites: [time-recency-decay]
deliverables: [notebooks/lezione-25-importance-scoring.ipynb]
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html
---

# Un punteggio di importanza composito

> **La lezione si segue nel notebook**
> `notebooks/lezione-25-importance-scoring.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il venticinquesimo passo
> del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento. Prerequisito: Lezione 24.

## Cosa saprai fare

Combinare `importance` esplicito, `recency` e `peso_importanza_base` per
type in un unico punteggio composito con una somma pesata dichiarata, e
spiegare perche' i pesi vanno giustificati invece di essere scelti a caso.

## Teoria essenziale

`importanza_composita = peso_importanza_base * (alpha * importance +
beta * recency)`, con `alpha + beta = 1` (qui `0.6/0.4`: il giudizio
esplicito pesa piu' del solo fattore temporale, ma il tempo non e'
ignorato). I pesi sono una **dichiarazione di priorita'**, non un
parametro da ottimizzare in astratto. Il risultato non e' vincolato a
`[0,1]`: e' un punteggio di ranking, non una probabilita' — puo' superare
1.0 quando il peso di type e' maggiore di 1.

## Nel progetto

Applicato a tutto il train set: nell'esecuzione di riferimento il range va
da 0.058 a 1.077, con le posizioni piu' alte dominate da memorie
`preference` e `semantic` con `importance` esplicito e recency entrambi
alti. Nessuna `episodic` compare in cima: con half-life corto (Lezione 24)
quasi tutte hanno gia' recency bassa, indipendentemente da quanto fosse
alto il loro `importance` originale — un comportamento voluto della
formula.

## Errori comuni

- Scegliere i pesi `alpha`/`beta` senza dichiarare la priorita' che
  rappresentano, come se fossero un dettaglio tecnico neutro.
- Aspettarsi che `importanza_composita` resti in `[0,1]` come una
  probabilita': e' un punteggio di ranking, il range dipende dai pesi di
  type.
- Interpretare un punteggio composito basso per una memoria con
  `importance` esplicito alto come un errore, invece di riconoscere
  l'effetto voluto della recency bassa.
- Ricalcolare `recency` con parametri diversi da quelli della Lezione 24,
  rompendo la coerenza tra le due lezioni.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- pandas, `DataFrame.sort_values`:
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html
