# Pitfalls: pmle-05-automate-orchestrate-ml-pipelines

- Automatizzare l'intera pipeline senza un passo di validazione dei dati
  o del modello prima di procedere: un errore a monte (dati corrotti, un
  modello peggiore del precedente) si propaga automaticamente invece di
  essere bloccato.
- Riaddestrare a un intervallo fisso arbitrario senza una policy motivata
  (es. basata su calo di metriche o volume di nuovi dati): spreca calcolo
  se il modello non ne ha bisogno, o lo lascia obsoleto se l'intervallo è
  troppo lungo.
- Scrivere il preprocessing due volte, una nella pipeline di training e
  una nel servizio di serving, invece di condividere la stessa logica:
  è la causa più comune di training-serving skew a livello di pipeline
  (vedi anche Dominio 4).
- Confondere CI/CD tradizionale (test e distribuzione di codice) con
  CI/CD/CT: la componente "CT" (continuous training) è specifica di ML e
  riguarda il modello stesso, non solo il codice che lo produce.
