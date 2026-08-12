# Piano — confine libreria/corso (`src/memory_ai/` vs notebook)

## Perche' questo piano

`src/memory_ai/` e' importato da 4 dei 61 notebook (`lezione-57` a `lezione-60`).
Gli altri 57 notebook non lo importano affatto — inclusi otto notebook (01, 02,
18, 25, 52, 54, 55, 56) la cui logica il pacchetto rispecchia parzialmente o
del tutto. Prima di trattare questo come deriva da correggere lezione per
lezione, questa iterazione ricostruisce **perche'** il confine e' fatto cosi',
verifica se le implementazioni inline sono davvero divergenti da `src/`, e
elenca cosa resta da fare.

Conclusione anticipata: il confine attuale e' quasi interamente **voluto**, non
accidentale, ed e' il prodotto di due decisioni esplicite e opposte prese in
momenti diversi (sotto). Non e' stata trovata nessuna lezione la cui
implementazione inline produca oggi un risultato diverso da `src/`. Il problema
reale trovato non e' un modulo orfano da eliminare (prima stesura di questo
piano, corretta in questa stessa iterazione dopo aver eseguito il codice
invece di leggerlo soltanto — vedi sotto): e' che il percorso di verifica
documentato per quel modulo non e' collegato a nessun gate automatico.

## La regola (una volta sola)

> Un notebook insegna un concetto **inline**, con la propria implementazione
> scritta da zero in cella (nomi di funzione in italiano, stile della lezione),
> quando il suo compito e' insegnare quel concetto per la prima volta. Importa
> da `src/memory_ai/` solo quando il suo compito e' **assemblare** componenti
> gia' insegnate altrove in un sistema funzionante — oggi, le sole quattro
> lezioni di chiusura del capstone (57-60) che costruiscono ed eseguono
> `MemoryAILab`.
>
> Se `src/memory_ai/` non copre affatto il dominio di una lezione, la domanda
> "inline o import" non si pone: resta inline per definizione (default per 53
> delle 61 lezioni — vedi tabella).

Questa regola non e' una scelta nuova di questo piano: e' il pattern che il
repository ha gia' costruito due volte, in direzioni opposte, con una
motivazione esplicita ogni volta:

