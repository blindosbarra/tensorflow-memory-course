# Piano WI-6 — lezioni 52-54

## Fetta scelta

Approfondire il segmento formato dalle lezioni 52-54 (architettura del
capstone, dataset del capstone, classificatore del tipo di memoria). Le
lezioni 31-51 sono gia' coperte dalle iterazioni precedenti; le lezioni
55-60 (resto del modulo capstone) restano fuori da questa fetta.

## Fonti scelte (aperte e verificate in questa sessione)

Nota preliminare: un blog personale (martinfowler.com) era stato preso in
considerazione per la lezione 52 e scartato su indicazione del committente
— per le affermazioni tracciate in evidence.yaml si usa solo documentazione
ufficiale di libreria o standard, mai un blog, anche se raggiungibile.

- `github.com/scikit-learn/scikit-learn` (`doc/modules/compose.rst`): la
  motivazione ufficiale di `Pipeline` — comporre piu' stimatori dietro
  un'interfaccia unica (voce "Convenience and encapsulation") e prevenire
  leakage fra train e test (voce "Safety"). Usata due volte con due
  affermazioni distinte: la prima per la lezione 52 (pattern
  stub/orchestratore con firma stabile), la seconda per la lezione 53
  (perche' il controllo di non-leakage nel notebook non e' ridondante).
- `github.com/scikit-learn/scikit-learn` (`doc/modules/model_evaluation.rst`):
  la baseline `DummyClassifier(strategy='most_frequent')`, per la lezione 54
  (la baseline di maggioranza calcolata a mano nel notebook).
- arxiv.org resta bloccato dal proxy in questa sessione. keras.io e
  ai.google.dev non sono stati necessari per questa fetta (lezioni di
  integrazione, non di teoria ML pura).

## Osservazione fuori scope (non corretta qui)

I tre pack (`capstone-architecture`, `capstone-dataset`, `capstone-classifier`)
avevano gia' una claim "main" con una fonte poco pertinente o generica
(rispettivamente: "Attention Is All You Need" per un'affermazione di
architettura software — palesemente scollegata; docs scikit-learn generiche
per dataset/classificatore — piu' pertinenti ma mai verificate live). Non
corretto in questo commit: WI-6 chiede di aggiungere fonti a NUOVE
affermazioni, non di auditare quelle esistenti. Segnalato in coda per un
item dedicato.

## Passi

1. Ampliare la teoria delle tre lezioni senza modificare gli esempi
   eseguibili (celle di codice invariate).
2. Registrare nello stesso commit le nuove affermazioni nei tre research
   pack (`knowledge/capstone-architecture`, `knowledge/capstone-dataset`,
   `knowledge/capstone-classifier`), usando solo le fonti aperte durante
   questa iterazione.
3. Riportare le tre lezioni a `technical_review` in `course/progress.yaml` e
   aggiornare l'handover di WI-6 con il residuo 55-60.
4. Eseguire prima i tre notebook interessati (`--only`), ripristinare gli
   eventuali dataset prodotti dal run parziale con `git checkout --
   datasets/`, quindi eseguire il gate completo 61/61.

## Nota sulla densita' raggiunta

Le lezioni 52-54 partivano piu' leggere (352/267/273 parole di markdown)
delle fette precedenti (tipicamente 350-450). Un solo paragrafo con fonte
primaria le avrebbe lasciate a 447/369/346 parole, sotto il range 430-560
raggiunto dalle fette 40-51. Per lezione 53 e 54 e' stato aggiunto un
secondo paragrafo tecnico (senza fonte esterna nuova: spiega un meccanismo
gia' presente nel codice — il perche' del leakage silenzioso in 53, il
termine di regolarizzazione L2 gia' nel gradiente collegato alla Lezione 12
in 54) per arrivare a 461/422 parole, in linea con lo standard.
