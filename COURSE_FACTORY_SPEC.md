# TensorFlow Memory AI Course Factory

> Specifica operativa per costruire, verificare e pubblicare con Codex un corso GitHub completo su TensorFlow, Keras, data engineering, DNN, embedding, sistemi di memoria, Gemma, LoRA, Vertex AI, evaluation, monitoring e preference training.

## 1. Missione

Questo repository deve diventare contemporaneamente:

1. un corso pratico per una persona con esperienza teorica e pratica limitata;
2. un laboratorio incrementale eseguibile;
3. una piccola “course factory” ripetibile;
4. un progetto finale dedicato alla rappresentazione e al recupero di memorie;
5. un sito statico pubblicabile con GitHub Pages.

Il lettore deve poter studiare in sessioni da 15–30 minuti. Ogni unità deve lasciare un risultato osservabile: codice eseguito, grafico, modello addestrato, test superato o breve esercizio completato.

## 2. Definizione di completamento

Il corso non è completo quando esistono molti file Markdown. È completo quando:

- tutti i moduli dichiarati in `course/course.yaml` sono presenti;
- ogni lezione dichiara prerequisiti, obiettivi e tempo stimato;
- ogni affermazione tecnica rilevante è collegata a una fonte primaria;
- tutti gli esempi Python passano lint e test;
- tutti i notebook sono eseguibili dall’inizio alla fine;
- dataset e output attesi sono riproducibili;
- gli esercizi hanno hint e soluzione separata;
- il progetto finale funziona localmente;
- esiste almeno una pipeline Vertex AI documentata e testabile;
- evaluation e monitoring producono report;
- il sito statico viene compilato senza errori;
- un principiante può seguire il percorso senza dipendenze implicite.

## 3. Principi non negoziabili

### 3.1 Fonti

Ordine di preferenza:

1. documentazione ufficiale TensorFlow, Keras, Google Cloud, OpenAI;
2. paper originali;
3. repository ufficiali;
4. articoli tecnici degli autori o maintainer;
5. fonti secondarie solo per chiarimenti, mai come unica prova.

Non usare contenuti copiati. Riassumere, citare e collegare.

### 3.2 Nessuna invenzione

Quando una fonte non basta:

- aggiungere una voce a `research_gaps.md`;
- non completare il paragrafo con supposizioni;
- non inventare API, metriche, risultati o compatibilità.

### 3.3 Esecuzione prima della pubblicazione

Ogni esempio deve essere eseguito. Una lezione non può essere marcata `done` se il relativo notebook non è stato validato automaticamente.

### 3.4 Progressione

La progressione obbligatoria è:

```text
Python/NumPy essenziale
→ dati e pulizia
→ tensori e autodiff
→ Keras e DNN
→ training ed evaluation
→ testo ed embedding
→ rappresentazione delle memorie
→ grafi e retrieval
→ Transformer e Gemma
→ LoRA/QLoRA
→ pipeline e deploy cloud
→ monitoring
→ preference training
→ progetto finale
```

### 3.5 Microlearning

Ogni lezione:

- 15–30 minuti;
- massimo 3 concetti nuovi principali;
- un solo obiettivo pratico;
- riepilogo finale di massimo 8 punti;
- quiz breve;
- esercizio eseguibile.

## 4. Risultato finale: Memory AI Lab

Il progetto finale riceve memorie testuali e produce:

```json
{
  "memory_id": "mem_001",
  "text": "Il 3 luglio Marco è andato a Glasgow con suo figlio.",
  "timestamp": "2026-07-03",
  "type": "episodic",
  "entities": ["Marco", "Glasgow", "figlio"],
  "topics": ["travel", "family"],
  "importance": 0.72,
  "should_store": true,
  "embedding": "<vector>",
  "relations": [
    {"source": "Marco", "type": "visited", "target": "Glasgow"}
  ]
}
```

Funzioni minime:

