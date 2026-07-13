# Research gaps

## gcp-ml-certification (2026-07-13)

Fonte primaria non raggiungibile dall'ambiente di lavoro: il PDF ufficiale
della exam guide (`services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english*.pdf`)
restituisce 403 a livello di proxy di rete della sandbox (policy denial,
non un errore del server). La pagina HTML ufficiale
(`cloud.google.com/learn/certification/guides/machine-learning-engineer`)
reindirizza allo stesso PDF bloccato.

Verificato invece con successo, e usato come fonte primaria per i claim
generali: `cloud.google.com/learn/certification/machine-learning-engineer`
(pagina di overview ufficiale, non il PDF con l'elenco completo dei bullet).

Conseguenza: per ogni lezione `pmle-0X-*` la sezione "Cosa copre l'esame"
riporta solo i claim confermati dalla pagina overview ufficiale o da
`docs.google.com`/`cloud.google.com` per i singoli servizi citati (BigQuery
ML, Vertex AI Workbench, Model Garden, ecc., verificati singolarmente sulla
loro documentazione prodotto). Non riporta l'elenco verbatim completo dei
bullet ufficiali della exam guide, che resta non verificato.

Non risolvere questo gap intuendo o parafrasando bullet non letti. Le due
strade valide:

1. l'utente incolla il testo del PDF ufficiale (accessibile dal suo
   browser, non da questa sandbox) in una futura sessione;
2. una sessione con policy di rete diversa recupera il PDF e aggiorna
   `evidence.yaml` di ogni lezione `pmle-0X-*` con i riferimenti esatti a
   sezione e bullet.

Fino ad allora, ogni lezione `pmle-0X-*` resta in stato `evidence_review`
nella state machine, non `writing`, anche se il testo didattico esiste: il
Gate A (research) non è pienamente soddisfatto senza il testo verbatim.

## Documentazione prodotto (docs.cloud.google.com) non raggiungibile

Tentativo di verifica diretta di BigQuery ML (`CREATE MODEL`, `ML.PREDICT`)
e Vertex AI AutoML sulla documentazione prodotto ufficiale: tutte le pagine
`cloud.google.com/<prodotto>/docs/...` reindirizzano a
`docs.cloud.google.com/...`, che restituisce 403 in questa sessione (non un
blocco di policy del proxy - lo stato del proxy non mostra relay failure
per questo host, quindi il 403 arriva dall'origine, probabilmente una
protezione anti-bot). Solo le pagine `cloud.google.com/learn/...` sono
risultate raggiungibili.

Conseguenza per le lezioni `pmle-0X-*`: la sintassi SQL di BigQuery ML
(`CREATE MODEL`, `ML.PREDICT`) e le caratteristiche di Vertex AI AutoML
descritte sono meccaniche stabili da anni e ben documentate in modo
consistente su innumerevoli fonti indipendenti, ma **non sono state
riverificate sulla pagina prodotto corrente in questa sessione**. Vanno
controllate contro `docs.cloud.google.com` (o l'equivalente raggiungibile)
alla prima occasione utile, prima di marcare `evidence_review: done` su
queste lezioni.

## Rebrand "Gemini Enterprise Agent Platform"

Le fonti secondarie concordano sul fatto che la exam guide 2026 sostituisce
riferimenti a "Vertex AI" con "Gemini Enterprise Agent Platform" in più
sezioni. Non è stato possibile verificare su documentazione prodotto
ufficiale Google Cloud se questo sia un rebrand totale di Vertex AI, un
nuovo prodotto che lo include, o una ridenominazione parziale limitata ad
alcune funzionalità (AutoML, Model Registry, Model Garden). Le lezioni
`pmle-0X-*` useranno "Vertex AI" (nome verificabile sulla documentazione
prodotto corrente) affiancato dalla nota esplicita che l'exam guide
ufficiale usa "Gemini Enterprise Agent Platform" per lo stesso ambito
funzionale, senza affermare l'equivalenza esatta tra i due nomi finché non
verificata.
