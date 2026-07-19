---
id: rlhf-rlaif-overview
title: RLHF, RLAIF e DPO a confronto
module: preference-learning
status: learner_review
estimated_minutes: 28
prerequisites: [reward-functions, preference-tuning]
deliverables: [notebooks/lezione-50-rlhf-rlaif.ipynb]
sources:
  - https://arxiv.org/abs/2212.08073
  - https://arxiv.org/abs/2203.02155
---

# RLHF, RLAIF e DPO a confronto

> **La lezione si segue nel notebook**
> `notebooks/lezione-50-rlhf-rlaif.ipynb`: teoria, codice eseguibile, esercizio e il
> 50esimo passo del progetto Memory AI Lab. Questa pagina e' il riassunto di
> riferimento.

## Cosa saprai fare

Capire le tre famiglie di allineamento da preferenze e mostrare in NumPy come
un reward model faccia da etichettatore (RLAIF) al posto dell'umano.

## Teoria essenziale

**RLHF** (umani → reward model → RL con KL; Ouyang et al., 2022), **RLAIF**
(le preferenze le genera un modello; Bai et al., 2022) e **DPO** (ottimizza la
politica direttamente; Rafailov et al., 2023). RLHF vs RLAIF = **chi
etichetta**; DPO = **come si ottimizza** — assi ortogonali.

## Cosa mostra il notebook

Un giudice AI con rumore crescente concorda con l'umano `0.87 / 0.81 / 0.69 /
0.39`; una politica DPO addestrata su etichette di un giudice **buono** raggiunge
allineamento umano `0.964`, con un giudice **scadente** crolla a `-0.167`. La
qualita' del giudice si propaga alla politica. Output reali.

## Collegamento al progetto

Nel progetto, un reward model (Lezione 47) puo' fare da giudice AI per
etichettare nuove coppie a basso costo (RLAIF), a patto di monitorarne la
qualita' contro un campione umano.

## Fonti

- Bai et al., *Constitutional AI*, 2022 — <https://arxiv.org/abs/2212.08073>
- Ouyang et al., *InstructGPT*, 2022 — <https://arxiv.org/abs/2203.02155>