- pulizia e validazione dei dati;
- classificazione del tipo di memoria;
- stima dell’importanza;
- generazione o estrazione di embedding;
- ricerca per similarità;
- grafo di entità, eventi, luoghi e tempo;
- estrazione strutturata con modello open;
- adattamento LoRA;
- evaluation offline;
- report di drift simulato;
- pipeline di training;
- deploy documentato;
- feedback preferenziale.

## 5. Architettura del repository

```text
.
├── AGENTS.md
├── README.md
├── COURSE_FACTORY_SPEC.md
├── pyproject.toml
├── mkdocs.yml
├── course/
│   ├── course.yaml
│   ├── progress.yaml
│   └── research_gaps.md
├── docs/
│   ├── index.md
│   ├── modules/
│   ├── glossary.md
│   └── references.md
├── knowledge/
│   └── <topic>/
│       ├── concepts.md
│       ├── apis.md
│       ├── examples.md
│       ├── pitfalls.md
│       ├── evidence.yaml
│       └── references.md
├── notebooks/
├── examples/
├── exercises/
├── solutions/
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── src/
│   └── memory_ai/
├── tests/
├── reports/
│   ├── research/
│   ├── evaluation/
│   └── reviews/
├── prompts/
├── templates/
├── schemas/
└── scripts/
```

## 6. Tooling consigliato

### Authoring e orchestrazione

- **Codex**: modifica del repository, implementazione, esecuzione, test e review delle patch.
- **GitHub**: versionamento, issue, pull request e Pages.
- **MkDocs Material**: sito statico costruito dai Markdown.
- **Python 3.11 o 3.12**: ambiente didattico principale.
- **uv**: gestione veloce e riproducibile delle dipendenze.
- **Jupyter / nbclient / nbconvert**: notebook e validazione automatica.
- **pytest, ruff, mypy**: test, lint e controlli di tipo.
- **TensorFlow/Keras/KerasHub**: stack ML.
- **Pandas, scikit-learn, NetworkX, Matplotlib**: dati, metriche e grafi.
- **Google Cloud SDK e Vertex AI SDK**: fase cloud.

La versione esatta delle dipendenze deve essere bloccata nel lockfile dopo aver verificato compatibilità e disponibilità nell’ambiente scelto.

## 7. Ruoli della Course Factory

I ruoli sono fasi logiche. Possono essere eseguiti da thread Codex separati, ma comunicano solo tramite file versionati.

### 7.1 Curriculum Planner

Input:

- questa specifica;
- `course/course.yaml`;
- profilo dello studente.

Output:

- mappa dei prerequisiti;
- obiettivi misurabili;
- deliverable;
- ordine delle lezioni;
- criteri di completamento.

Non scrive il contenuto delle lezioni.

### 7.2 Researcher

Per una singola lezione:

- cerca fonti primarie;
- registra URL, titolo, data e claim supportati;
- produce note sintetiche;
- segnala conflitti o API deprecate;
- aggiorna `knowledge/<topic>/`.

Non scrive la lezione finale.

### 7.3 Evidence Reviewer

Controlla:

- autorevolezza;
- attualità;
- corrispondenza tra claim e fonte;
- eventuali incompatibilità di versione;
- copertura delle domande didattiche.

Può respingere il research pack.

### 7.4 Lesson Writer

Usa solo il research pack approvato. Produce:

- intuizione;
- teoria necessaria;
- esempio guidato;
- collegamento al progetto finale;
- riepilogo;
- quiz.

Non inventa codice non eseguito.

### 7.5 Lab Engineer

Produce:

- notebook;
- moduli Python;
- dataset sintetici;
- output attesi;
- test;
- comandi di esecuzione.

### 7.6 Exercise Designer

Produce:

- esercizio;
- criteri di successo;
- hint progressivi;
- test automatici;
- soluzione separata.

### 7.7 Technical Reviewer

Verifica:

- correttezza matematica;
- API;
- esecuzione;
- chiarezza;
- leakage;
- metriche;
- riproducibilità;
- sicurezza e costi cloud.

### 7.8 Editor

Uniforma:

