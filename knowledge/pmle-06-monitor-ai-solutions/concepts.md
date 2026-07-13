# Concepts: pmle-06-monitor-ai-solutions

Decisione research: contenuto `VERIFIED` contro il testo verbatim della
exam guide ufficiale (vedi evidence.yaml). Le definizioni dei quattro tipi
di deriva (drift) sono spiegate con conoscenza ML generale, non da
documentazione di prodotto.

## Concetti coperti

1. Il Dominio 6 ("Monitoring AI solutions", **~13% del peso**, ultimo
   dominio ma non meno importante) copre come riconoscere che qualcosa è
   andato storto **dopo** che una soluzione AI è in produzione — sia per
   rischi di sicurezza sia per degrado di performance nel tempo.
2. Sottosezione 6.1 — **identificare i rischi**: costruire sistemi AI
   sicuri proteggendo contro sfruttamento non intenzionale e fughe di
   dati o modelli (esfiltrazione di dati, prompt malevoli, condivisione
   involontaria di dati sensibili con un LLM) con lo strumento di
   sicurezza appropriato (espressioni regolari per filtrare pattern
   noti, filtri di sicurezza, Model Armor); allinearsi a pratiche di AI
   responsabile (es. monitorare per bias nelle predizioni); spiegabilità
   del modello su Agent Platform.
3. Sottosezione 6.2 — **monitorare, testare, risolvere problemi**:
   configurare Model Monitoring su Gemini Enterprise Agent Platform per
   metriche di valutazione continua su modelli in produzione; monitorare
   problemi comuni — **training-serving skew** (incoerenza tra come i
   dati sono processati in training e in serving, già visto nei Domini
   4-5), **data drift** (la distribuzione statistica dei dati in ingresso
   cambia rispetto al training), **concept drift** (la relazione tra
   input e target vero cambia nel tempo, anche se i dati in ingresso
   restano simili), **feature attribution drift** (l'importanza relativa
   delle feature per le predizioni del modello cambia nel tempo); e
   monitorare/testare/valutare soluzioni generative.

## Il filo conduttore del dominio

Le due sottosezioni rispondono a: *quali rischi devo prevenire prima che
succedano?* (6.1, sicurezza e responsabilità), *come mi accorgo che il
modello si sta degradando, dopo che è in produzione?* (6.2, monitoraggio
continuo). Il tema comune è che **un modello in produzione non è un
artefatto statico**: sia il mondo che genera i dati sia gli utenti che
interagiscono con il modello cambiano nel tempo, e senza monitoraggio
attivo il degrado passa inosservato fino a diventare un problema serio.

## Perché data drift, concept drift e feature attribution drift sono concetti diversi

Sono facili da confondere ma indicano problemi diversi: con **data
drift**, i nuovi dati "sembrano diversi" (es. distribuzione di età degli
utenti cambiata) ma la relazione con il target potrebbe essere ancora
valida. Con **concept drift**, anche se i dati sembrano simili, la
relazione che il modello ha imparato non è più vera (es. cosa definisce
uno spam email è cambiato). Con **feature attribution drift**, il modello
continua a fare predizioni ragionevoli ma inizia a "guardare" a feature
diverse per farlo — un segnale d'allarme anche quando l'accuratezza
osservata non è ancora calata visibilmente.

## Collegamento al resto del corso

Le Lezioni 3-4 del corso principale (train/validation/test, data leakage)
insegnano a valutare un modello **una volta**, su uno split fissato. Il
Dominio 6 tratta la domanda che il corso principale non affronta: quella
valutazione resta valida nel tempo? Il monitoraggio continuo è
concettualmente lo stesso controllo di leakage e di validità della
Lezione 4, applicato ripetutamente su dati che arrivano dopo il
deployment, non solo una volta prima di esso.

## Limiti

Questa lezione non tratta la configurazione pratica di Model Monitoring,
la sintassi per configurare filtri di sicurezza, o i dettagli di Model
Armor: la exam guide elenca queste come **strumenti/attività da saper
riconoscere**, non fornisce dettagli implementativi. Le definizioni dei
quattro tipi di drift sono conoscenza ML generale, non specifica di
prodotto (vedi evidence.yaml). "Model Armor" e "Agent Platform Inference"
sono citati esattamente come li nomina la guida, senza dettagli
implementativi non verificabili (prodotti troppo recenti per conoscenza
pre-addestramento affidabile, vedi `course/research_gaps.md`).
