---
id: gemma-lora
title: LoRA su Gemma
module: lora
status: learner_review
estimated_minutes: 25
prerequisites: [gemma-inference, lora-from-scratch]
deliverables: [notebooks/lezione-41-gemma-lora.ipynb]
sources:
  - https://keras.io/keras_hub/api/models/gemma/
  - https://arxiv.org/abs/2106.09685
---

# LoRA su Gemma

> **La lezione si segue nel notebook**
> `notebooks/lezione-41-gemma-lora.ipynb`. Prerequisiti: Lezioni 35, 40.
>
> ⚠️ **Nota di ambiente.** Le celle Gemma sono **guardate** e saltate in questo
> ambiente/CI (pesi gated). Il codice e' l'API reale; la parte di progetto e'
> eseguibile. Vedi `course/research_gaps.md`.

## Cosa saprai fare

Attivare LoRA su Gemma via KerasHub (`backbone.enable_lora(rank=...)`) e stimare
il risparmio di parametri, capendo cosa cambia rispetto alla LoRA costruita a
mano nella Lezione 40.

## Teoria essenziale

Nella Lezione 40 abbiamo inserito a mano $B,A$ dentro un singolo strato. Su un
modello vero non serve: KerasHub espone `backbone.enable_lora(rank=r)`, che
**inietta** gli adapter LoRA negli strati di attenzione, **congela** i pesi
originali e rende addestrabili solo gli adapter. Poi si addestra col normale
`fit`, ma i parametri addestrabili crollano — esattamente il risparmio della
Lezione 39.

## Cosa mostra il notebook

La cella `enable_lora` (guardata) e' l'API reale. La cella di **progetto**
eseguibile stima il risparmio su uno strato di attenzione di dimensione tipica
di Gemma-2B ($d\_model\approx2048$, ~18 blocchi, ~4 proiezioni per blocco): con
$r=4$ si addestra **~0.39%** dei parametri di attenzione (riduzione ~256x).
Numero realmente eseguito con la formula della Lezione 39 (le dimensioni sono
d'ordine di grandezza, dichiarate come tali).

## Collegamento al progetto

Il passo 41 aggiunge `stima_trainable_lora(...)`: giustifica quantitativamente
perche' LoRA rende praticabile adattare Gemma. Gli adapter risultanti sono
piccoli e portabili (Lezione 44) e la qualita' va confrontata con una baseline
(Lezione 43).

## Riepilogo

1. Su Gemma: `backbone.enable_lora(rank=r)`, non si riscrivono gli strati.
2. Inietta adapter negli strati di attenzione, congela il resto.
3. Si addestra col normale `fit`, parametri addestrabili minimi.
4. Stessa idea della Lezione 40, su un modello reale.
5. Con $r=4$ su Gemma-2B si addestra ben meno dell'1% dell'attenzione.

## Fonti

- *Gemma models — KerasHub* — <https://keras.io/keras_hub/api/models/gemma/>
- Hu et al., *LoRA*, 2021 — <https://arxiv.org/abs/2106.09685>