- terminologia;
- stile;
- collegamenti interni;
- glossario;
- lunghezza;
- navigazione.

Non altera il significato tecnico senza nuova review.

## 8. State machine di una lezione

Ogni voce di `course/course.yaml` attraversa:

```text
planned
→ researching
→ evidence_review
→ writing
→ lab_build
→ technical_review
→ learner_review
→ done
```

Una fase fallita torna alla fase precedente.

Codex deve aggiornare `course/progress.yaml` dopo ogni task. Non può marcare `done` senza soddisfare tutti i gate.

## 9. Quality gates

### Gate A — Research

- almeno 2 fonti primarie quando il tema lo consente;
- ogni claim tecnico importante appare in `evidence.yaml`;
- nessuna fonte irraggiungibile;
- eventuali versioni indicate.

### Gate B — Lesson

- obiettivi verificabili;
- prerequisiti espliciti;
- teoria proporzionata;
- nessun salto logico;
- collegamento al progetto finale;
- citazioni presenti.

### Gate C — Code

- `ruff check .`;
- `mypy src`;
- `pytest`;
- notebook eseguito con kernel pulito;
- seed controllato dove possibile;
- nessuna credenziale;
- nessun path locale assoluto.

### Gate D — Didattica

- lezione completabile entro il tempo dichiarato;
- massimo 3 concetti principali;
- output osservabile;
- quiz non puramente mnemonico;
- esercizio coerente con gli obiettivi.

### Gate E — Publish

- build MkDocs;
- link check;
- navigazione aggiornata;
- glossario aggiornato;
- progress tracker coerente.

## 10. Processo operativo

### Passo 0 — Bootstrap

Codex deve:

1. leggere `AGENTS.md`;
2. leggere questa specifica;
3. validare `course/course.yaml`;
4. creare ambiente Python;
5. installare dipendenze;
6. aggiungere CI;
7. costruire il sito vuoto;
8. eseguire i controlli iniziali.

### Passo 1 — Vertical slice

Prima di generare tutto, completare una sola lezione pilota:

`data-cleaning-01-missing-values`

La vertical slice deve includere:

- research pack;
- lezione;
- notebook;
- esercizio;
- soluzione;
- test;
- pagina MkDocs;
- review report.

Solo dopo approvazione estendere la factory.

### Passo 2 — Foundation modules

Completare in ordine:

1. Python e NumPy essenziali;
2. dati tabellari;
3. split e leakage;
4. tensori;
5. gradienti;
6. prima DNN;
7. training loop;
8. overfitting ed evaluation.

### Passo 3 — Memory representation

Costruire progressivamente:

- schema delle memorie;
- dataset sintetico;
- classificatore;
- importance scorer;
- embedding;
- visualizzazione;
- grafo;
- retrieval ibrido.

### Passo 4 — Language model adaptation

- tokenizer e Transformer;
- inferenza con modello open minimo;
- dataset instruction;
- structured output;
- LoRA;
- QLoRA opzionale;
- confronto baseline/fine-tuned.

### Passo 5 — MLOps

- packaging;
- artifact;
- pipeline locale;
- pipeline Vertex AI;
- model registry;
- deploy;
- evaluation;
- monitoring;
- cost guardrails.

### Passo 6 — Preference learning

- raccolta feedback sintetico;
- coppie chosen/rejected;
- reward esplicito;
- preference tuning;
- confronto controllato;
- limiti e rischi.

### Passo 7 — Course release

- eseguire tutti i notebook;
- generare report;
- build del sito;
- release tag;
- changelog;
- istruzioni di studio.

## 11. Prompt di avvio per Codex

Usare questo prompt nel primo thread:

