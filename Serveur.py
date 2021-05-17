# Définition d'un serveur réseau rudimentaire2#
# # Ce serveur attend la connexion d'un client
import sys
import socket
import threading
from threading import Lock
import os 
HOST = '192.168.1.49'
PORT = 50000
counter = 0         # compteur de connexions actives
dernierPrix = "0"

mutex = Lock()

class Server(threading.Thread):
      def __init__ (self, conn) :
            threading.Thread.__init__(self)
            self.connexion = conn
      def run(self):
            # Dialogue avec le client :
            nom = self.getName() # Chaque thread possède un nom
            while 1:
                  msgClient = self.connexion.recv(1024).decode("Utf8")
                  if not msgClient or msgClient.upper() =="FIN":
                        break
                  message = "%s> %s" % (nom, msgClient)
                  print(message)
            # Faire suivre le message à tous les autres clients :
                  #debut section critique 
                  mutex.acquire()
                  for cle in conn_client:
                        if cle != nom: # ne pas le renvoyer à l'émetteur
                              conn_client[cle].send(message.encode("Utf8"))
                  mutex.release()
                  #fin section critique
            # Fermeture de la connexion :
            self.connexion.close() # couper la connexion côté serveur
            del conn_client[nom] # supprimer son entrée dans le dictionnaire
            print("Client %s déconnecté." % nom)
# Le thread se termine ici

      #Fonction Consulter le fichier factures.txt par le serveur qui
      #joue le role du commisseur-prisur 
      def consulterFacture(self):
            file = open('factures.txt', 'r')
            lignes = file.read()
            print(lignes)
      
      #Fonction Consulter le fichier histo.txt par le serveur qui
      #joue le role du commisseur-prisur 
      def consulterHisto(self):
            file = open('histo.txt', 'r')
            lignes = file.read()
            print(lignes)
      
      #Fonction Consulter le fichier biens.txt par le serveur qui
      #joue le role du commisseur-prisur et qui retourne l'id d'article et son prix de début 
      def consulterBiens(self,dernierPrix):
            file = open('biens.txt', 'r')
            T = file.readlines()
            print(T)
            for ligne in T :
                  d = 'Disponible'
                  if d in ligne.split():
                         idArticle = ligne[0]
                         prixArticle = ligne[3:8]
            file.close()
            if int(dernierPrix) > int(prixArticle):
                  prixArticle = dernierPrix
            return (idArticle,prixArticle)

      #Fonction de comparaison entre le prix de début et le prix anoncer par le client 
      #et faire la mise à jour du fichier biens.txt et histo.txt
      def comparaisonPrix(self, msgClient, L):
            file = open('biens.txt', 'r')
            T= file.readlines()
            file.close()
            if int(msgClient) > int(L[1]) :
                  print("faire mise à jour")
                  x=int(L[0])
                  T[x] = "%s  %s  %s Disponible 0\n" %(L[0],L[1],msgClient)
                  file = open('biens.txt', 'w') 
                  file.writelines(T)  
                  #Mise à jour du fichier texte Histo.txt pour la tracabilité    
                        #récupération du l'ancien continue 
                  file = open('histo.txt', 'r')
                  lignes = file.readlines()
                  file.close()
                  #Faire realement la mise à jour du contenu du fichier histo.txt
                  lignes.append('\n'+"2 %d echec \n" %(int(msgClient)-int(L[1])))
                  file = open('histo.txt', 'w')
                  file.writelines(lignes)
                  return(msgClient)
            else : 
                  print("Donner prix >")
                  return(L[1])


      #Cette fonction est responsable à la fermuture de la vente aux encheres 
      #la mise à jour finale des fichiers biens, histo et facture 
      def clotureVente(self): 
            #Mise à jour du fichier texte Histo.txt pour la tracabilité    
                        #récupération du l'ancien continue 
            file = open('Factures.txt', 'r')
            lignes = file.readlines()
            file.close()
            #Faire realement la mise à jour du contenu du fichier histo.txt
            #On va faire l'ajout de la ligne au fichier sans oublier d'ajouter les 20% supplimentaire et de faire le total 
            #des achats pour les clients en question 
            file = open('Factures.txt', 'w')
            file.writelines(lignes)


# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2) liaison du socket à une adresse précise :14#
try:
     mySocket.bind((HOST, PORT))
except socket.error:
      print("La liaison du socket à l'adresse choisie a échoué.")
      sys.exit
while 1:
            # 3) Attente de la requête de connexion d'un client
      print("Serveur prêt, en attente de requêtes ...")
      mySocket.listen(5)
      # Attente et prise en charge des connexions demandées par les clients :
      conn_client = {}    # dictionnaire des connexions clients    
      while 1:
            connexion, adresse = mySocket.accept()
            # Créer un nouvel objet thread pour gérer la connexion :
            th = Server(connexion)
            th.start()
           
            L=th.consulterBiens(dernierPrix)
            # Mémoriser la connexion dans le dictionnaire :
            it = th.getName() # identifiant du thread
            conn_client[it] = connexion
            print("Client %s connecté, adresse IP %s, port %s." %\
                        (it, adresse[0], adresse[1]))
           
            # Dialogue avec le client :
            msgServeur = "id de l'article est %s et son prix de départ est %s" % (L[0], L[1])
            connexion.send(msgServeur.encode("Utf8"))
            msgClient = connexion.recv(1024).decode("Utf8")
            #Test sur le nv prix proposer par le client
            dernierPrix = th.comparaisonPrix(msgClient,L)
            #Modification du prix du départ 
            L=th.consulterBiens(dernierPrix)
            #Attendre 30 secondes et les clients ne reponds pas cloturer la vente aux encheres 
            #pour cette article en question
      # 6) Fermeture de la connexion :
      connexion.send("fin".encode("Utf8"))
      print("Connexion interrompue.")
      connexion.close()


      ch = input("<R>ecommencer <T>erminer ? ")
      if ch.upper() =='T':        
         break
