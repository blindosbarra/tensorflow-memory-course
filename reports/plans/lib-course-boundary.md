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
implementazione inline produca oggi un risultato diverso da `src/`. L'unico
problema reale trovato e' un pezzo di `src/` orfano (nessun notebook lo usa),
non una lezione da correggere.

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
| 01 dati-mancanti | `data_cleaning.py` | teach-inline | **conforme** | vedi "caso orfano" sotto: il modulo esiste ma non e' piu' importato da nessuno dal 2026-07-12 |
| 02 duplicati-tipi-outlier | `data_quality.py` | teach-inline | **conforme** | idem |
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

## Il problema reale trovato: moduli orfani

`src/memory_ai/data_cleaning.py` e `data_quality.py` esistono, hanno test
dedicati (`tests/test_data_cleaning.py`, `tests/test_data_quality.py`) e
passano `mypy`/`ruff`/`pytest` — ma **nessun notebook li importa**, ne' la
lezione 01/02 (che correttamente insegna inline, per la decisione 1 sopra) ne'
il capstone (`pipeline.py` dichiara nel proprio docstring che
`MemoryAILab.process` non ne ha bisogno).

Origine: `data_cleaning.py` (2026-07-10) e `data_quality.py` (2026-07-11) sono
stati scritti **prima** di `3fa5799` (2026-07-12), quando le lezioni 01/02
importavano ancora da `memory_ai`. Il commit che ha reso i notebook
autosufficienti ha aggiornato i notebook ma non ha rimosso i moduli
`src/` ne' i loro test: sono un residuo del modello a libreria condivisa che
il corso ha deliberatamente lasciato.

Controllo di merito: la logica inline della lezione 01 (colonne critiche
`memory_id`/`text`/`timestamp`, `type` imputato con la costante `"unknown"`,
`importance` imputata con la mediana) coincide oggi con quella di
`clean_memory_records` — non e' rotta, e' semplicemente non collegata. Ma
niente lo garantisce per il futuro: i test del modulo verificano il modulo
contro se stesso (valori attesi scritti a mano), non contro il notebook, quindi
una futura modifica alla lezione 01/02 potrebbe divergere da `data_cleaning.py`/
`data_quality.py` senza che nessun gate se ne accorga.

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

Non ci sono lezioni da correggere (vedi sopra: zero derive trovate). Le
azioni rimaste sono sul confine stesso, non sul contenuto delle lezioni:

1. **Ritirare `src/memory_ai/data_cleaning.py`, `data_quality.py` e i loro
   test** — codice morto rispetto a qualunque notebook, residuo di un modello
   di corso che non esiste piu' dal 2026-07-12. Alternativa scartata:
   ricollegarli alla lezione 01/02 riaprirebbe il modello a starter-file che
   l'allievo ha chiesto di rimuovere — non farlo senza una nuova decisione
   esplicita dell'autore del corso.
2. *(Facoltativo, non bloccante)* valutare se aggiungere un controllo di
   parita' automatizzato fra le otto lezioni "origine" e i moduli
   corrispondenti di `src/`, cosi' che un futuro edit di codice a una di
   quelle lezioni fallisca un gate invece di dipendere da un messaggio di
   commit onesto. Da proporre come nuovo item, non da costruire qui.

Con l'item 1 completato, la Priorita' A di questo loop e' esaurita: il
confine libreria/corso e' documentato, verificato lezione per lezione, e
l'unico scostamento reale e' stato messo in coda.
