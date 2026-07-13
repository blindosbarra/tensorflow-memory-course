---
id: pmle-06-monitor-ai-solutions
title: "Certificazione PMLE - Dominio 6: monitorare le soluzioni AI"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: [pmle-05-automate-orchestrate-ml-pipelines]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# Certificazione PMLE — Dominio 6: monitorare le soluzioni AI

!!! note "Stato: contenuto verificato su fonte primaria"
    Contenuto verificato parola per parola contro la exam guide ufficiale
    Google Cloud, fornita direttamente dallo studente. Le definizioni dei
    quattro tipi di drift sono spiegate con conoscenza ML generale, non
    da documentazione di prodotto — segnalato dove compare.

## Cosa copre questo dominio

Il Dominio 6 ("Monitoring AI solutions", **~13% dell'esame**, ultimo
dominio ma non meno importante) copre come riconoscere che qualcosa è
andato storto **dopo** che una soluzione AI è in produzione — sia per
rischi di sicurezza sia per degrado di performance nel tempo. Con questo
dominio si chiude il ciclo dei sei: dalla scelta dello strumento (Dominio
1) al monitoraggio continuo di un sistema già in produzione (qui).

## Teoria essenziale

### 6.1 — Identificare i rischi

Tre considerazioni: costruire sistemi AI sicuri proteggendo contro
sfruttamento non intenzionale e fughe di dati o modelli (esfiltrazione di
dati, prompt malevoli, condivisione involontaria di dati sensibili con un
LLM) con lo strumento di sicurezza appropriato (espressioni regolari,
filtri di sicurezza, Model Armor); allinearsi a pratiche di **AI
responsabile** (es. monitorare per bias nelle predizioni); spiegabilità
del modello su Agent Platform (es. Agent Platform Inference).

### 6.2 — Monitorare, testare, risolvere problemi

Tre considerazioni: configurare **Model Monitoring** su Gemini Enterprise
Agent Platform per metriche di valutazione continua su modelli in
produzione; monitorare problemi comuni; monitorare/testare/valutare
soluzioni generative.

I quattro problemi comuni citati dalla guida (concetti ML generali, non
specifici di un prodotto): **training-serving skew** (incoerenza tra come
i dati sono processati in training e in serving, già visto nei Domini
4-5); **data drift** (la distribuzione statistica dei dati in ingresso
cambia rispetto al training, ma la relazione con il target potrebbe
restare valida); **concept drift** (la relazione tra input e target vero
cambia nel tempo, anche se i dati in ingresso sembrano simili); **feature
attribution drift** (l'importanza relativa delle feature per le
predizioni del modello cambia nel tempo, anche senza calo visibile di
accuratezza).

Sono facili da confondere ma indicano problemi diversi. Con data drift, i
nuovi dati "sembrano diversi" ma la relazione appresa potrebbe essere
ancora valida. Con concept drift, anche se i dati sembrano simili, la
relazione che il modello ha imparato non è più vera. Con feature
attribution drift, il modello continua a fare predizioni ragionevoli ma
inizia a basarle su feature diverse — un segnale d'allarme anche quando
l'accuratezza osservata non è ancora calata.

### Collegamento al corso principale

Le Lezioni 3-4 del corso principale (train/validation/test, data leakage)
insegnano a valutare un modello **una volta**, su uno split fissato. Il
Dominio 6 tratta la domanda che il corso principale non affronta: quella
valutazione resta valida nel tempo? Il monitoraggio continuo è
concettualmente lo stesso controllo di validità della Lezione 4,
applicato ripetutamente su dati che arrivano dopo il deployment, non solo
una volta prima di esso.

## Scenari di ragionamento

(Dettagliati in `knowledge/pmle-06-monitor-ai-solutions/examples.md`.)

- Un modello di credit scoring inizia a fare più errori: profilo
  demografico cambiato → data drift; relazione rischio-profilo cambiata
  per condizioni economiche → concept drift. Richiedono interventi
  diversi.
- Un'applicazione con LLM su documenti interni: un prompt costruito ad
  arte potrebbe indurre il modello a rivelare informazioni sensibili —
  rischio che gli strumenti di sicurezza (filtri, regex, Model Armor)
  mitigano.
- Un modello di rilevamento frodi mantiene accuratezza stabile ma inizia
  a basare le predizioni su feature diverse → feature attribution drift,
  visibile solo monitorando l'importanza delle feature, non solo
  l'accuratezza.

## Errori comuni

- Monitorare solo l'accuratezza aggregata, senza controllare
  distribuzione dei dati o importanza delle feature: data drift o feature
  attribution drift possono essere invisibili finché non sono già seri.
- Trattare la sicurezza di un'applicazione con LLM come un problema
  risolto una volta in sviluppo, invece che come monitoraggio continuo.
- Confondere data drift e concept drift, applicando la correzione
  sbagliata.
- Trattare il monitoraggio del bias come separato dal monitoraggio
  "tecnico": la guida le tratta come parte della stessa competenza di
  identificazione dei rischi.

## Quiz

1. Un modello di credit scoring peggiora. Come distingui se è data drift
   o concept drift, e perché la distinzione conta per la correzione da
   applicare?
2. Perché il monitoraggio della sicurezza di un'applicazione con LLM non
   può fermarsi alla fase di sviluppo?
3. Un modello mantiene la stessa accuratezza aggregata per mesi, ma inizia
   a basare le predizioni su feature diverse rispetto a quando è stato
   validato. Quale tipo di drift descrive questo caso, e perché
   l'accuratezza da sola non lo cattura?

<details>
<summary><b>Apri le risposte</b></summary>

1. Se i dati in ingresso "sembrano diversi" ma la relazione con il target
   potrebbe restare valida, è data drift; se anche con dati simili la
   relazione appresa non è più vera, è concept drift. La distinzione
   conta perché nel primo caso può bastare più dati recenti dello stesso
   tipo, nel secondo serve riconsiderare cosa il modello sta cercando di
   predire.
2. Perché nuovi tentativi di prompt malevolo o di esfiltrazione dati
   possono emergere dopo il rilascio, con utenti reali che il team non ha
   previsto in fase di test; la sicurezza va quindi monitorata in modo
   continuo, non verificata una sola volta.
3. Feature attribution drift: l'importanza relativa delle feature per le
   predizioni cambia nel tempo. L'accuratezza da sola non lo cattura
   perché il modello può continuare a dare risposte corrette pur
   basandole su segnali diversi da quelli validati — un cambiamento
   interno silenzioso finché non emerge un calo di performance più
   evidente.

</details>

## Fonti

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (fonte primaria verbatim, fornita dallo studente in questa
  sessione):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (pagina ufficiale, contesto generale sull'esame):
  https://cloud.google.com/learn/certification/machine-learning-engineer
