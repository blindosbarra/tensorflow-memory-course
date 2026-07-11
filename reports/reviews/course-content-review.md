# Review: contenuto del corso (syllabus + lezioni 1-2 + metodo)

Data: 2026-07-11
Tipo: learner/content review avversariale
Ambito: `docs/syllabus.md`, `course/course.yaml`, lezioni
`data-cleaning-01-missing-values` e `duplicates-types-outliers` (pagina,
esercizio, soluzione, notebook, knowledge pack), template lezione, processo di
learner review.

## Decisione

**FAIL didattico.** PASS tecnico confermato (test, lint, notebook e build
passano), ma i gate B e D — così come sono stati applicati finora — non hanno
misurato ciò che conta: lo studente non impara a fare nulla che non sapesse già
fare, perché non gli viene mai chiesto di fare nulla.

Il feedback dello studente è esplicito: il corso oggi è "una spiegazione di
poche righe di codice", il syllabus non regge e il contenuto è superficiale e
senza teoria. Questa review conferma il feedback punto per punto.

## Blocker

### B1. Lo studente non scrive mai codice

Tutta la logica è già implementata in `src/memory_ai/`. L'esercizio della
lezione 2 dice testualmente "Usa la funzione gia' pronta": lo studente importa
`duplicate_memory_mask` e `clean_memory_quality_issues`, le chiama, e legge
l'output. La "soluzione" in `solutions/duplicates-types-outliers.md` è
identica all'esempio guidato della lezione (stesse ~6 righe). Il notebook è
una copia dell'esempio: 5 celle che chiamano le stesse funzioni.

`uv run pytest` è presentato come "controllo automatico" dell'esercizio, ma i
test verificano il codice del repository, non il lavoro dello studente: passano
anche se lo studente non ha aperto nessun file.

