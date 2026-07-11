# Soluzione commentata: missing values

L'implementazione completa, applicata al dataset challenge e non all'esempio
guidato, e' in `solutions/data-cleaning-01-missing-values_starter.py`.

## Risposte al quiz

1. **Non basta sapere quante celle sono vuote.** Se l'assenza dipende dal valore
   non osservato, il sottoinsieme visibile puo' essere distorto; la strategia va
   motivata usando il processo che ha prodotto l'assenza.
2. **La mediana e' piu' robusta a pochi valori estremi.** La media usa ogni
   distanza numerica e viene trascinata maggiormente dagli estremi.
3. **L'imputazione comprime la distribuzione.** Inserire molte copie dello stesso
   valore crea massa artificiale e tende a ridurre la variabilita'; il flag rende
   osservabile quali valori non erano originali.