```text
Agisci come lead engineer e course-factory orchestrator.

Leggi integralmente:
- AGENTS.md
- COURSE_FACTORY_SPEC.md
- course/course.yaml
- prompts/
- templates/
- schemas/

Obiettivo immediato:
costruire il bootstrap tecnico del repository e una sola vertical slice completa per la lezione `data-cleaning-01-missing-values`.

Vincoli:
- non generare ancora l’intero corso;
- usa fonti primarie e registra l’evidenza;
- non inventare API o risultati;
- ogni notebook deve essere eseguito;
- ogni esempio deve avere test;
- aggiorna course/progress.yaml;
- crea piccoli commit logici;
- documenta decisioni e lacune;
- non usare credenziali cloud;
- mantieni il percorso eseguibile localmente.

Prima di modificare file:
1. esegui una gap analysis del repository;
2. scrivi `reports/bootstrap-plan.md`;
3. proponi una sequenza di patch;
4. poi implementa senza attendere ulteriori conferme.

Definition of done:
- ambiente riproducibile;
- CI di base;
- sito MkDocs compilabile;
- vertical slice completa;
- tutti i quality gate superati;
- report finale in `reports/reviews/bootstrap-review.md`.
```

## 12. Prompt per completare un modulo

```text
Completa esclusivamente il modulo <MODULE_ID> seguendo la state machine del repository.

Procedura:
1. leggi prerequisiti, dipendenze e deliverable in course/course.yaml;
2. crea o aggiorna il research pack;
3. valida le fonti e compila evidence.yaml;
4. scrivi le lezioni usando il template;
5. implementa lab, notebook ed esercizi;
6. esegui test e notebook;
7. svolgi una review tecnica e didattica;
8. correggi i problemi;
9. aggiorna progress.yaml e la navigazione del sito.

Non marcare il modulo done se:
- ci sono claim non supportati;
- un notebook non è stato eseguito;
- i test falliscono;
- mancano esercizi o soluzione;
- sono presenti dipendenze implicite;
- la documentazione cloud non include costi, cleanup e modalità locale.
```

## 13. Prompt di review indipendente

```text
Non implementare nuove funzionalità. Esegui una review avversariale del modulo <MODULE_ID>.

Controlla:
- correttezza teorica e matematica;
- fonti e attualità;
- compatibilità delle API;
- esecuzione dei notebook;
- leakage e errori metodologici;
- chiarezza per un principiante;
- coerenza con i prerequisiti;
- riproducibilità;
- costi e rischi cloud;
- completezza degli esercizi.

Scrivi il report in reports/reviews/<MODULE_ID>.md con:
- blocker;
- major;
- minor;
- test mancanti;
- claim da verificare;
- decisione PASS o FAIL.

Se trovi problemi, applica solo correzioni chiaramente verificabili. Non nascondere i fallimenti.
```

## 14. Strategia multi-thread Codex

Usare thread separati solo per unità indipendenti:

- Thread A: research pack modulo 1;
- Thread B: research pack modulo 2;
- Thread C: infrastruttura CI e notebook execution;
- Thread D: review di moduli già completi.

Non far modificare contemporaneamente a più thread:

- `course/progress.yaml`;
- `mkdocs.yml`;
- `docs/index.md`;
- file condivisi del progetto finale.

Integrare tramite pull request piccole. Ogni PR deve riferirsi a un modulo o a un’infrastruttura precisa.

## 15. Strategia del modello minimo open

La progressione suggerita è:

1. DNN Keras costruita da zero per classificazione;
2. piccolo encoder o embedding model per similarità;
3. modello Gemma di dimensione compatibile con l’ambiente;
4. LoRA;
5. QLoRA solo se hardware e backend lo consentono.

La factory deve verificare al momento dell’implementazione quali preset KerasHub siano disponibili e compatibili. Non fissare nel materiale didattico nomi o dimensioni senza test.

## 16. Pipeline cloud

La fase cloud deve essere opzionale e avere una modalità locale equivalente.

Pipeline logica:

```text
validate data
→ transform
→ train
→ evaluate
→ quality gate
→ register
→ deploy
→ smoke test
→ monitor
```

Ogni lab cloud deve includere:

- prerequisiti;
- servizi utilizzati;
- stima qualitativa dei costi;
- comando di cleanup;
- alternativa locale;
- separazione tra training e serving;
- gestione delle credenziali tramite meccanismi standard;
- nessuna chiave salvata nel repository.

