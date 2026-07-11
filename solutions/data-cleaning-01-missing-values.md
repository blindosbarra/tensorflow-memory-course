# Soluzione commentata: missing values

L'implementazione completa del challenge sui sensori, diverso dall'esempio
guidato, e' in `solutions/data-cleaning-01-missing-values_starter.py`.

## Risposte al quiz

1. Il guasto dipende dal valore non osservato: eliminare i picchi mancanti
   sottorappresenta proprio le ore calde e puo' abbassare le stime.
2. Controllerei forma, asimmetria e valori estremi della distribuzione
   osservata, oltre al significato operativo della misura. La mediana e' piu'
   resistente agli estremi; la media usa tutte le distanze.
3. Dopo `fillna` non e' piu' possibile distinguere una misura originale da una
   sostituita guardando il solo valore. Il flag preserva questa provenienza.
