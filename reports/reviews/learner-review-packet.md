# Packet di avvio — learner review umana

## Cosa blocca cosa

`course/progress.yaml` (`course_status`) e' fermo su
`fasi_0_6_e_8_9_autorate_fase_7_mlops_non_costruita_in_attesa_di_learner_review_umana`:
tutto il contenuto autorabile e' scritto, ma nessuna lezione puo' passare da
`learner_review` a `done` senza un verdetto umano — e' l'ultimo gate della
state machine (`COURSE_FACTORY_SPEC.md` §8) e non e' delegabile a un agente
per costruzione.

**Nessuna lezione ha oggi un verdetto formale.** `templates/learner-review.md`
esiste dal rework del 2026-07-12, ma `reports/reviews/` non contiene ancora
nessun file `*-learner-review.md` compilato. La nota di progress.yaml del
2026-07-12 ("learner PASSED the notebook format on lesson 1") registra
un'approvazione del **formato**, non il verdetto formale con quiz/tempo/
chiarezza che il template chiede — non conta come review gia' fatta.

**Non tutte le 60 lezioni sono pronte per questo passo.** Contando
`course/progress.yaml` per stato:

| Stato | Lezioni | Range |
|---|---|---|
| `learner_review` (pronte, in attesa del solo umano) | **30** | lezioni 01-30 |
| `technical_review` (non ancora pronte) | 30 | lezioni 31-60 |
| `planned` / `writing` | 11 | moduli mlops e code non ancora scritti |

