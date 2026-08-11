# Piano WI-6 — lezioni 55-60 (fetta completa)

## Fetta coperta

L'intera fetta richiesta per questa iterazione, lezioni 55-60 — chiusura del
modulo capstone: embedding/retrieval/grafo (55), estrazione strutturata con
Gemma+LoRA (56), valutazione offline (57), pipeline `MemoryAILab` (58),
monitoraggio/drift (59), demo finale (60). Le lezioni 31-54 sono gia' coperte
dalle iterazioni precedenti. Con questa fetta **WI-6 copre l'intero range
31-60** dichiarato dal titolo dell'item.

Il lavoro e' stato fatto in due passate nella stessa iterazione (55-57, poi
58-60) per tenere il diff di ciascuna passata verificabile con lo stesso gate
rapido `--only` prima del gate completo; il commit finale e' unico, come
richiesto, e include entrambe le passate.

## Fonti scelte (aperte e verificate in questa sessione, accessed_at 2026-08-11)

Lezioni 55-57:
- `scikit-learn.org/stable/modules/metrics.html` (cosine similarity):
  lezione 55, perche' `E @ q` su vettori normalizzati e' esattamente il
  coseno, non un'approssimazione.
- `networkx.org/documentation/stable/reference/introduction.html`:
  lezione 55, la rappresentazione interna di NetworkX (dizionario di
  dizionari) replicata a mano dal grafo del notebook.
- `keras.io/keras_hub/api/models/gemma/gemma_backbone/`: lezione 56, la
  firma ufficiale di `GemmaBackbone.enable_lora(rank, target_layer_names)`.
- `scikit-learn.org/stable/modules/model_evaluation.html` (F-measures):
  lezione 57, la definizione ufficiale dell'F1 come media armonica.

Lezioni 58-60:
- `scikit-learn.org/stable/modules/classification_threshold.html`: lezione
  58, la distinzione ufficiale fra stima di probabilita' e decisione a
  soglia, per `should_store = imp >= self.soglia`.
- `arxiv.org/abs/2307.11878` ("The Population Resemblance Statistic: A
  Chi-Square Measure of Fit for Banking"): lezione 59, la formula PSI e le
  soglie 0.10/0.25 ("costanti di Lewis") gia' usate dal notebook. Nota:
  arxiv.org, bloccato dal proxy in tutte le sessioni precedenti di WI-6
  (documentato dalle fette 43-45 in poi), era raggiungibile in questa
  sessione — verificato con una richiesta di controllo prima di usarlo.
- `rfc-editor.org/rfc/rfc7231` (§4.2.2, Idempotent Methods): lezione 60, la
  definizione standard di idempotenza applicata al controllo di
  deduplicazione per `memory_id` in `MemoryAILab.process`.

Un blog personale non e' stato preso in considerazione per nessuna delle sei
lezioni: tutte le fonti sono documentazione ufficiale di libreria/framework
(scikit-learn, NetworkX, KerasHub) o standard/paper (RFC 7231, arXiv), come
richiesto dal committente.

## Passi eseguiti

1. Ampliata la teoria delle sei lezioni senza modificare gli esempi
   eseguibili (celle di codice invariate) — solo le celle markdown di teoria
   ("## Teoria essenziale" per 55-59; "## Il lab al lavoro" per la 60, unica
   cella di teoria che la lezione 60 possiede: non ha una sezione "##
   Teoria essenziale" perche' e' la demo finale, non un'introduzione di
   concetti nuovi).
2. Registrate nello stesso commit sei nuove affermazioni nei sei research
   pack (`knowledge/capstone-*`), usando solo le fonti aperte durante
   questa iterazione.
3. Riportate tutte e sei le lezioni a `technical_review` in
   `course/progress.yaml`.
4. Eseguiti due gate rapidi `--only` (uno per le lezioni 55-57, uno per le
   lezioni 58-60: nessuno dei due ha sporcato `datasets/processed/`, queste
   sei lezioni non scrivono file condivisi) e un gate completo 61/61 finale
   in background.

## Trappola incontrata e corretta

La prima versione dello script di edit (per le lezioni 55-57) aggiungeva un
paragrafo la cui ultima riga non terminava con `\n`, poi appendeva una riga
vuota "\n" come separatore: risultato, un solo a-capo invece di una vera
riga vuota fra paragrafi in markdown (serve `\n\n`). Corretto imponendo, con
un `assert`, che ogni paragrafo passato alla funzione di append termini gia'
con `\n`; verificato contro il diff prima di procedere, e riusato lo stesso
script corretto per le lezioni 58-60.

## Nota sulla densita' raggiunta

Le sei lezioni partivano molto piu' leggere delle fette precedenti (60/62/
54/42/93/33 parole). Con due paragrafi a fonte primaria per lezione si
arriva a 293/224/225/221/306/215 parole — in linea con lo standard gia'
raggiunto dalle lezioni capstone 52-54 (186/197/242 parole), che restano
piu' leggere delle lezioni di teoria pura (31-51, tipicamente 350-560)
perche' sono lezioni di integrazione, non di introduzione di un concetto
nuovo.

## Osservazione fuori scope (non corretta qui)

Le claim "main" preesistenti in `capstone-pipeline` (cita LoRA per
un'affermazione di orchestrazione software) e in `capstone-demo` (cita DPO
per l'esecuzione end-to-end) usano fonti non pertinenti al claim, come gia'
osservato per `capstone-architecture/dataset/classifier` nella fetta 52-54.
Non corretto qui: WI-6 aggiunge fonti a nuove affermazioni, non audita
quelle esistenti — coerente con l'item WI-15 gia' aperto in coda per questo.

## Stato finale di WI-6

Con questa fetta, tutte le lezioni 31-60 nominate dal titolo dell'item sono
state approfondite con fonti primarie verificate. Il campo `files` di WI-6
in `reports/handover/queue.yaml` copre gia' l'intero range (pattern glob
`lezione-3*`, `lezione-4*`, `lezione-5*`, piu' la lezione 60 esplicita); non
risultano altre lezioni nel range 31-60 con teoria non approfondita da
questa serie di iterazioni. L'item puo' essere chiuso `done` dopo l'ultima
verifica del gate completo di questo commit.
