---
id: episodic-semantic-preference
title: Episodic, semantic, preference
module: memory-representation
status: learner_review
estimated_minutes: 25
prerequisites: [memory-schema]
deliverables: [notebooks/lezione-23-episodic-semantic-preference.ipynb]
sources:
  - https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html
  - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
---

# Episodic, semantic, preference

> **La lezione si segue nel notebook**
> `notebooks/lezione-23-episodic-semantic-preference.ipynb`: teoria,
> dimostrazioni eseguibili, esercizio con soluzione spiegata e il
> ventitreesimo passo del progetto Memory AI Lab. Questa pagina e' il
> riassunto di riferimento. Prerequisito: Lezione 22.

## Cosa saprai fare

Caratterizzare episodic/semantic/preference/unknown con criteri concreti
(ancorato a un evento? fatto generale? opinione personale?), e costruire
una tabella di parametri per type che le Lezioni 24-25 useranno
direttamente.

## Teoria essenziale

I quattro `type` descrivono relazioni diverse col tempo e con
l'aggiornamento, non etichette intercambiabili: **episodic** (evento
ancorato a un momento, rilevanza che cala in fretta), **semantic** (fatto
generale, resta rilevante finche' resta vero, non decade col solo passare
del tempo), **preference** (opinione/impostazione, non decade ma va
controllata per sovrascritture), **unknown** (type non determinato con
sicurezza, peso ridotto per mancanza di informazione). La
caratterizzazione si traduce in due parametri dichiarati per type:
half-life (Lezione 24) e peso di importanza base (Lezione 25).

## Nel progetto

`PARAMETRI_TIPO` (dict con half-life e peso base per ciascuno dei 4 type)
applicato a tutto il train set con `Series.map`; riepilogo con
`groupby('type')`. Sono scelte di design dichiarate esplicitamente, non
misure — un sistema reale le calibrerebbe su dati d'uso.

## Errori comuni

- Trattare i quattro `type` come intercambiabili nelle lezioni successive
  (stesso half-life, stesso peso) invece di differenziarli.
- Presentare i valori di `PARAMETRI_TIPO` come misurati invece che come
  scelte di design dichiarate.
- Assumere che una preferenza vecchia sia automaticamente meno valida di
  una recente: il problema e' la sovrascrittura (Lezione 29), non il
  tempo passato.
- Dare a `unknown` lo stesso peso della media degli altri type invece di
  un peso ridotto che rifletta l'incertezza.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- pandas, `Series.map`:
  https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html
- pandas, `DataFrame.groupby`:
  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
