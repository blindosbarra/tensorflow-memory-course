---
id: memory-schema
title: Uno schema esplicito per la memoria
module: memory-representation
status: learner_review
estimated_minutes: 25
prerequisites: [retrieval-metrics]
deliverables: [notebooks/lezione-22-schema-memoria.ipynb]
sources:
  - https://docs.python.org/3/library/dataclasses.html
  - https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
---

# Uno schema esplicito per la memoria

> **La lezione si segue nel notebook**
> `notebooks/lezione-22-schema-memoria.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il ventiduesimo passo del
> progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.
> Prerequisito: Lezione 21. Apre la Fase 4 (rappresentare le memorie).

## Cosa saprai fare

Definire uno schema esplicito per una memoria con `dataclasses`, scrivere
una funzione di validazione che distingue errori bloccanti da avvisi, e
capire perche' formalizzare un contratto conta quando piu' lezioni
costruiscono sopra agli stessi dati.

## Teoria essenziale

La Lezione 1 distingueva gia' campi critici (`memory_id`, `text`,
`timestamp` — senza uno di questi la riga perde identita') da campi
recuperabili (`type`, `importance`): uno schema implicito. Oggi lo
rendiamo esplicito con `@dataclass` (struttura dichiarativa, libreria
standard, nessuna validazione automatica) e una funzione di validazione
dedicata che applica le regole del dominio, restituendo **errori**
bloccanti separati da **avvisi** non bloccanti — la stessa distinzione
critico/recuperabile, applicata alla validazione invece che alla scelta
scarto/imputazione.

## Nel progetto

`valida_memoria` applicata a tutte le memorie di train/val/test: zero
errori attesi (i dati sono gia' puliti dalle Lezioni 1-5), verificato con
un `assert` finale — non un secondo giro di pulizia, una prova di
correttezza su cui le lezioni successive della Fase 4 possono contare.

## Errori comuni

- Fermare la validazione al primo errore trovato invece di raccogliere
  tutti i problemi di un record.
- Trattare un valore leggermente fuori range come bloccante quanto un
  identificatore mancante: la gravita' del problema conta, non solo la
  sua esistenza.
- Confondere `@dataclass` (struttura dati) con una libreria di
  validazione: Python non controlla tipi o range da solo, va scritto
  esplicitamente.
- Saltare l'`assert` finale sul report aggregato, trasformando una
  garanzia verificabile in un'assunzione non controllata.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- Python, documentazione ufficiale, modulo `dataclasses`:
  https://docs.python.org/3/library/dataclasses.html
- pandas, `to_datetime`:
  https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
