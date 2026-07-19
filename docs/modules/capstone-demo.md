---
id: capstone-demo
title: Demo: il Memory AI Lab al lavoro
module: capstone
status: learner_review
estimated_minutes: 28
prerequisites: [capstone-pipeline]
deliverables: [notebooks/lezione-60-capstone-demo.ipynb]
sources:
  - https://arxiv.org/abs/2305.18290
---

# Demo: il Memory AI Lab al lavoro

> **La lezione si segue nel notebook**
> `notebooks/lezione-60-capstone-demo.ipynb`: teoria, codice eseguibile, esercizio e il 60esimo
> passo del progetto Memory AI Lab. Questa pagina e' il riassunto di riferimento.

## Cosa saprai fare

Eseguire il lab completo su piu' memorie d'esempio e chiudere il corso.

## Teoria essenziale

Istanziamo `MemoryAILab` e lo eseguiamo su memorie eterogenee (episodiche, semantiche, di preferenza). Per ognuna otteniamo il record strutturato completo — il risultato di 60 lezioni.

## Cosa mostra il notebook

Su 4 memorie d'esempio, il lab produce i record e ne **archivia 2** (quelle sopra la soglia di importanza): 'Marco visited Glasgow' (episodic, 0.42) e 'The user prefers morning sessions' (preference, 0.60) vengono memorizzate; 'Water boils...' (0.28) e 'ok.' (0.12) no. `process` e' idempotente sull'id (nessun duplicato). Output reali.

## Collegamento al progetto

Il passo 60 chiude il corso: dal CSV grezzo (Fase 1) a un Memory AI Lab che pulisce, classifica, rappresenta, collega, valuta l'importanza, adatta modelli open (LoRA), impara dalle preferenze e si monitora dal drift.

## Fonti

- Rafailov et al., 2023, *Direct Preference Optimization* — <https://arxiv.org/abs/2305.18290>
