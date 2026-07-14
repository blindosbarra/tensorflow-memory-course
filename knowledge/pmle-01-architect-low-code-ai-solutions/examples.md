# Examples: pmle-01-architect-low-code-ai-solutions

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). I tre scenari sotto sono
sviluppati per intero (non solo elencati) nella lezione pubblicata
(`docs/modules/pmle-01-architect-low-code-ai-solutions.md`), attorno a
un'unica azienda fittizia ("Nordica Commerce") per dare continuità invece
di tre esempi scollegati.

## Scenario 1: previsione della domanda (BigQuery ML)

Nordica ha tre anni di storico ordini già in BigQuery, per SKU, per
settimana, e vuole prevedere le vendite del prossimo trimestre. Il team è
composto da due analisti forti in SQL, senza competenze di deep learning
dedicate. L'alternativa "fai da te" (esportare i dati, allenare un ARIMA
in un notebook con pandas/statsmodels, ripetere l'export ogni settimana)
comporta tre costi nascosti: una pipeline di export da mantenere, un
ambiente notebook da tenere aggiornato, previsioni che invecchiano tra un
export e l'altro. Un `CREATE MODEL` di tipo `ARIMA_PLUS` in BigQuery ML
elimina tutti e tre, perché addestra dove i dati già vivono.

## Scenario 2: controllo qualità sulle foto prodotto (AutoML)

Il magazzino di Nordica fotografa ogni reso e vuole segnalare
automaticamente i pezzi danneggiati; esiste già un pilota con qualche
migliaio di foto etichettate. Nessuno in azienda ha mai progettato una
rete convoluzionale — costruirla da zero (il percorso delle Lezioni 6-15
del corso principale) richiederebbe settimane di lavoro specialistico per
un'azienda il cui prodotto non è il machine learning. Agent Platform
AutoML assorbe la complessità architetturale: il team fornisce solo le
foto etichettate.

## Scenario 3: riassunto dei ticket di assistenza (API/modello fondazionale)

Il supporto clienti di Nordica riceve circa duemila ticket al giorno e
vuole un riassunto automatico per ciascuno. Riassumere testo è una
capacità che un modello fondazionale già possiede, quindi la scelta a
minimo codice è integrare un modello del Model Garden via API, non
addestrarne uno nuovo. Il vincolo che la exam guide rende esplicito è il
costo di quella integrazione su scala: chiamare il modello più potente
disponibile duemila volte al giorno fa crescere la spesa annuale in
proporzione e può introdurre più latenza di quanta lo strumento di
supporto ne tolleri. Un modello più piccolo, scelto o messo a punto per
questo compito specifico, può raggiungere la stessa qualità percepita a
una frazione del costo.

## Scenario 4 (esercizio nella lezione, senza soluzione qui)

Un quarto scenario — stima del rinnovo contratto per clienti B2B, con dati
già collegati in più tabelle BigQuery — è proposto come esercizio nella
sezione "Prova tu" della lezione pubblicata, con la soluzione ragionata
nel quiz finale. Non ripetuto qui per non anticipare la risposta.
