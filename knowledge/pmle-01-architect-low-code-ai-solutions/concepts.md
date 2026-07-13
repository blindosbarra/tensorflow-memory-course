# Concepts: pmle-01-architect-low-code-ai-solutions

Decisione research: `NEEDS_REVERIFICATION` (vedi evidence.yaml e
`course/research_gaps.md`). Il testo sotto e' costruito solo sui claim
`verified`; i due claim `needs_reverification` sono usati con nota
esplicita nella lezione, non nascosti.

## Concetti coperti

1. Il Dominio 1 dell'esame ("architect low-code AI solutions", ~13% del
   peso secondo fonti secondarie corroboranti, percentuale non confermata
   sulla exam guide primaria) valuta la capacita' di **scegliere lo
   strumento con il minimo codice necessario** per un problema di ML dato,
   non di scrivere quel codice a mano.
2. Due famiglie di strumenti low-code distinte, con casi d'uso diversi:
   - **BigQuery ML**: addestri e servi modelli con SQL, dentro il
     data warehouse dove i dati gia' vivono. Adatto quando i dati sono
     gia' in BigQuery e il problema e' tabellare/serie storiche.
   - **AutoML**: addestri modelli su dati tabellari, immagini, testo,
     video, senza scrivere l'architettura del modello. Adatto quando serve
     un modello di produzione senza competenze di deep learning
     specializzate.
3. Una terza famiglia: usare **API o modelli fondazionali gia' pronti**
   (non addestrare nulla, solo integrare) quando il compito rientra in
   capacita' generiche (visione, linguaggio, generazione), valutando
   costo/latenza/disponibilita' come vincoli di progettazione, non solo
   come dettagli implementativi.

## Collegamento al resto del corso

Le lezioni 1-15 del corso principale insegnano a costruire un
classificatore **da zero** (NumPy, poi Keras) per capire *cosa* fa un
modello. Questo modulo insegna la decisione opposta e complementare:
*quando NON serve costruirlo da zero* perche' uno strumento gestito
risolve lo stesso problema piu' in fretta. Sono competenze diverse:
capire il modello (corso principale) vs scegliere lo strumento giusto per
il contesto aziendale (questo modulo).

## Limiti

Questa lezione non tratta la sintassi SQL completa di BigQuery ML ne' la
configurazione dettagliata di un job AutoML: sono meccaniche stabili ma
non riverificate in questa sessione (vedi evidence.yaml). Non tratta
"Gemini Enterprise Agent Platform" come prodotto specifico, perche' il suo
rapporto esatto con Vertex AI non e' verificato (vedi research_gaps.md).