1. **2026-07-12, commit `3fa5799`** ("lessons become self-contained
   notebooks with one growing project"). Prima di questo commit, le lezioni
   01 e 02 importavano da `memory_ai.data_cleaning` / `memory_ai.data_quality`
   in un modello a starter-file + pytest dedicati. Il messaggio di commit e'
   esplicito: *"Format change requested by the learner"* — il modello a
   libreria condivisa e' stato rimosso su richiesta diretta di chi segue il
   corso, a favore di notebook autosufficienti. `reports/handover/AGENT_LOOP.md`
   istruisce gli agenti futuri a non resuscitare quello scaffolding
   (`templates/lesson.md` e' dichiarato superato per questo).
2. **2026-08-09/11, WI-13** ("Estrarre i componenti del capstone in
   `src/memory_ai/` con test"). Le lezioni 58 e 60 dovevano assemblare i
   componenti delle lezioni 54-56 in una pipeline `MemoryAILab` reale e
   testata — riscrivere quella logica a mano in ogni cella non avrebbe
   insegnato nulla di nuovo e avrebbe reso impossibile testarla. Le note
   dell'item sono esplicite: *"i notebook 54-56 continuano a insegnare la
   costruzione da zero"* — l'estrazione era per la pipeline, non per
   sostituire le lezioni che insegnano i pezzi.

Le due decisioni non si contraddicono: riguardano fasi diverse del corso
(prima esposizione a un concetto vs. assemblaggio finale di concetti gia'
visti) e sono state prese entrambe dall'autore/allievo del corso, non
inferite da un agente. Questo piano le rende esplicite come regola unica
invece di lasciarle solo nella storia dei commit.

## Tabella per lezione

Solo le lezioni il cui dominio e' effettivamente coperto da un modulo di
`src/memory_ai/` sono elencate; le altre 49 non hanno un modulo corrispondente
e la regola non si applica (vedi nota sotto la tabella).

| Lezione | Modulo `src/` corrispondente | Decisione | Stato attuale | Nota |
|---|---|---|---|---|
| 01 dati-mancanti | `data_cleaning.py` (via `examples/data_cleaning_missing_values.py`) | teach-inline | **conforme** | il notebook insegna inline; `src/`+`examples/` e' l'implementazione di riferimento separata, per scelta documentata in README — vedi sotto |
| 02 duplicati-tipi-outlier | `data_quality.py` (via `examples/duplicates_types_outliers.py`) | teach-inline | **conforme** | idem |
| 18 cosine-similarity | `embedding.py` (proprieta' matematica, non la funzione) | teach-inline | **conforme** | lezione 18 stabilisce la proprieta' "vettori unitari -> coseno = prodotto scalare" che `embedding.py` usa; non e' la stessa implementazione, e' il prerequisito matematico |
| 25 importance-scoring | `importance.py` | teach-inline | **conforme** | |
| 52 capstone-architettura | `schema.py` (`MemoryRecord`) | teach-inline | **conforme** | definisce lo stub che 54-58 riempiono |
| 54 capstone-classificatore | `classifier.py` | teach-inline | **conforme** | estratto 2026-08-11 **dopo** l'approfondimento della lezione (2026-08-10): riflette lo stato corrente |
| 55 capstone-embedding-grafo | `embedding.py`, `text.py` (entita') | teach-inline | **conforme** | vedi "controllo ordine estrazione" sotto |
| 56 capstone-gemma-lora | `text.py` (relazioni) | teach-inline | **conforme** | idem |
| 57 capstone-valutazione | (usa i prodotti della pipeline) | import-from-src | **conforme** | importa `memory_ai` |
| 58 capstone-pipeline | `pipeline.py` (`MemoryAILab`) | import-from-src | **conforme** | importa `memory_ai` |
| 59 capstone-monitoring | (usa `MemoryAILab`) | import-from-src | **conforme** | importa `memory_ai` |
| 60 capstone-demo | (usa `MemoryAILab`) | import-from-src | **conforme** | importa `memory_ai` |

Le lezioni 26-29 (entita'/relazioni, grafo, retrieval ibrido, contraddizioni)
**non** sono nella tabella nonostante nomi simili a `text.py`/`embedding.py`:
insegnano le stesse idee con librerie vere (NetworkX, un embedding Keras
addestrato) mentre il capstone usa versioni volutamente semplificate
(hashing invece di embedding addestrato, dizionario scritto a mano invece di
NetworkX) proprio per restare senza dipendenze pesanti — `pipeline.py` lo
dichiara esplicitamente nel proprio docstring. Non e' un caso di mancato
riuso: sono due implementazioni diverse per scopi diversi, non una
duplicazione della stessa logica.

Le restanti 49 lezioni (numpy/tensori/gradienti, attention, transformer,
LoRA/QLoRA, DPO/RLHF, i moduli PMLE, il notebook consolidato 01-15, ecc.) non
condividono dominio con nessun modulo di `src/memory_ai/`: la domanda
"inline o import" non si applica, restano inline per definizione.

## Casi di deriva cercati e non trovati

Il compito assegnato presumeva casi di "codice inline che e' effettivamente
divergente da `src/`". Sono stati controllati i punti a rischio piu' concreto
(estrazione avvenuta *prima* di una modifica successiva alla lezione
d'origine, quindi potenzialmente non piu' in parita'):

- **`schema.py`/`classifier.py` vs lezioni 52/54**: la lezione e' stata
  approfondita il 2026-08-10 (`2cf3d76`, teoria e fonti, messaggio di commit
  conferma *"Nessuna cella di codice toccata"*); `classifier.py` e' stato
  estratto il 2026-08-11 (`25123ff`), **dopo** quella modifica. Nessuna
  divergenza possibile.
- **`text.py`/`embedding.py` vs lezioni 55/56**: qui l'ordine e' invertito —
  `text.py`/`embedding.py` sono stati estratti il 2026-08-09 (`b873324`), e le
  lezioni 55/56 sono state approfondite **dopo**, il 2026-08-11 (`50bdaa3`).
  Controllato il diff di quel commit: tocca solo `course/progress.yaml`,
  `knowledge/*/evidence.yaml` e le celle markdown di teoria dei tre notebook
  55-57; il messaggio di commit lo dichiara esplicitamente
  (*"Nessuna cella di codice toccata"*) e il diff lo conferma. Nessuna
  divergenza risultante, ma l'ordine resta un precedente pericoloso (vedi
  sotto).

Non e' stata trovata nessuna lezione dove l'implementazione inline produce
oggi un output diverso da `src/`. La coda "correggere una lezione per
iterazione, a partire dai casi di deriva reale" e' quindi **vuota**: non c'e'
nessuna lezione da correggere per questo motivo.

## Il problema reale trovato: `examples/` non e' collegato a nessun gate

**Correzione rispetto alla prima stesura di questo piano (stessa iterazione,
prima del commit).** La prima stesura chiamava `data_cleaning.py` e
`data_quality.py` "moduli orfani" da ritirare, basandosi solo su una `grep`
che non li trovava importati da nessun notebook. Prima di agire su quella
conclusione ho letto `README.md` (riga 118): *"I moduli `examples/` e
`src/memory_ai/` sono implementazione di riferimento della pipeline, non
materiale di studio."* Quella riga e' stata scritta nel commit `b24eb16`,
**lo stesso giorno e poche ore dopo** `3fa5799` (quello che ha reso i notebook
autosufficienti) — non e' un residuo dimenticato, e' la decisione presa
subito dopo per spiegare perche' `src/memory_ai/` e `examples/` restano nel
repository nonostante i notebook non li importino piu'. `examples/data_cleaning_missing_values.py`
e `examples/duplicates_types_outliers.py` chiamano esattamente
`data_cleaning.py`/`data_quality.py`: il collegamento esiste, e' solo fuori
dai notebook.

Eseguito `uv run python examples/data_cleaning_missing_values.py` per
verificare che sia ancora vivo (non solo documentato): gira, e riscrive
`datasets/processed/memory_events_clean.csv`. **Trappola**: quel file e'
condiviso con le lezioni 01-05 (il "progetto che cresce"), quindi eseguire
lo script lo ha sporcato con un contenuto diverso da quello atteso dalle
lezioni successive — ripristinato subito con `git checkout --` prima di
qualunque commit, come richiede la sezione "Verifica" di `AGENT_LOOP.md` per
i run parziali. Il contenuto che lo script produce (4 righe, da
`memory_events_raw.csv` isolato) e quello committato in `memory_events_clean.csv`
(6 righe) non coincidono a prima vista, ma non e' deriva: il file committato
e' il prodotto della catena lezione 01 -> 02 (-> 05), lo script riproduce
solo il primo anello in isolamento. Confrontato l'anello giusto — sullo
stesso `memory_events_raw.csv`, `clean_memory_records` scarta `mem_004` e
`mem_005` (campo critico mancante: `text` e `timestamp` rispettivamente nel
CSV grezzo) esattamente come la cella inline della lezione 01, che usa lo
stesso criterio (`CRITICI_MEMORIA`, imputazione `type` a costante
`"unknown"`, `importance` a mediana). Nessuna divergenza di comportamento
trovata.

Il problema reale non e' quindi "codice morto da eliminare": e' che questo
percorso — `examples/*.py` che invoca `src/memory_ai/data_cleaning.py` /
`data_quality.py` come implementazione di riferimento delle lezioni 01/02 —
non e' eseguito da **nessun test, nessun CI, nessuno script di verifica**
(controllato: nessuna occorrenza di `examples/` in `tests/`, `.github/` o
`scripts/`). `reports/evaluation/*.json`, l'output dichiarato di questi
script, non e' stato rigenerato dal 2026-07-11 — da prima del cambio di
formato dei notebook. E' un ramo del repository che il README promette
funzionante e che *e'* ancora funzionante, ma solo perche' nessuno lo ha
ancora rotto, non perche' qualcosa lo impedirebbe.

## Nessun controllo di parita' e' automatizzato

La "verifica per PARITA'" citata nelle note di WI-13 (222 testi confrontati,
zero differenze) e' stata un controllo manuale, una tantum, fatto al momento
dell'estrazione — non e' un test che gira di nuovo. `tests/test_*.py` testano
`src/memory_ai/` contro valori attesi scritti a mano, non contro l'output
delle celle dei notebook 01, 02, 18, 25, 52, 54, 55, 56. Le due verifiche
sopra ("nessuna cella di codice toccata") si sono appoggiate al messaggio di
commit, non a un gate eseguibile. Non e' nello scope di questa iterazione
costruirne uno (sarebbe un nuovo work item, non "correggere una lezione"):
lo segnalo qui perche' un'iterazione futura possa deciderne la necessita'.

## Coda di lavoro per le iterazioni successive

Non ci sono lezioni da correggere (vedi sopra: zero derive trovate) e non ci
sono moduli da ritirare (vedi sopra: `data_cleaning.py`/`data_quality.py` sono
la implementazione di riferimento documentata, non codice morto). Le azioni
rimaste sono sulla verificabilita' del confine, non sul suo contenuto:

1. Aggiungere `examples/data_cleaning_missing_values.py` e
   `examples/duplicates_types_outliers.py` a un gate eseguibile (`pytest` con
   `subprocess`, o una riga in `scripts/`), cosi' che "implementazione di
   riferimento" smetta di dipendere dal fatto che nessuno l'ha ancora rotta.
   Lo script deve girare su un file temporaneo, non su
   `datasets/processed/memory_events_clean.csv` (condiviso con le lezioni
   01-05) — la trappola incontrata in questa iterazione va evitata dal gate
   stesso, non solo documentata.
2. *(Facoltativo, non bloccante)* valutare se aggiungere un controllo di
   parita' automatizzato fra le otto lezioni "origine" e i moduli
   corrispondenti di `src/`, cosi' che un futuro edit di codice a una di
   quelle lezioni fallisca un gate invece di dipendere da un messaggio di
   commit onesto. Da proporre come nuovo item, non da costruire qui.

Nessuno dei due item e' un "fix a una lezione" nel senso in cui la Priorita' A
del loop lo intendeva — sono manutenzione del confine, non correzioni di
contenuto. Con la scoperta che non esiste nessuna lezione da correggere e
nessun modulo da ritirare, la Priorita' A e' de facto chiusa: il confine
libreria/corso e' documentato, verificato lezione per lezione (eseguendo il
codice, non solo leggendolo), e gli unici due item rimasti sono manutenzione
opzionale della verificabilita', non debito accumulato.
