---
id: lora-from-scratch
title: 'LoRA da zero: addestrare un adapter'
module: lora
status: learner_review
estimated_minutes: 30
prerequisites: [lora-math]
deliverables: [notebooks/lezione-40-lora-from-scratch.ipynb]
sources:
  - https://arxiv.org/abs/2106.09685
---

# LoRA da zero: addestrare un adapter

> **La lezione si segue nel notebook**
> `notebooks/lezione-40-lora-from-scratch.ipynb`: **interamente eseguibile** in
> NumPy. Prerequisito: Lezione 39.

## Cosa saprai fare

Addestrare davvero un adapter LoRA in NumPy su un compito giocattolo, tenendo
$W_0$ congelato, e vedere la perdita scendere con pochissimi parametri.

## Teoria essenziale

Uno strato LoRA calcola $y = x(W_0 + \frac{\alpha}{r}BA)$. Convenzioni (Hu et
al., 2021):

- $A$ casuale piccola, $B=0$ → all'avvio $BA=0$, il modello parte **identico**
  al pre-addestrato (nessuno shock iniziale).
- si addestrano solo $A,B$ via gradient descent; $W_0$ resta fermo.
- il fattore $\alpha/r$ scala l'effetto dell'adapter.

## Cosa mostra il notebook

Su una regressione giocattolo ($d=16,k=8,r=2$) la perdita parte da `5.6381`
(adapter nullo = solo $W_0$) e scende a `2.6155` in 300 passi di gradient
descent scritto a mano — un miglioramento di 2.2x, **senza mai toccare $W_0$**
(verificato con `np.array_equal`). Il miglioramento e' parziale e onesto: un
adapter di rango 2 puo' fittare solo in parte un aggiornamento a rango pieno.
Un `assert` conferma che un adapter appena creato ($B=0$) riproduce esattamente
l'output di solo $W_0$. Parametri addestrati: 48 vs 128 del pieno.

## Collegamento al progetto

Il passo 40 impacchetta `crea_adapter` / `applica_lora` con le convenzioni
corrette. E' il mattone che la Lezione 41 innesterebbe dentro Gemma.

## Riepilogo

1. Strato LoRA: $y = x(W_0 + \frac{\alpha}{r}BA)$.
2. $A$ piccola casuale, $B=0$ → si parte identici al pre-addestrato.
3. Si addestrano solo $A,B$; $W_0$ congelato (verificato bit a bit).
4. La perdita scende: l'adapter impara l'aggiornamento del compito.
5. $\alpha/r$ scala l'effetto.
6. Pochissimi parametri rispetto al pieno.

## Fonti

- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685>
