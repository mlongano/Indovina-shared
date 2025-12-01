import socket
import threading
import random
import time
# Per l'invio e la ricezione dei dati ho bisogno di bytes
# Per la loro conversione conviene usare la libreria struct
import struct

class House:
    """
    La classe House implementa il banco di gioco
    Viene sfruttato il multithreading per gestire:
     - Il tempo di gioco effettivo
     - La successione di giocate da parte dei giocatori

    Una giocata consiste in un messaggio con 1 numero intero senza segno da 4 bytes

    Una risposta consiste in un messaggio con 2 numeri interi senza segno da 4 bytes e 
    una descrizione di lunghezza variabile
    Il primo valore rappresenta la codifica dell'esito
    Il secondo valore rappresenta la lunghezza in bytes effettiva della descrizione che segue in coda 
    """

    def __init__(self, housePort = 4321, playerPort = 1234):
        """
        Costruttore
        Il costruttore della classe House accetta i seguenti parametri:
         - La porta di ascolto locale dei messaggi UDP provenienti dai giocatori
         - La porta di ascolto remota dei messaggi sui giocatori
        """
        # Mi metterò in ascolto su tutte le interfacce di rete e sulla porta indicata
        self.__housePort = housePort
        self.__houseIP = "0.0.0.0"
        # Salvo la porta di ascolto sui giocatori
        self.__playerPort = playerPort
        # Istanzio un oggetto socket con IPv4 e UDP - con abilitazione del broadcast
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__sock.bind((self.__houseIP, self.__housePort))
        self.__maxBuffer = 1024

        # Numero da indovinare
        self.__number = 0
        # Durata di una partita in secondi
        self.__gameTime = 30
        # Istante di tempo in cui inizia una partita
        self.__gameStart = 0
        # Per sapere se una partita è finita
        self.__stopGame = False
        # Intervallo massimo di attesa per una giocata (in secondi)
        self.__interval = 5
        self.__sock.settimeout(self.__interval)

        # Dizionario di giocatori dove la chiave è l'IP e il valore è il numero di giocate rimanenti
        self.__players = {}
        # Numero massimo di giocate per ogni giocatore
        self.__maxAttempts = 10

    def Start(self):
        """
        Start()
        Metodo pubblico per la gestione infinita di partite
        e accettare le giocate da parte dei giocatori
        """

        # TODO Avvio un thread che tiene il tempo di gioco...

        # Un ciclo infinito esterno gestisce le varie partite
        # Un ciclo infinito interno gestisce le giocate di una singola partita
        while True:
            # Per ogni partita scelgo un numero casuale
            self.__number = random.randint(0, 1000)
            print(f"Nuova partita avviata! Il numero da indovinare è {self.__number}")
            
            # Elimino tutti i giocatori della partita precedente
            self.__players = {}

            # Inizia la partita!
            self.__stopGame = False
            # Azzero il contatore del tempo
            self.__gameStart = time.monotonic()
            while True:
                # Mi metto in ascolto temporaneo di una giocata da parte di qualcuno
                try:
                    # Controllo se è finito il tempo
                    if self.__stopGame:
                        # Mando un messaggio in broadcast a tutti i giocatori
                        # avvisando che la partita è finita senza un vincitore
                        description = f"La partita è finita! Nessuno ha indovinato il numero {self.__number}"
                        self.__SendMessage(4, description, "255.255.255.255")
                        break

                    # Attendo una giocata da qualcuno
                    (data, (playerIP, playerPort)) = self.__sock.recvfrom(self.__maxBuffer)
                    print(f"Arrivati dati:\n{data}")

                    # Controllo se il giocatore è nel dizionario

                    # Riduco il numero delle sue giocate

                    # Controllo se ha finito i tentativi

                    # Controllo se ha indovinato il numero

                    # torno in attesa... 


                    pass
                except Exception as e:
                    # Gestione di eventuali errori
                    print(f"E' successo qualcosa di brutto... \n{e}")
                    # Si ignora il problema e si passa alla giocata successiva
    
    def __SendMessage(self, result, description, playerIP):
        """
        Metodo privato per l'invio dell'esito con descrizione di una singola giocata
        al player indicato, in unicast o in broadcast a seconda dell'IP
        """
        pass