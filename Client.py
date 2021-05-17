
# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).

import socket, sys, threading

HOST = '192.168.1.49'
PORT = 50000

class ClientReception(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
    
    def run(self):
        while 1:
            message_recu = self.connexion.recv(1024).decode("Utf8")
            print("*" + message_recu + "*")
            if not message_recu or message_recu.upper() =="FIN":
                break
            # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        th_E._stop()
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()

class ClientEmission(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
    
    def run(self):
        while 1: 
            message_emis = input()
            self.connexion.send(message_emis.encode("Utf8"))




# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2) envoi d'une requête de connexion au serveur :
try:
    mySocket.connect((HOST,PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ClientEmission(mySocket)
th_R = ClientReception(mySocket)
th_E.start()
th_R.start()