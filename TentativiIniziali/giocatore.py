import socket

class Giocatore():
    def __init__(self):
        self.__Server_IP = "192.168.5.25" # IP del tavolo
        self.__Player_IP = "0.0.0.0" # IP del giocatore
        self.__Server_Port = 6767 # Porta del server per inviare le giocate
        self.__Player_Port = 4141 # Porta del client per ricevere l’esito delle giocate
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ipv4 e UDP

    def Start(self):
        try:
            # dovrebbe sollevare un eccezione se una porta è occupata
            self.__sock.bind((self.__Player_IP, self.__Player_Port))
        except:
            raise Exception("Errore nel chiedere la porta di ascolto")
        
        while True:
            # chiedo all'utente da tastiera il numero
            giocata = input('Indovina il numero: ')
            # giocata = giocata.strip()
            
            # validità della stringa
            try:
                giocata = int(giocata) # tentiamo il cast
            except:
                print("Attenzione a quello che scrivi, pirla!")
                # torniamo fuori dal ciclo
                continue

            # convertiamo in bytes
            giocata = giocata.to_bytes(1024, byteorder='little')
            # mandiamo al server la giocata
            self.__sock.sendto(giocata, (self.__Server_IP, self.__Server_Port))
            print('dati inviati')


            # aspettiamo una risposta dal server
            risposta = self.__sock.recvfrom(1024)
            print(risposta)

            # ripartiamo con la partita

