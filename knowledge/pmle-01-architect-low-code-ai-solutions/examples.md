# Examples: pmle-01-architect-low-code-ai-solutions

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud - vedi nota del modulo in
`course.yaml`). Gli scenari sotto sono di ragionamento, non codice testato.

## Scenario 1: dati gia' in BigQuery

Un'azienda ha lo storico vendite in BigQuery e vuole prevedere le vendite
del prossimo trimestre per prodotto. I dati non devono uscire dal
warehouse, il problema e' una serie storica tabellare. La scelta a minimo
codice e' BigQuery ML con un modello di forecasting, non l'esportazione dei
dati verso un notebook.

## Scenario 2: classificazione di immagini senza team ML dedicato

Un'azienda deve classificare foto di prodotti difettosi vs integri, non ha
un team di computer vision, ha poche migliaia di immagini etichettate. La
scelta a minimo codice e' AutoML per immagini, non una rete convoluzionale
scritta da zero (il corso principale, Lezioni 6-15, insegna a costruirla
per capire *come* funziona; qui la domanda e' *quando* non serve
costruirla).

## Scenario 3: compito generico di linguaggio

Un'azienda vuole riassumere ticket di supporto in arrivo. Il compito
rientra nelle capacita' generiche di un modello fondazionale gia'
disponibile: la scelta a minimo codice e' integrare un'API esistente
(valutando costo e latenza), non addestrare un modello dedicato.
