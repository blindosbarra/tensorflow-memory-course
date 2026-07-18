---
id: entity-event-relations
title: Entita' e relazioni
module: memory-representation
status: learner_review
estimated_minutes: 25
prerequisites: [importance-scoring]
deliverables: [notebooks/lezione-26-entita-e-relazioni.ipynb]
sources:
  - https://docs.python.org/3/library/re.html
  - https://docs.python.org/3/library/itertools.html#itertools.combinations
---

# Entita' e relazioni

> **La lezione si segue nel notebook**
> `notebooks/lezione-26-entita-e-relazioni.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il ventiseiesimo passo
> del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento. Prerequisito: Lezione 25.

## Cosa saprai fare

Estrarre entita' da un testo con un'euristica basata su espressioni
regolari, spiegarne onestamente i limiti rispetto a un vero sistema di
NER, e costruire la mappa entita' -> memorie e le co-occorrenze tra
entita' per l'intero archivio.

## Teoria essenziale

Senza libreria di NER installata ne' accesso di rete per scaricarne una,
l'estrazione usa un'**euristica dichiarata**: parole capitalizzate che non
sono la prima parola della frase (le frasi normali iniziano comunque con
maiuscola), con una lista di esclusione (`STOPWORD_MAIUSCOLE`) costruita
osservando i falsi positivi su questo dataset. Limiti dichiarati: nessuna
distinzione persona/luogo/altro, nessuna gestione di entita' multi-parola,
dipendenza dalla capitalizzazione, lista di esclusione non universale.

## Nel progetto

`estrai_entita` applicata a tutto il train set: nell'esecuzione di
riferimento 157 memorie su 213 (~74%) contengono almeno un'entita'
riconosciuta. La mappa entita' -> memorie e le coppie di co-occorrenza
(entita' che compaiono nella stessa memoria) sono i dati grezzi da cui la
Lezione 27 costruisce un grafo navigabile.

## Errori comuni

- Trattare l'euristica come un vero NER, aspettandosi che distingua
  persone da luoghi.
- Riusare `STOPWORD_MAIUSCOLE` su un testo diverso senza rivederla: e'
  costruita osservando i falsi positivi di **questo** dataset.
- Confondere le co-occorrenze (dati grezzi) con un grafo vero e proprio
  (struttura esplicita di nodi e archi, Lezione 27).
- Ignorare le memorie senza entita' riconosciute invece di trattarle come
  un caso normale e atteso (frasi generiche senza nomi propri).

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- Python, documentazione ufficiale, modulo `re`:
  https://docs.python.org/3/library/re.html
- Python, documentazione ufficiale, `itertools.combinations`:
  https://docs.python.org/3/library/itertools.html#itertools.combinations
