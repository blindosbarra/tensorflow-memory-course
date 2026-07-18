---
id: contradiction-and-update
title: Contraddizioni e aggiornamento
module: memory-representation
status: learner_review
estimated_minutes: 25
prerequisites: [hybrid-retrieval]
deliverables: [notebooks/lezione-29-contraddizioni.ipynb]
sources:
  - https://docs.python.org/3/library/re.html
---

# Contraddizioni e aggiornamento

> **La lezione si segue nel notebook**
> `notebooks/lezione-29-contraddizioni.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il ventinovesimo (e
> ultimo della Fase 4) passo del progetto Memory AI Lab. Questa pagina e'
> il riassunto di riferimento. Prerequisito: Lezione 28. Chiude la Fase 4.

## Cosa saprai fare

Rilevare una contraddizione tra due memorie `preference` con un'euristica
dichiarata (polarita' opposta + argomento condiviso), applicare una
politica di aggiornamento che non cancella mai (segna come superata,
mantiene la storia), e riconoscere onestamente i limiti dell'euristica su
casi che non copre.

## Teoria essenziale

Il tempo da solo (Lezione 24) non basta a decidere se una `preference` e'
ancora valida: serve confrontare il contenuto. Euristica: **polarita'**
(`positiva` se `likes`/`prefers`, `negativa` se `dislikes`) + **argomento**
(parole di contenuto dopo aver tolto il prefisso fisso e le parole
vuote). Due memorie sono in conflitto se hanno polarita' opposta e
condividono almeno una parola di argomento. La politica di aggiornamento
non cancella mai: marca la memoria vecchia con `superseded_by` (il
`memory_id` di quella nuova), mantenendo la storia — stesso principio dei
flag di audit della Lezione 1.

## Nel progetto

Tre nuove memorie `preference` confrontate con l'archivio storico (61
memorie): due (`"dislikes walking meetings"`, `"likes late
notifications"`) marcano rispettivamente 13 e 17 memorie storiche come
superate, nessuna cancellata (30 superate, 31 ancora valide, 61 totali).
La terza (`"prefers evening sessions"` contro una storica `"prefers
morning sessions"` sullo stesso progetto) **non** rileva alcun conflitto:
l'euristica cattura solo opposizioni di polarita' esplicita
(likes/dislikes), non valori diversi della stessa dimensione (mattina/
sera) — un limite dichiarato, dimostrato concretamente, non nascosto.

## Errori comuni

- Cancellare le memorie superate invece di marcarle, perdendo la storia.
- Aspettarsi che l'euristica rilevi qualunque tipo di contraddizione
  semantica, non solo i conflitti di polarita' esplicita.
- Applicare il rilevamento di contraddizioni a memorie `episodic` o
  `semantic`: la nozione di "superata da una nuova versione" e' propria
  delle `preference` (Lezione 23).
- Confrontare una nuova memoria solo con le memorie **non ancora
  superate**, dimenticando di ricalcolare la maschera booleana
  sull'intero archivio a ogni iterazione (un bug reale di allineamento
  indici incontrato durante lo sviluppo di questa lezione).

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- Python, documentazione ufficiale, modulo `re`:
  https://docs.python.org/3/library/re.html
