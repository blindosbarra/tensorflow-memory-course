---
id: baseline-comparison
title: 'LoRA vs full fine-tuning: il confronto'
module: lora
status: learner_review
estimated_minutes: 30
prerequisites: [lora-from-scratch]
deliverables: [notebooks/lezione-43-baseline-comparison.ipynb]
sources:
  - https://arxiv.org/abs/2106.09685
---

# LoRA vs full fine-tuning: il confronto

> **La lezione si segue nel notebook**
> `notebooks/lezione-43-baseline-comparison.ipynb`: **interamente eseguibile**
> in NumPy. Prerequisito: Lezione 40.

## Cosa saprai fare

Confrontare davvero full fine-tuning e LoRA sullo stesso compito — parametri
addestrati e perdita finale — e scegliere il rango piu' piccolo che basta.

## Teoria essenziale

LoRA punta a *quasi* la qualita' del full fine-tuning con pochissimi parametri.
"Quasi" quanto dipende dal rango $r$ e dalla natura dell'aggiornamento: quando
$\Delta W$ e' davvero a **rango basso** (la premessa della Lezione 39), un
adapter con $r$ sufficiente raggiunge il full fine-tuning.

## Cosa mostra il notebook

Su un compito dove l'aggiornamento vero e' di **rango 3**, i risultati eseguiti:

| strategia | parametri | perdita |
|-----------|-----------|---------|
| full fine-tuning | 384 | 0.0 |
| LoRA r=1 | 40 | 9.221 |
| LoRA r=2 | 80 | 3.128 |
| **LoRA r=3** | **120** | **0.0** |
| LoRA r=4 | 160 | 0.0 |
| LoRA r=8 | 320 | 0.0 |

A $r=3$ (il rango vero) LoRA **eguaglia** il full fine-tuning con un terzo dei
parametri; oltre $r=3$ il guadagno e' nullo. La funzione `scegli_rango`
seleziona correttamente il rango piu' piccolo sotto la soglia di perdita (r=3).
Nota di onesta': una prima stesura usava un aggiornamento a rango pieno — dove
LoRA *non puo'* eguagliare il full FT — ed e' stata corretta a un aggiornamento
a rango basso, cosi' il confronto riflette davvero la premessa di LoRA.

## Collegamento al progetto

Il passo 43 aggiunge `scegli_rango(risultati, perdita_max)`: dato un budget di
qualita', sceglie il rango piu' piccolo che lo rispetta — la decisione tipica
quando si adatta il modello del progetto.

## Riepilogo

1. LoRA punta a *quasi* la qualita' del full con pochi parametri.
2. Il rango $r$ regola il compromesso qualita'/costo.
3. Se $\Delta W$ e' a rango basso, $r \ge$ quel rango eguaglia il full.
4. Oltre il rango vero il guadagno e' marginale.
5. La scelta pratica: il rango **piu' piccolo** sotto la soglia.
6. Full fine-tuning e' il tetto di riferimento.

## Fonti

- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685>