Questo viola una regola scritta nel syllabus stesso ("Se una lezione sembra
solo teoria o solo comandi, va migliorata"): queste lezioni sono solo comandi.

### B2. La teoria è assente

La sezione "Teoria essenziale" della lezione 1 sono due paragrafi che
descrivono API (`isna()`, `SimpleImputer`). Nella lezione 2 la sezione non
esiste nemmeno. Mancano, restando dentro lo scope microlearning:

- **Missing values**: i meccanismi di missingness (MCAR/MAR/MNAR) anche solo
  come intuizione — sono esattamente ciò che decide "scarto o imputo", cioè la
  decisione che la lezione dichiara di insegnare; perché mediana e non media
  (robustezza agli outlier); cosa fa l'imputazione alla distribuzione
  (riduce la varianza, concentra massa sulla mediana) e perché il flag
  `*_was_missing` mitiga il problema.
- **Outlier**: la lezione usa solo la regola di dominio (range 0-1). Va bene
  come scelta, ma non nomina mai l'alternativa statistica (IQR, z-score) — lo
  studente esce senza sapere che esiste, né perché qui non serve. Inoltre il
  clipping non è discusso: accumula massa sui bordi 0.0 e 1.0, e "correggere"
  un valore impossibile invece di scartarlo è una scelta con conseguenze, non
  un dettaglio.
- **Duplicati**: nessun accenno ai near-duplicates (stesso evento scritto in
  modo diverso), che per un sistema di memoria testuale è il caso reale.

Il quiz aggrava il problema: chiede cose mai spiegate. Q1 lezione 1 ("perché
`isna()` e non `== pd.NA`") non è rispondibile con il testo, che dice solo
"si usa `isna()`" senza spiegare la semantica di propagazione di NaN/NA. Q2
lezione 1 richiede il concetto di test set, che viene insegnato due lezioni
dopo. Le altre domande si rispondono copiando il riepilogo: Gate D ("quiz non
puramente mnemonico") non è di fatto superato.

### B3. Il syllabus è incoerente con course.yaml e con la spec

- `course/course.yaml` definisce il modulo `foundations`
  (python-numpy-refresh, vettori/tensori, derivate/gradienti,
  probabilità/loss) come primo modulo, e la spec (§3.4) dichiara la
  progressione obbligatoria a partire da "Python/NumPy essenziale". Il
  syllabus lo **salta**: Fase 1 parte dai missing values e "Dove siamo ora"
  indica come prossima lezione `train-validation-test`. O foundations rientra
  nel percorso, o va rimosso da course.yaml e la spec va aggiornata: oggi i
  tre documenti raccontano tre corsi diversi.
- Le 8 fasi del syllabus non mappano i 10 moduli di course.yaml (fasi e moduli
  hanno nomi, confini e contenuti diversi); il lettore non può capire a che
  punto del yaml corrisponde una fase.
- course.yaml pianifica ~70 lezioni. A 15-30 minuti l'una sono 20-35 ore di
  corso con un processo che produce una lezione per ciclo di review: non c'è
  né una priorità ("percorso minimo") né una stima totale, né criteri di
  taglio. Il syllabus non dichiara alcun assessment di fine fase: il
  "Risultato della fase" è una frase, non qualcosa che lo studente possa
  verificare di saper fare.
- Nessuna fase ha obiettivi misurabili per lezione (il yaml ha solo id).

## Major

### M1. Il corso si chiama "TensorFlow" ma TensorFlow non compare

Dopo due lezioni non c'è un tensore, un array NumPy, né una riga di TF. La
sezione "Dentro TensorFlow/Keras" della lezione 1 esiste solo per dire che
TensorFlow non c'è; nella lezione 2 la sezione è stata silenziosamente
rimossa (il template non è rispettato). L'aspettativa creata dal titolo è
disattesa e il syllabus non la gestisce: serve o una lezione-ponte subito
(NumPy → tensori) o una dichiarazione esplicita in apertura di syllabus del
perché TF arriva in Fase 2.

### M2. Il dataset dà le risposte prima delle domande

`memory_events_quality_issues.csv` ha 7 righe e la lezione elenca in anticipo
i 3 problemi contenuti ("duplicati; importance non numerica; importance fuori
range"), mostrando pure la tabella incriminata nel primo paragrafo. Non c'è
alcun momento diagnostico: lo studente non trova i problemi, li riconosce
dopo che gli sono stati indicati. Serve un secondo dataset più grande
(≥100 righe, generato con seed) e non commentato, su cui l'esercizio chieda di
scoprire e quantificare i problemi.

### M3. Il quiz non ha risposte e i criteri di successo non sono verificabili

Le soluzioni coprono solo l'esercizio (e sono la copia dell'esempio). Le
domande del quiz non hanno risposta da nessuna parte nel repo: lo studente non
può autovalutarsi. I "criteri di successo" della lezione 2 sono "riesci a
spiegare X" senza rubrica né risposta di riferimento.

### M4. La learner review non ha un processo

La spec (§19) mette la review umana come gate obbligatorio, ma non esiste un
template di learner review (esiste solo `templates/review.md`, tecnico), né
metriche: tempo effettivo sulla lezione, punteggio quiz, "cosa sai fare ora
che prima non sapevi fare". Il feedback negativo del 2026-07-10 ("failed the
slice for clarity and learner focus") è registrato solo come nota in
progress.yaml e la lezione 2 ha replicato la stessa struttura che aveva
fallito: il segnale è stato archiviato, non incorporato nel metodo.

### M5. L'esercizio non è progressivo

Non esiste il passaggio "scrivi tu la funzione, poi confronta con la
soluzione". Il formato corretto per questo repo è: file starter in
`exercises/` con firma e TODO (es. `find_duplicates(frame, keys)`), test
dedicati in `tests/exercises/` che girano sul file dello studente, hint
progressivi che portano alla soluzione, soluzione separata che è più della
copia dell'esempio guidato.

## Minor

- `SimpleImputer` per un fill costante e una mediana è una dipendenza pesante
  e produce il codice più contorto del repo
  (`astype("object").where(notna, np.nan)` in `data_cleaning.py:69-70`):
  `fillna` di pandas sarebbe più leggibile per il pubblico dichiarato. Se
  l'obiettivo è introdurre l'API sklearn in vista del fit/transform sul solo
  train set, va detto esplicitamente, altrimenti è complessità gratuita.
- La stima di 25 minuti non è realistica: la parte attiva (2 comandi e la
  lettura di un report JSON) dura meno di 10 minuti. O si aggiunge lavoro vero
  (vedi M5) o si dichiara 10-15.
- Le fonti della lezione 2 sono tre pagine di reference API pandas: nessuna
  fonte concettuale su duplicati/outlier. Gate A ("almeno 2 fonti primarie
  quando il tema lo consente") è rispettato solo formalmente.
- I knowledge pack (`knowledge/*/concepts.md`) ripetono la lezione in forma
  abbreviata invece di contenere la ricerca che la lezione dovrebbe
  distillare: il flusso researcher → writer previsto dalla spec è di fatto
  invertito.

## Verifiche eseguite

- [x] Fonti
- [x] Teoria
- [ ] Matematica (non applicabile: nelle lezioni non c'è matematica)
- [x] API
- [x] Codice
- [x] Notebook
- [x] Test
- [x] Didattica
- [x] Link
- [x] Build sito (non rieseguita in questa review; verificata il 2026-07-11
  nella review tecnica)

## Comandi

```bash
uv run pytest
# 8 passed

uv run ruff check .
# All checks passed!

uv run python scripts/execute_notebooks.py
# Executing notebooks/data-cleaning-01-missing-values.ipynb
# Executing notebooks/duplicates-types-outliers.ipynb
```

## Azioni raccomandate (in ordine)

1. **Riscrivere il template di lezione** prima di produrre altro contenuto:
   sezione di teoria reale (concetti e trade-off, non solo API; le API vanno
   in "Esempio guidato"), esercizio a completamento con test sul codice dello
   studente, quiz con risposte commentate in `solutions/`.
2. **Riscrivere il syllabus** allineandolo a `course/course.yaml`: reintegrare
   o eliminare `foundations` (decisione da prendere, non da lasciare
   implicita), mappare fasi ↔ moduli 1:1, dichiarare per ogni fase un
   assessment concreto di uscita e una stima di ore totali, definire un
   percorso minimo prioritario dentro le ~70 lezioni.
3. **Rifare gli esercizi delle due lezioni esistenti** nel formato starter +
   test dedicati (M5), con il dataset diagnostico non commentato (M2).
4. **Creare `templates/learner-review.md`** con metriche minime (tempo,
   punteggio quiz, output prodotto autonomamente) e usarlo come gate: senza
   questo, il gate "learner_review" resta una casella da spuntare.
5. Solo dopo 1-4, riprendere la produzione con `train-validation-test` (o con
   la prima lezione foundations, in base alla decisione al punto 2).

## Decisione su progress.yaml

- `duplicates-types-outliers`: learner_review **failed** → torna in
  `writing`.
- `data-cleaning-01-missing-values`: resta `done` formalmente, ma questa
  review la segnala per rework con gli stessi rilievi (B1, B2, M3, M5); va
  riaperta quando il template sarà aggiornato.
- La produzione di nuove lezioni è bloccata finché template ed esercizi non
  sono ristrutturati.
