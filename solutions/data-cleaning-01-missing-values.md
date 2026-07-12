# Soluzione: missing values

La soluzione completa, spiegata riga per riga, sta **dentro il notebook
della lezione**, subito dopo la cella "Prova tu":

```text
notebooks/lezione-01-dati-mancanti.ipynb
```

## Risposte al quiz

Anche queste sono nel notebook (sezione finale, blocco richiudibile "Apri le
risposte"). Copia di riferimento:

1. Il guasto dipende dal valore non osservato (MNAR): eliminare le righe
   mancanti sottorappresenta proprio le ore calde e distorce le stime.
2. Controllerei forma, asimmetria e valori estremi della distribuzione
   osservata, oltre al significato operativo della misura. La mediana e'
   resistente agli estremi; la media usa tutte le distanze.
3. Dopo `fillna` non e' piu' possibile distinguere una misura originale da
   una sostituita guardando il solo valore. Il flag preserva la provenienza.
