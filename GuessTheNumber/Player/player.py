import socket
import threading
# Per l'invio e la ricezione dei dati ho bisogno di bytes
# Per la loro conversione conviene usare la libreria struct
import struct

# Classe che implementa il giocatore
class Player():
    """
    La classe Player implementa il giocatore
    Viene sfruttato il multithreading per gestire:
     - L'invio di giocate (un tentativo alla volta)
     - La ricezione dell'esito di ogni giocata

    Una giocata consiste in un messaggio con 1 numero intero senza segno da 4 bytes

    Una risposta consiste in un messaggio con 2 numeri interi senza segno da 4 bytes e 
    una descrizione di lunghezza variabile
    Il primo valore rappresenta la codifica dell'esito
    Il secondo valore rappresenta la lunghezza in bytes effettiva della descrizione che segue in coda 
    """

    def __init__(self, housePort = 4321, houseIP = "127.0.0.1", playerPort = 1234):
        """
        Costruttore
        Il costruttore della classe Player accetta i seguenti parametri:
         - La porta e l'IP di ascolto remoto dei messaggi UDP sul banco
         - La porta di ascolto locale dei messaggi UDP dal banco
        """
        # Dettagli di connessione verso il banco
        self.__housePort = housePort
        self.__houseIP = houseIP
        # Il giocatore si metterà in ascolto su tutte le proprie interfacce di rete e la porta indicata
        self.__playerPort = playerPort
        self.__playerIP = "0.0.0.0"
        # Istanzio un oggetto socket IPv4 e UDP
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__playerIP, self.__playerPort))
        self.__maxBuffer = 1024

    def Start(self):
        """
        Start()
        Metodo pubblico per la partecipazione al gioco
        """
        # Questo metodo avvia 2 threads, uno per l'invio delle giocate al banco e uno per gestire le risposte
        senderThread = threading.Thread(target = self.__Sender)
        senderThread.start()

        receiverThread = threading.Thread(target = self.__Receiver)
        receiverThread.start()
    
    def __Sender(self):
        """
        Metodo privato avviato come thread per l'invio dei messaggi al banco
        """
        # Il formato "!" forza il Big-Endian, I è un intero senza segno di 4 bytes
        format ="!I"

        # Continuo a chiedere un valore intero all'utente da inviare come giocata al banco
        while True:
            try:
                # Chiedo il numero all'utente via tastiera
                number = int(input("Scrivi un numero da 0 a 1000: "))
                # Converto il numero inserito in bytes
                dataPacked = struct.pack(format, number)
                # Adesso li posso inviare
                self.__sock.sendto(dataPacked, (self.__houseIP, self.__housePort))
            except TypeError as tpe:
                print(f"Attenzione, hai digitato un valore errato!\n{tpe}")
            except Exception as e:
                print(f"Attenzione, qualcosa è andato storto nell'invio dei dati!\n{e}") 

    def __Receiver(self):
        """
        Metodo privato avviato che thread per l'ascolto dei messaggi dal banco
        """
        # Il formato "!" forza il Big-Endian, "I" rappresenta un intero senza segno da 4 bytes
        format = "!II"
        # TODO da completare il formato...

        # Ciclo infinito di attesa messaggi
        while True:
            try:
                # Attesa bloccante di messaggi
                (data, (houseIP, housePort)) = self.__sock.recvfrom(self.__maxBuffer)
                print(f"Arrivato un messaggio:\n{data}")

                # TODO Gestione dell'esito e della descrizione...
            except:
                pass
    

