---
id: adapter-packaging
title: Impacchettare e distribuire un adapter
module: lora
status: learner_review
estimated_minutes: 25
prerequisites: [lora-from-scratch]
deliverables: [notebooks/lezione-44-adapter-packaging.ipynb]
sources:
  - https://arxiv.org/abs/2106.09685
---

# Impacchettare e distribuire un adapter

> **La lezione si segue nel notebook**
> `notebooks/lezione-44-adapter-packaging.ipynb`: **interamente eseguibile** in
> NumPy. Prerequisito: Lezione 40. Chiude la Fase 6.

## Cosa saprai fare

Salvare e ricaricare solo l'adapter LoRA (pochi KB) invece dell'intero modello,
verificando che l'output resti identico.

## Teoria essenziale

L'adattamento LoRA vive in due piccole matrici $A,B$. Non serve distribuire un
modello da gigabyte per ogni compito: si distribuisce un **adapter** da pochi
KB, applicato sopra la stessa base condivisa. Piu' compiti = piu' adapter
intercambiabili, un solo modello base. Salvare l'adapter = salvare $A,B$ e i
metadati (rango, scala); ricaricarlo sulla base congelata da' lo **stesso**
comportamento.

## Cosa mostra il notebook

L'adapter salvato con `np.savez` occupa `4052` byte contro `32768` della sola
base $W_0$ (~**8x piu' piccolo**) — e la base non viene nemmeno distribuita. Dopo
salva/ricarica, un `assert` verifica che l'output sia **identico** (`atol=1e-6`)
e che il rango venga ripristinato dai metadati. Il notebook rimuove i propri
file temporanei alla fine (nessun artefatto committato). Numeri realmente
eseguiti.

## Collegamento al progetto

Il passo 44 aggiunge `salva_adapter` / `carica_adapter` con i metadati necessari
a riapplicare l'adapter senza indovinare iperparametri. E' l'ultimo mattone
della Fase 6: il progetto puo' tenere piu' adapter (uno per tipo di adattamento)
sopra un'unica base.

## Riepilogo

1. L'adattamento vive in due piccole matrici $A,B$.
2. Distribuisci un **adapter** (pochi KB), non un modello da gigabyte.
3. Una sola base condivisa + molti adapter intercambiabili.
4. Salvare = $A,B$ + metadati (rango, scala).
5. Ricaricare sulla stessa base da' output **identico** (verificato).
6. Chiude la Fase 6.

## Fonti

- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685>
