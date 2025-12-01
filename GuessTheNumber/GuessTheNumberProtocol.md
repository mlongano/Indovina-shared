**Guess The Number Protocol**

Questo documento espone le regole di messaggistica che devono essere rispettate tra giocatori e banco in una partita di **Guess The Number** \- *Indovina il numero*

*Nota*  
Nel seguito:

- il banco viene chiamato **house**   
- il giocatore viene chiamato **player**

**Regole del gioco**

Ogni **30** secondi il banco avvia una nuova partita scegliendo a caso un numero compreso nell’intervallo **\[0; 1000\]** estremi inclusi.  
Un giocatore tenta di indovinare il numero avendo a disposizione un massimo di **10** tentativi per ogni partita.

**Specifiche tecniche di sviluppo**

Il protocollo di trasporto utilizzato tra banco e giocatori è **UDP**, rispettivamente sulle porte di default di ascolto **4321** e **1234**. Tali porte possono comunque essere modificate a *Run-Time*

Riepilogo porte di ascolto su protocollo di trasporto **UDP**:  
**House:  4321**  
**Player: 1234**  
---

Messaggi generati dal Giocatore

Il giocatore può esclusivamente inviare messaggi a lunghezza fissa composti da un solo numero intero senza segno, composto da 4 bytes, che rappresenta un singolo tentativo per indovinare il numero.

Messaggi generati dal Banco

Il banco può generare 5 messaggi differenti in base all’esito della giocata o al termine della partita corrente:

- 0: Tentativi terminati del giocatore  
- 1: Tentativo fallito del giocatore  
- 2: Partita vinta dal giocatore  
- 3: Partita vinta da un altro giocatore **(inviato in broadcast)**  
- 4: Partita terminata senza vincitori   **(inviato in broadcast)**

Oltre all’esito della giocata, il banco fornisce una descrizione di lunghezza variabile che può essere sfruttata dal giocatore per conoscere l’avanzamento della partita.  
Per gestire messaggi con lunghezza variabile contenenti tipi di dato differenti (interi e stringhe) è necessario definire un **header** con l’esito e la lunghezza specifica della descrizione e un **payload** con la descrizione effettiva.  
L’esito e la lunghezza della descrizione sono numeri interi senza segno composti da 4 bytes. 

