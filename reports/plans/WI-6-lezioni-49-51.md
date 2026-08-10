# Piano WI-6 — lezioni 49-51

## Fetta scelta

Approfondire il segmento formato dalle lezioni 49-51 (preference tuning di
una politica DPO, RLHF/RLAIF/DPO a confronto, rischi del preference learning
online). Le lezioni 31-48 sono gia' coperte dalle iterazioni precedenti; le
lezioni 52-60 (capstone) restano fuori da questa fetta.

## Fonti scelte (aperte e verificate in questa sessione)

- `github.com/huggingface/trl` (`docs/source/dpo_trainer.md`, sezione
  "Logged metrics"): definizione esatta di `rewards/accuracies` e
  `rewards/margins`, le stesse due quantita' che il notebook 49 calcola come
  `accuratezza()` e `margine_dpo()`. Diversa dalla citazione gia' usata nella
  lezione 48 (stessa pagina, ma la sezione sul significato di beta e
  sull'eliminazione del campionamento dal modello linguistico), per evitare
  di duplicare la stessa affermazione.
- `github.com/huggingface/trl` (`docs/source/index.md`): la tassonomia dei
  trainer in "Online methods" (PPOTrainer, GRPOTrainer, RLOOTrainer,
  OnlineDPOTrainer, ...) e "Offline methods" (DPOTrainer, SFTTrainer,
  KTOTrainer, ...), un secondo riscontro indipendente dell'asse "come si
  ottimizza" gia' insegnato nella lezione 50. Nota: la pagina non definisce
  in prosa cosa renda un metodo online/offline — la claim registrata e' solo
  la classificazione stessa, non un'interpretazione del motivo.
- `github.com/huggingface/trl` (`docs/source/reward_trainer.md`, blocco TIP
  su `center_rewards_coefficient`): la sottodeterminazione del modello
  Bradley-Terry (sommare una costante a tutti i reward non cambia le
  probabilita' di preferenza) e la mitigazione via `center_rewards_coefficient`,
  citando "Helping or Herding? Reward Model Ensembles Mitigate but do not
  Eliminate Reward Hacking" come motivazione — un rischio di reward hacking
  strutturale, distinto dall'over-ottimizzazione online gia' mostrata nella
  lezione 51. Il paper citato (su huggingface.co/papers) non e' stato aperto
  direttamente: la claim copre solo cio' che la pagina TRL stessa afferma.
- arxiv.org resta bloccato dal proxy in questa sessione: le fonti arXiv gia'
  citate nei tre pack (Rafailov 2023, Constitutional AI, Ouyang 2022,
  Gao et al. 2022) restano `needs_reverification`, non vengono ripromosse
  senza averle lette davvero.

## Passi

1. Ampliare la teoria delle tre lezioni senza modificare gli esempi
   eseguibili (celle di codice invariate); un solo paragrafo nuovo per
   lezione, con fonte primaria in coda alla cella "Teoria essenziale",
   seguendo esattamente il formato delle fette precedenti (46-48, 43-45...).
2. Registrare nello stesso commit le nuove affermazioni nei tre research
   pack (`knowledge/preference-tuning`, `knowledge/rlhf-rlaif-overview`,
   `knowledge/online-learning-risks`), usando solo le fonti aperte durante
   questa iterazione.
3. Riportare le tre lezioni a `technical_review` in `course/progress.yaml` e
   aggiornare l'handover di WI-6 con il residuo 52-60.
4. Eseguire prima i tre notebook interessati (`--only`), ripristinare gli
   eventuali dataset prodotti dal run parziale con `git checkout --
   datasets/`, quindi eseguire il gate completo 61/61.

## Trappola da tenere presente (dal segmento 40-42)

Mai scrivere formule LaTeX (`\right)`, `\alpha`, `\beta`, `\theta`...)
attraverso un layer che interpreta gli escape (heredoc, `echo`, shell). Ogni
cella e' stata modificata caricando il notebook con `json.load`, mutando la
lista `source` della cella in Python con stringhe letterali (`\\pi_\\theta`,
ecc. gia' presenti nel file, non toccate) e scrivendo con
`json.dump(..., ensure_ascii=False, indent=1)` seguito da una newline
finale. Verificato con `nbformat.validate`, un controllo di caratteri di
controllo (`[\x00-\x08\x0b-\x1f]`) e un confronto `tail -c 5 | od -c` con un
notebook non toccato.

Trappola di formattazione emersa in questa fetta: l'ultima riga di ogni
cella "Teoria essenziale" toccata **non** terminava con `\n` (convenzione
nbformat per l'ultimo elemento di `source`). Un primo tentativo ha aggiunto
il nuovo paragrafo direttamente dopo, senza correggere quella riga: il
risultato concatenava l'ultima frase del paragrafo precedente al nuovo senza
riga vuota fra i due (un solo `\n`, non due), fondendo visivamente i due
paragrafi in uno. Corretto aggiungendo esplicitamente `\n` alla vecchia
ultima riga prima di appendere il nuovo blocco — verificato confrontando il
diff con quello del commit 7db71f0 (fetta 46-48), che segue lo stesso
pattern.
