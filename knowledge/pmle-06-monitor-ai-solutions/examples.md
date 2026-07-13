# Examples: pmle-06-monitor-ai-solutions

Nessun esempio di codice eseguito in questo repository per questo modulo
(teoria pura, nessuna credenziale cloud). Gli scenari sotto sono di
ragionamento, non codice testato.

## Scenario 1: distinguere data drift da concept drift

Un modello di credit scoring inizia a fare più errori. Ipotesi A: il
profilo demografico dei nuovi richiedenti è cambiato (più giovani, meno
storico creditizio) — questo è data drift, i dati in ingresso sono
diversi. Ipotesi B: le condizioni economiche generali sono cambiate e lo
stesso profilo che prima indicava basso rischio ora ne indica uno più
alto — questo è concept drift, la relazione tra input e target vero è
cambiata anche se i dati sembrano simili. Le due ipotesi richiedono
interventi diversi: nella prima potrebbe bastare più dati recenti dello
stesso tipo, nella seconda serve riconsiderare cosa il modello sta
cercando di predire.

## Scenario 2: sicurezza applicata a un'applicazione con LLM

Un'applicazione aziendale usa un LLM per rispondere a domande dei
dipendenti su documenti interni. Un rischio citato dalla sottosezione 6.1
è che un dipendente, con un prompt costruito ad arte, induca il modello a
rivelare informazioni sensibili contenute nel contesto ma non destinate a
quell'utente. Gli strumenti di sicurezza (filtri, regex per pattern noti,
Model Armor) servono a mitigare questo tipo di rischio, non solo errori
di predizione.

## Scenario 3: feature attribution drift senza calo di accuratezza visibile

Un modello di rilevamento frodi mantiene la stessa accuratezza aggregata
per mesi, ma inizia gradualmente a basare le predizioni su feature diverse
rispetto a quando è stato validato (es. da pattern di importo a pattern
di orario). L'accuratezza osservata non segnala ancora un problema, ma il
comportamento interno del modello è cambiato — esattamente il tipo di
segnale che il monitoraggio della feature attribution drift, distinto
dal solo monitoraggio dell'accuratezza, è pensato per catturare.