Le lezioni 31-60 sono tornate a `technical_review` durante WI-6 (che ha
approfondito la teoria di tutta la seconda meta' del corso): quel contenuto
nuovo non ha ancora attraversato una review tecnica, quindi non e' corretto
proporlo a un revisore umano adesso — leggerebbe testo mai controllato e il
suo giudizio si mischierebbe con un gate diverso. Questo packet copre quindi
**solo le 30 lezioni gia' in `learner_review`** (01-30); le altre 30 restano
un item successivo, dopo la loro technical_review.

## Le 3 lezioni da leggere per prime

Non tutte le 30 lezioni pronte insieme: queste tre danno il segnale piu' alto
con il minimo investimento di tempo, e coprono tre rischi diversi.

### 1. Lezione 01 — `data-cleaning-01-missing-values` (`notebooks/lezione-01-dati-mancanti.ipynb`)

**Perche' per prima.** E' l'unica lezione del corso ad aver gia' fallito una
review umana in passato (`course/progress.yaml`, nota del 2026-07-11:
*"learner review failed course content; both existing lessons were
reworked"*) e ad essere stata riscritta da zero nel formato attuale
(notebook autosufficiente) lo stesso giorno del cambio di formato
(`3fa5799`, 2026-07-12). Ogni lezione successiva **replica la struttura di
questa** (teoria, esempio guidato, esercizio con soluzione subito sotto,
quiz, passo di progetto). Se il problema che l'ha fatta fallire la prima
volta non e' davvero risolto, e' un difetto che si e' propagato per
sessanta lezioni, non un difetto isolato.

**Cosa giudicare in particolare.** Il problema originale era "clarity and
learner focus", non tecnico: leggendo, capisci *perche'* un dato manca prima
di vedere *come* si ripara (Parte 1 lo mette in questo ordine apposta)? La
sezione finale scrive nel progetto (`datasets/processed/memory_events_clean.csv`)
in modo che il collegamento fra l'esercizio e il "Memory AI Lab" sia
visibile, non solo dichiarato — funziona quel collegamento per te?

### 2. Lezione 22 — `memory-schema` (`notebooks/lezione-22-schema-memoria.ipynb`)

**Perche' questa.** E' il punto in cui il corso smette di essere
"data engineering generico" e diventa esplicitamente il corso che promette
di essere: apre la Fase 4 (rappresentare le memorie) e introduce il
`@dataclass MemoryRecord` che ogni lezione successiva, fino al capstone,
riusa come contratto. E' anche la prima lezione che dichiara esplicitamente
un prerequisito a distanza (Lezione 1) invece di ripartire da zero — il
punto in cui la promessa "un progetto che cresce lezione dopo lezione"
smette di essere solo un file CSV condiviso e diventa un'architettura dati.
Se il salto non e' chiaro qui, il resto della Fase 4-9 eredita la
confusione.

**Cosa giudicare in particolare.** Il collegamento esplicito a Lezione 1
("campi critici vs recuperabili era gia' uno schema implicito, oggi lo
rendiamo esplicito") ti fa effettivamente ricordare quella lezione, o
presuppone che tu l'abbia gia' interiorizzata? La scelta di `validate()` che
ritorna una lista di problemi invece di sollevare un'eccezione (motivata nel
notebook) ti sembra giustificata o arbitraria?

### 3. Lezione 30 — `attention-intuition` (`notebooks/lezione-30-attention-intuition.ipynb`)

**Perche' questa.** E' l'ultima lezione **gia' pronta** per la review — la
lezione 31 (self-attention matematica) e tutto cio' che segue e' ancora in
`technical_review`. E' quindi la frontiera attuale: il punto fino a cui il
learner puo' arrivare oggi, e la lezione che deve prepararlo al blocco piu'
duro del corso (Transformer, Gemma, LoRA) prima che quel blocco sia a sua
volta pronto per lui. Dichiara un tempo stimato esplicito nel notebook
("Tempo stimato: 25 minuti") — le altre due no: e' anche un test di
quell'aspettativa.

**Cosa giudicare in particolare.** L'attenzione e' presentata come "recupero
morbido" collegata esplicitamente al retrieval per soglia della Lezione 28
(rigido, top-k) — l'analogia regge, o e' un'etichetta appiccicata sopra
matematica scollegata? Dopo questa lezione ti senti pronto per una versione
matematicamente piena di Q/K/V (Lezione 31), o l'intuizione resta un
passaggio isolato?

## Cosa giudicare, in generale

Per ognuna delle tre, il template (`templates/learner-review.md`) struttura
gia' il giudizio — non improvvisare una rubrica diversa:

- **Quiz**: rispondibile leggendo solo il testo della lezione, non a memoria
  o per intuito esterno?
- **Esercizio**: risolvibile senza guardare la soluzione subito sotto, nel
  tempo dichiarato (quando dichiarato)?
- **"Cosa so fare ora che prima non sapevo fare"**: risposta libera
  obbligatoria — se non riesci a scriverla in una frase concreta, e' un
  segnale che la lezione non ha lasciato nulla di operativo.
- **Chiarezza per sezione (1-5)**: le sei sotto-sezioni del template, non un
  voto unico alla lezione.
- **Blocker / ambiguita' / suggerimenti**: testo libero, anche minimo.

## Dove registrare il verdetto

1. Copiare `templates/learner-review.md` in
   `reports/reviews/data-cleaning-01-missing-values-learner-review.md`,
   `reports/reviews/memory-schema-learner-review.md` e
   `reports/reviews/attention-intuition-learner-review.md` (un file per
   lezione, nome esatto = id della lezione in `course/course.yaml` + suffisso
   `-learner-review`).
2. Compilarlo per intero — la decisione **PASS | FAIL** in cima non basta da
   sola, il template la vuole accompagnata da tempo, punteggio quiz e le
   sezioni di chiarezza: sono il segnale che rende il verdetto verificabile
   da chi legge il file dopo, non solo un'etichetta.
3. **PASS**: aggiornare `course/progress.yaml` per quella lezione —
   `state_machine.learner_review: done`, `state_machine.done: done`,
   `status: done`, con una nota datata che rimanda al file di review appena
   creato. Questo e' l'unico punto in cui uno stato passa a `done` per
   decisione umana, non per un gate automatico: chi applica l'update deve
   avere in mano il file PASS compilato, non solo un messaggio a voce.
4. **FAIL**: lasciare `state_machine.learner_review: in_progress`, riportare
   nella nota di progress.yaml quale sezione del template ha causato il FAIL
   (Blocker/Ambiguita'), e instradare la lezione alla fase responsabile
   (`writing` se il problema e' il testo, `lab_build` se e' l'esercizio,
   `technical_review` se e' il codice) — non lasciarla generica in
   `learner_review` senza indicare dove tornare, o la prossima iterazione
   dovra' rifare la diagnosi da capo.
5. `course_status` in cima al file resta invariato finche' non e' stato
   emesso un verdetto (di qualunque segno) su tutte le 30 lezioni in
   `learner_review` — le tre di questo packet sono l'inizio, non la fine,
   del gate.

## Dopo queste tre

- Le altre 27 lezioni in `learner_review` (elenco completo:
  `uv run python -c "import yaml; d=yaml.safe_load(open('course/progress.yaml')); [print(m,l) for m,mod in d['modules'].items() for l,x in (mod.get('lessons') or {}).items() if x.get('status')=='learner_review']"`)
  seguono lo stesso template, una alla volta o a gruppi a discrezione del
  revisore — nessuna di loro ha una ragione specifica per passare avanti
  alle tre di questo packet.
- Le 30 lezioni in `technical_review` (31-60) **non vanno proposte al
  revisore umano finche' non tornano a `learner_review`**: serve prima un
  giro di technical review sul contenuto aggiunto da WI-6 (agente-eseguibile,
  non un item per l'umano). E' lavoro separato da questo packet, non
  incluso qui.
