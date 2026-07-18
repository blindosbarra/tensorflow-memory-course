---
id: graph-memory-networkx
title: Il grafo delle memorie
module: memory-representation
status: learner_review
estimated_minutes: 30
prerequisites: [entity-event-relations]
deliverables: [notebooks/lezione-27-grafo-memorie.ipynb]
sources:
  - https://networkx.org/documentation/stable/reference/classes/graph.html
  - https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
---

# Il grafo delle memorie

> **La lezione si segue nel notebook**
> `notebooks/lezione-27-grafo-memorie.ipynb`: teoria, dimostrazioni
> eseguibili, esercizio con soluzione spiegata e il ventisettesimo passo
> del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento. Prerequisito: Lezione 26.

## Cosa saprai fare

Costruire un grafo bipartito memoria-entita' con `networkx`, interrogarlo
per trovare memorie correlate a piu' salti (via entita' condivisa), e
visualizzarlo.

## Teoria essenziale

Un grafo **bipartito** ha due tipi di nodo (memoria, entita'): ogni arco
collega sempre un nodo di un tipo all'altro, mai due nodi dello stesso
tipo direttamente. Una tabella piatta risponde bene a lookup diretti
("quali memorie menzionano Lucia?") ma non a domande a **piu' salti**
("quali altre memorie condividono un'entita' con questa memoria
specifica?"), che richiedono di attraversare memoria -> entita' -> altre
memorie. Il **grado** di un nodo entita' e' quante memorie la
menzionano; i **vicini a 2 salti** di una memoria sono le altre memorie
che condividono almeno un'entita' con essa.

## Nel progetto

Grafo bipartito su tutto il train set: 227 nodi (213 memorie, 14 entita'),
241 archi nell'esecuzione di riferimento. `memorie_correlate(memory_id)`
trova le memorie a 2 salti — un segnale di correlazione basato su un fatto
esplicito condiviso, diverso dalla similarita' per embedding (Lezioni
17-18): due memorie possono condividere un'entita' pur avendo embedding
poco simili, o viceversa. Le entita' piu' connesse (hub del grafo) sono
visivamente evidenti nella visualizzazione con `spring_layout`.

## Errori comuni

- Aggiungere archi diretti tra due memorie o tra due entita' in un grafo
  che e' pensato come bipartito, rompendo la struttura.
- Confondere il grado di un'entita' (quante memorie la menzionano) con la
  sua importanza semantica: e' solo una misura di connettivita'.
- Aspettarsi che `memorie_correlate` trovi le stesse connessioni della
  similarita' coseno: sono segnali diversi, complementari.
- Visualizzare l'intero grafo senza filtrare (con centinaia di nodi
  memoria) invece di limitarsi a un sottografo leggibile.

## Quiz

Le domande e le risposte commentate sono nel notebook della lezione.

## Fonti

- NetworkX, `Graph`:
  https://networkx.org/documentation/stable/reference/classes/graph.html
- NetworkX, `spring_layout`:
  https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
