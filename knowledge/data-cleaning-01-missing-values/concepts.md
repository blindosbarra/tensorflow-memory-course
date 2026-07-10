# Concepts: missing values

Decisione research: `READY_FOR_WRITING`.

## Concetti coperti

1. Un valore mancante non e' sempre lo stesso oggetto tecnico: pandas distingue
   rappresentazioni come `NaN`, `NaT` e `NA` in base al tipo di dato.
2. La diagnosi deve precedere la correzione: contare i missing value per colonna
   rende esplicita la perdita informativa.
3. Per un dataset tabellare piccolo, due scelte semplici e verificabili sono:
   scartare righe prive di campi critici e imputare feature non critiche.

## Collegamento al Memory AI Lab

Una memoria senza testo o timestamp non e' recuperabile in modo affidabile nel
progetto finale. Campi come `type` e `importance`, invece, possono essere
imputati in modo trasparente e marcati con flag di audit.

## Limiti

Questa lezione non tratta meccanismi statistici come MCAR, MAR e MNAR. Il tema
richiede una lezione successiva e una fonte metodologica dedicata.
