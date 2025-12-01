import random
import socket
import time

class Tavolo():
    def __init__(self):
        self.__Server_IP = "0.0.0.0" # Così ascolto su ogni interfaccia di rete del server
        self.__Server_Port= 6767 # Porta di ascolto sul server per i tentativi del giocatore
        self.__Player_Port = 4141 # Porta di ascolto sul client per gli esiti delle giocate
        self.__Max_Tentativi = 10
        self.__Tempo_Limite = 15 # Durata di una partita in secondi
        # Chiedo al sistema operativo la possibilità di mettermi in ascolto
        # in UDP sulla porta Server_Port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 

    # Questo è il metodo principale della classe Tavolo
    # Dopo le fasi iniziali di preparazione del gioco
    # Avvia un loop infinito di giocate dei client
    def Start(self):
        try:
            # dovrebbe sollevare un eccezione se una porta è occupata
            self.__sock.bind((self.__Server_IP, self.__Server_Port))
        except:
            raise Exception("Errore nel chiedere la porta di ascolto")
        
        # Ciclo infinito della gestione delle partite
        while True:
            # Preparo la partita
            numero = random.randint(0, 1000)
            print(f"Generato numero {numero}")

            # Dizionario che tiene traccia dei giocatori e le loro giocate
            # Viene inizializzato come dizionario vuoto perchè non ho idea di chi verrà a giocare
            # Contiene coppie chiave:valore dove la chiave è l'ip del client e il valore è il numero 
            # di giocate rimanenti
            giocatori = {}
            

            # TODO: Implementare la logica per avviare il timer

            # TODO: Implementare una black list di ip bannati

            # Ciclo potenzialmente infinito di gestione di una singola partita
            while True:
                # Mi metto in ascolto di una giocata da parte di qualcuno
                (giocata, (ip_giocatore, porta_giocatore)) = self.__sock.recvfrom(1024) # ascoltiamo 
                giocata = int.from_bytes() # codifica per i caratteri a lunghezza variabile

                
                print(f"Giocata {giocata} da {ip_giocatore} ")
                # Aggiungere il giocatore se non è presente nel dizionario
                if ip_giocatore not in giocatori:
                    giocatori[ip_giocatore] = self.__Max_Tentativi - 1 # consumiamo una giocata
                else:
                    giocatori[ip_giocatore] -= 1 # consumiamo una giocata

                # controlliamo se il giocatore ha esaurito le sue giocate
                if giocatori[ip_giocatore] <= 0:
                    # per evitare che si possa andare "troppo" in negativo
                    # mettiamo a 0
                    giocatori[ip_giocatore] = 0
                    
                    # avviso il giocatore che ha terminato i tentativi e passo alla giocata successiva
                    self.__mandaEsito(f"Hai esaurito i tentativi! Riprova nella prossima partita", ip_giocatore)
                    continue
                
                # Controllo la validità
                if not isinstance(giocata, (int)):
                    # avviso il giocatore che ha sbagliato e passo alla giocata successiva
                    self.__mandaEsito(f"Hai sbagliato! Ti rimangono solo {self.__Max_Tentativi} tentativi", ip_giocatore)
                    continue
                
                # Controllo se il giocatore ha vinto
                # Mando esito
                if giocata == numero:
                    # broadcast 
                    message = f"Il giocatore {ip_giocatore} ha vinto! Inizia una nuova partita"
                    # TODO: elenco di interfacce di rete della nostre macchine ed applicare a tutte le interfacce
                    # in maniera sequenziale le maschere e vedere a quale rete appartengono per poter conoscere
                    # il broadcast
                    # COMPITI: librerie per vedere come si calcola automaticamente il broadcast di un ip, dato l'ip 
                    # e la maschera

                    # mandiamo il messagio al broadcast e alla porta del client
                    self.__mandaEsito(message, "192.168.5.255")
                    break # si termina la partita
                else: # se l'esito è negativo
                    message = f"Hai sbagliato! Ti rimangono solo {self.__Max_Tentativi} tentativi"
                    self.__mandaEsito(message, ip_giocatore)
                    continue

    def __mandaEsito(self, message, ip_giocatore):
        message = message.encode('utf-8')
        self.__sock.sendto(message, (ip_giocatore, self.__Player_Port))
                
                
