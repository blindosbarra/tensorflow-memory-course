# Piano WI-6 — lezioni 43-45

## Fetta scelta

Approfondire il segmento formato dalle lezioni 43-45 (confronto LoRA/full
fine-tuning, packaging degli adapter, schema del feedback — apertura della
Fase 7). Le lezioni 31-42 sono gia' coperte dalle iterazioni precedenti; le
lezioni 46-60 restano fuori da questa fetta.

## Fonti scelte (da aprire e verificare in questa sessione)

- `github.com/microsoft/LoRA` (README ufficiale): numeri concreti del
  confronto RoBERTa base full fine-tuning vs LoRA (parametri addestrati e
  punteggio medio GLUE) per la lezione 43; comportamento di merge/eval e
  assenza di latenza aggiuntiva in inferenza per la lezione 44.
- `github.com/huggingface/trl` (`docs/source/dataset_formats.md`): la
  convenzione (prompt, chosen, rejected) per i dataset di preferenza, per la
  lezione 45.
- arxiv.org e' bloccato dal proxy in questa sessione: le fonti arXiv gia'
  citate nei pack (LoRA, InstructGPT) restano `needs_reverification`, non
  vengono ripromosse; le fonti nuove usano solo sorgenti raggiungibili.

## Passi

1. Ampliare la teoria del confronto LoRA/full fine-tuning, del packaging
   degli adapter e dello schema di feedback senza modificare gli esempi
   eseguibili (celle di codice invariate).
2. Registrare nello stesso commit le nuove affermazioni nei tre research
   pack (`knowledge/baseline-comparison`, `knowledge/adapter-packaging`,
   `knowledge/feedback-schema`), usando le fonti aperte durante questa
   iterazione.
3. Riportare le tre lezioni a `technical_review` in `course/progress.yaml`
   e aggiornare l'handover di WI-6 con il residuo 46-60.
4. Eseguire prima i tre notebook interessati, ripristinare gli eventuali
   dataset prodotti dal run parziale, quindi eseguire il gate completo
   61/61.
