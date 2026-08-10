# Piano WI-6 — lezioni 46-48

## Fetta scelta

Approfondire il segmento formato dalle lezioni 46-48 (coppie chosen/rejected,
reward function con Bradley-Terry, intuizione di DPO). Le lezioni 31-45 sono
gia' coperte dalle iterazioni precedenti; le lezioni 49-60 restano fuori da
questa fetta.

## Fonti scelte (da aprire e verificare in questa sessione)

- `github.com/huggingface/trl` (`docs/source/reward_trainer.md`): requisiti
  del dataset (campi chosen/rejected, filtro dei pareggi, margine come
  metrica loggata) per la lezione 46; formula esatta della loss Bradley-Terry
  per la lezione 47.
- `github.com/huggingface/trl` (`docs/source/dpo_trainer.md`): formula
  esatta della loss DPO, ruolo di beta, e l'affermazione che DPO elimina il
  campionamento dal modello linguistico durante il training, per la
  lezione 48.
- arxiv.org resta bloccato dal proxy in questa sessione: le fonti arXiv gia'
  citate nei pack (InstructGPT, DPO) restano `needs_reverification`, non
  vengono ripromosse; le fonti nuove usano solo sorgenti raggiungibili.

## Passi

1. Ampliare la teoria delle coppie chosen/rejected, della reward function
   Bradley-Terry e dell'intuizione DPO senza modificare gli esempi
   eseguibili (celle di codice invariate).
2. Registrare nello stesso commit le nuove affermazioni nei tre research
   pack (`knowledge/chosen-rejected-data`, `knowledge/reward-functions`,
   `knowledge/dpo-intuition`), usando le fonti aperte durante questa
   iterazione.
3. Riportare le tre lezioni a `technical_review` in `course/progress.yaml`
   e aggiornare l'handover di WI-6 con il residuo 49-60.
4. Eseguire prima i tre notebook interessati, ripristinare gli eventuali
   dataset prodotti dal run parziale, quindi eseguire il gate completo
   61/61.
