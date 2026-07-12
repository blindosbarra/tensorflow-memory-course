# Soluzione: duplicati, tipi e outlier

La soluzione completa, spiegata riga per riga, sta **dentro il notebook
della lezione**, subito dopo la cella "Prova tu":

```text
notebooks/duplicates-types-outliers.ipynb
```

## Risposte al quiz

Anche queste sono nel notebook (sezione finale, blocco richiudibile "Apri le
risposte"). Copia di riferimento:

1. No. E' un outlier statistico possibile, ma non viola il contratto di
   dominio. Va investigato, non corretto automaticamente.
2. La stessa stazione produce molte letture valide. Senza l'istante, tutte
   diventerebbero falsi duplicati; identita' e' una decisione sulla chiave.
3. Serve un flag creato prima del `clip`: dopo, tutti i valori sono dentro il
   contratto per costruzione e non si puo' piu' sapere quali erano fuori.