## 17. Evaluation del Memory AI Lab

Metriche minime:

### Classificazione

- precision;
- recall;
- macro F1;
- confusion matrix;
- calibration quando rilevante.

### Estrazione strutturata

- JSON valid rate;
- field accuracy;
- entity precision/recall;
- date normalization accuracy;
- hallucinated field rate.

### Retrieval

- Recall@K;
- MRR;
- nDCG opzionale;
- temporal relevance;
- duplicate retrieval rate.

### Memoria

- retention correctness;
- contradiction detection;
- update correctness;
- stale-memory rate;
- graph consistency.

### Operazioni

- latenza;
- throughput;
- error rate;
- dimensione artifact;
- uso memoria;
- costo stimato.

## 18. Monitoring

Il corso deve distinguere:

- data quality;
- feature drift;
- prediction drift;
- embedding drift;
- performance drift;
- serving health;
- feedback drift.

Poiché spesso le label arrivano tardi, includere proxy metric e spiegare i loro limiti.

## 19. Human-in-the-loop

Il proprietario del corso deve intervenire in quattro punti:

1. approvazione della vertical slice;
2. prova reale di ogni milestone;
3. decisioni sui costi cloud;
4. valutazione qualitativa del progetto finale.

Il resto può essere automatizzato, ma nessun agente può certificare da solo che il corso sia realmente comprensibile.

## 20. Roadmap consigliata

### Milestone 0 — Factory bootstrap

- struttura;
- ambiente;
- CI;
- MkDocs;
- template;
- vertical slice.

### Milestone 1 — Foundations

- dati;
- TensorFlow;
- Keras;
- DNN;
- evaluation.

### Milestone 2 — Memory representations

- schema;
- embedding;
- visualizzazione;
- grafi;
- retrieval.

### Milestone 3 — Gemma e LoRA

- Transformer;
- inference;
- structured extraction;
- LoRA;
- evaluation.

### Milestone 4 — MLOps

- pipeline;
- deploy;
- monitoring.

### Milestone 5 — Preference learning e capstone

- feedback;
- preference data;
- training;
- applicazione completa;
- sito finale.

## 21. Rischi principali

- generazione massiva di contenuto superficiale;
- tutorial copiati o senza fonti;
- notebook mai eseguiti;
- API obsolete;
- dipendenze incompatibili;
- corso troppo teorico;
- salto prematuro verso LLM e RL;
- costi cloud non controllati;
- “reinforcement learning” usato come etichetta impropria;
- grafi decorativi senza reale utilità;
- metriche non collegate al comportamento desiderato.

La vertical slice e i quality gate servono esattamente a impedire questi fallimenti.

## 22. Fonti iniziali da registrare

- TensorFlow `tf.data` guide: https://www.tensorflow.org/guide/data
- TensorFlow data performance: https://www.tensorflow.org/guide/data_performance
- TensorFlow tutorials: https://www.tensorflow.org/tutorials
- Keras examples: https://keras.io/examples/
- KerasHub getting started: https://keras.io/keras_hub/getting_started/
- Keras Gemma LoRA/QLoRA example: https://keras.io/examples/keras_recipes/parameter_efficient_finetuning_of_gemma_with_lora_and_qlora/
- OpenAI Codex cloud documentation: https://developers.openai.com/codex/cloud
- OpenAI Codex repository: https://github.com/openai/codex

Questa lista è un seed, non l’intera knowledge base.

## 23. Primo comando umano

Dopo aver creato il repository e caricato questi file:

1. collegare il repository a Codex;
2. aprire un nuovo thread;
3. incollare il prompt della sezione 11;
4. lasciare che Codex produca la vertical slice;
5. provare personalmente la lezione;
6. correggere il template prima di scalare.

Non chiedere “costruisci tutto il corso” al primo task. Dopo la vertical slice approvata, assegnare un modulo alla volta o piccoli gruppi senza conflitti.
