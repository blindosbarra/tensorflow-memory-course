# Piano WI-6 — lezioni 55-57

## Fetta scelta

Approfondire il segmento formato dalle lezioni 55-57 (embedding/retrieval/
grafo, estrazione strutturata con Gemma+LoRA, valutazione offline del lab).
Le lezioni 31-54 sono gia' coperte dalle iterazioni precedenti; le lezioni
58-60 (pipeline, monitoring, demo — chiusura del modulo capstone) restano
fuori da questa fetta, per lo stesso motivo delle fette precedenti: tre
lezioni per commit e' lo standard di densita' gia' seguito da WI-6 dalla
fetta 34-36 in poi, e la lezione 60 non ha nemmeno una sezione
"## Teoria essenziale" (ha "## Il lab al lavoro": e' la demo finale, non una
lezione di teoria — va valutata a parte nella prossima iterazione, non
forzata nello stesso pattern).

## Fonti scelte (aperte e verificate in questa sessione, accessed_at 2026-08-11)

- `scikit-learn.org/stable/modules/metrics.html` (Pairwise metrics — cosine
  similarity): la definizione formale della similarita' coseno come prodotto
  scalare L2-normalizzato, per la lezione 55 (perche' `E @ q` su vettori gia'
  normalizzati e' esattamente il coseno, non un'approssimazione).
- `networkx.org/documentation/stable/reference/introduction.html`: la
  rappresentazione interna di NetworkX (dizionario di dizionari), per la
  lezione 55 (il grafo del notebook, un dizionario di insiemi scritto a
  mano per evitare la dipendenza opzionale, replica lo stesso principio che
  NetworkX stesso usa e motiva con la velocita' di lookup su grafi sparsi).
- `keras.io/keras_hub/api/models/gemma/gemma_backbone/`: la firma ufficiale
  di `GemmaBackbone.enable_lora(rank, target_layer_names=None)`, per la
  lezione 56 (quali layer vengono adattati, cosa fa `rank=4` nella cella
  guardata).
- `scikit-learn.org/stable/modules/model_evaluation.html` (Precision, recall
  and F-measures): la definizione ufficiale dell'F1 come media armonica
  pesata di precisione e richiamo, per la lezione 57 (la stessa formula
  usata dal notebook per valutare l'estrazione di relazioni).
- arxiv.org resta bloccato dal proxy in questa sessione; non necessario per
  questa fetta (nessuna delle tre lezioni cita direttamente un paper).

## Passi

1. Ampliare la teoria delle tre lezioni senza modificare gli esempi
   eseguibili (celle di codice invariate) — solo la cella markdown
   "## Teoria essenziale".
2. Registrare nello stesso commit le nuove affermazioni nei tre research
   pack (`knowledge/capstone-embedding-graph`, `knowledge/capstone-gemma-lora`,
   `knowledge/capstone-evaluation`), usando solo le fonti aperte durante
   questa iterazione.
3. Riportare le tre lezioni a `technical_review` in `course/progress.yaml`
   (status, state_machine.technical_review -> in_progress,
   state_machine.learner_review -> pending, nota datata) e aggiornare
   l'handover di WI-6 in `reports/handover/queue.yaml` con il residuo 58-60.
4. Eseguire prima i tre notebook interessati (`--only`), verificare che il
   run parziale non abbia sporcato `datasets/processed/` (non l'ha fatto:
   queste tre lezioni non scrivono file condivisi), poi eseguire il gate
   completo 61/61.

## Trappola incontrata e corretta

Il primo tentativo di scrittura ha prodotto un bug di concatenazione: le
funzioni ausiliarie appendevano un nuovo paragrafo, poi un separatore "riga
vuota", ma l'ultima riga del paragrafo appena scritto non terminava con
`\n` — risultato: `"...di TF-IDF."` seguito da `"\n"` produce un singolo
a-capo (`"...di TF-IDF.\nIl grafo..."`), non una riga vuota fra paragrafi
(serve `\n\n`). Corretto imponendo che ogni paragrafo passato alla funzione
di append termini gia' con `\n`, con un `assert` che lo verifica prima di
scrivere. Verificato confrontando il diff con il pattern gia' visto nelle
lezioni 52-54 (dove ogni riga, compresa l'ultima di ogni paragrafo, termina
con `\n`).

## Nota sulla densita' raggiunta

Le lezioni 55-57 partivano molto piu' leggere delle fette precedenti (60/62/
54 parole, contro il range 180-460 raggiunto da 43-54). Con due paragrafi a
fonte primaria per lezione si arriva a 293/224/225 parole — in linea con lo
standard delle lezioni capstone gia' remediate (52: 186, 54: 197), che
restano piu' leggere delle lezioni di teoria pura (31-51, tipicamente
350-560) perche' sono lezioni di integrazione, non di introduzione di un
concetto nuovo.

## Cosa resta (per la prossima iterazione)

Lezioni 58 (pipeline), 59 (monitoring) e 60 (demo). Nota per chi la
riprende: la lezione 60 non ha una cella "## Teoria essenziale" (ha
"## Il lab al lavoro", 33 parole) — verificare con l'autore del corso se va
trattata come le altre (aggiungendo teoria) o lasciata come chiusura leggera
del corso, prima di applicarci lo stesso pattern.
