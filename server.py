
"""Server for multithreaded (asynchronous) de vente aux enchere -  application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from threading import Timer
from datetime import datetime
import select,time,threading
import os

auction = False
reference= "test"
bidder =""
bidtime= datetime.now()
prix = 0
global prixinit
joins =[]
done = False
factures={}
#processus time 
class TestThreading(object):
    global bidtime
    global bidder
    global auction
    global joins
    global prix
    global prixinit

    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global bidtime
        global bidder
        global auction
        global done
        global joins
        while True:
            # More statements comes here
            
            
            
            if ((datetime.now()-bidtime).seconds==25 and not done):
                diffuserj(bytes("La vente au enchère va cloturer dans 10 seconds" , "utf8"))
                done = True
            if ((datetime.now()-bidtime).seconds>35): #auction ended
                bien = open("bien.txt","a")
                if (bidder!=""): #bidder exist
                    diffuserj(bytes("The auction has ended ,%s won." % bidder, "utf8"))
                    print("The auction has ended ,%s won." % bidder)
                    bien.write(strbien(reference,prixinit,prix,"Vendu",bidder+"\n"))
                    bien.close()
                    histo = open("histo.txt","a")
                    histo.write(strhisto(bidder,prix,"succes\n"))
                    histo.close()
                    #ajouter a factures
                    if (bidder not in list(factures.keys())):
                       fact = open("factures.txt","a")
                       fact.write(strfact(bidder,prix)+"\n")
                       fact.close()
                       factures[bidder]=prix
                    else : #bidder exist deja dans factures
                        factures[bidder]=factures[bidder]+prix
                        remplir()
                        
                    
                    auction = False
                    joins=[]
                    bidder=""
                    break
                
                else :  #no bidder . produit disponible
                    if auction:
                        diffuserj(bytes("Vente aux enchere a fini sans gagnant", "utf8"))
                        print("Vente aux enchere a fini sans gagnant")
                        bien.write(strbien(reference,prixinit,prixinit,"Disponible","N/A\n"))
                        bien.close()
                        auction = False
                        joins=[]
                        break
                    
                    
                auction = False
                joins=[]
                break
                
            time.sleep(self.interval)
#proccessus menu
class menu(object):
    global bidtime
    global bidder
    global auction
    global reference
    global prix
    global prixinit
    global done

    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global bidtime
        global bidder
        global auction
        global done
        global prix
        global prixinit
        global reference
        while True:
            # More statements comes here
            if not auction :
                print("1-Débuter une vente aux encheres")
                print("2-Consulter la liste des biens  ")
                print("3-Consulter la facture d'un acheteur ")
                print("4-Consulter l'historique des propositions ")
                print("5-Quitter")
                reponse = input()
                if (reponse =="1"):
                    reference = input("reference =")
                    prix = int(input("Prix initial = "))
                    prixinit= prix
                    auction = True
                    done = False
                    histo = open("histo.txt","a")
                    histo.write("------------------\n")
                    histo.write("Produit "+reference+" :\n")
                    histo.close()
                    bidtime = datetime.now()
                    tr = TestThreading()
                    diffuser(bytes("La vente aux encheres est débuter avec cette  : "+reference+str(prix), "utf8"))
                    diffuser(bytes("Pour integrer cette cente au enchere veuillez tapez  /join dans le TexteField.", "utf8"))
                    
                    print("en attente de connection...")
                elif (reponse=="2"):
                    bien = open("bien.txt","r")
                    l = bien.readlines()
                    for i in l :
                        print(i)
                    bien.close()
                elif (reponse=="4"):
                    histo = open("histo.txt","r")
                    l = histo.readlines()
                    for i in l :
                        print(i)
                    histo.close()
                elif (reponse=="3"):
                    ach =""
                    ach = input("Veuillez entrer le nom de l'acheteur")
                    fact = open("factures.txt","r")
                    l = fact.readlines()
                    for i in l :
                        if i.split(" ")[0] == ach :
                            print(i)
                    fact.close()
                elif (reponse=="5"):
                      os._exit(0) #interaction avec le sys des fichiers 
                else:
                    print("Wrong value")
                    
                
                
            time.sleep(self.interval)
            

def accepter_connexions():
    while True:
        try:
            client, client_address = SERVER.accept()
            client.send(bytes("Ecrivez votre nom !","utf8"))
            addresses[client] = client_address
            Thread(target=gerer_client, args=(client,)).start()
        except:
            print("")
            break
        
        


def gerer_client(client):  
    nom = client.recv(BUFSIZ).decode("utf8")
    global prix
    global bidder
    global bidtime
    global auction
    global done
    if 1 :
        
        client.send(bytes('Bienvenue %s! ' % nom, "utf8"))
        tr = TestThreading()
        if (auction):
            client.send(bytes('There is an auction going on :'+reference+"("+str(prix)+")\n", "utf8"))
            client.send(bytes("\n To join the auction use /join ", "utf8"))
        else :
            client.send(bytes("There is no auction going on , please wait for a new auction", "utf8"))
           
        while True:
            
            clients[client] = nom
            msg = client.recv(BUFSIZ)
            if auction:
                if msg == bytes("/join", "utf8") and not joined(nom):
                    add(nom)
                    ms = "%s has joined the auction" % nom
                    diffuserj(bytes(ms, "utf8"))
                    client.send(bytes(''+reference+", current price ("+str(prix)+") ,\n", "utf8"))
                    client.send(bytes("To quit the auction use /q ", "utf8"))
                    print(nom+" has joined the auction"); 
                   
                else :
                    if msg == bytes("/join", "utf8") and joined(nom):
                        client.send(bytes("You are already in the auction! ", "utf8"))
                if joined(nom):
                    try :
                        msgint=int(msg)
                        #print(nom,"placed a new bid:"+msg)
                        if (msgint > prix): #prix valide
                            diffuserj(msg,nom+" made a new bid,the current price is :")
                            
                            if (bidder!=""):
                                histo = open("histo.txt","a")
                                histo.write(strhisto(bidder,prix,"echec\n"))

                                histo.close()
                            
                            prix = msgint
                            bidder = nom
                            bidtime= datetime.now()
                            done = False
                            print("latest bidder : "+nom+"("+str(msgint)+"),"+bidtime.strftime("%H:%M:%S"))
                        else :
                            if msg != bytes("/q", "utf8"):
                                client.send(bytes("wrong bid!", "utf8"))
                    
                    except:
                        if (msg != bytes("/q", "utf8") and msg != bytes("/join", "utf8")):
                            client.send(bytes("wrong input !", "utf8"))
                
                if msg == bytes("/q", "utf8"):
                    if not joined(nom):
                        client.send(bytes("you are not in an auction !", "utf8"))
                    if bidder == nom and joined(nom):
                        client.send(bytes("you can't quit , you are the latest bidder !", "utf8"))
                    if bidder != nom and joined(nom):
                        diffuserj(bytes("%s has left the auction." % nom, "utf8"))
                        print(nom+" has left the auction")
                        client.send(bytes("To join again use /join", "utf8"))
                        quit(nom)
                if not joined(nom) and msg != bytes("/join", "utf8") and msg != bytes("/q", "utf8"):
                    client.send(bytes("you are not in an action !", "utf8"))
            else :
                 client.send(bytes("There is no auction going on , please wait for a new auction", "utf8"))
                
        
                 
               


#diffuser un message a tous les client connectés
def diffuser(msg, prefix=""): 

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
#diffuser un message au clients joins
def diffuserj(msg, prefix=""): 

    for sock in clients:
        if joined(clients[sock]):
            sock.send(bytes(prefix, "utf8")+msg)


#fonction qui retourne True si un client a rejoint la vente
def joined(nom):
    global joins
    for i in joins:
        if i==nom:
            return True
    return False
#fonction qui ajout un client a la liste des client joints
def add(nom):
    global joins
    joins.append(nom)

#l'inverse de add
def quit(nom):
    global joins
    joins.remove(nom)

#fonction pour lire les factures du fichier factures.txt et remplir le
#dictionnaire factures.
def remplirfactures():
    global factures
    fact = open("factures.txt","a")
    fact.close()
    fact = open("factures.txt","r")
    l = fact.readlines()
    fact.close()
    for i in l:
        nom = i.split(" ")[0]
        p = i.split(" ")[-1]
        if p[-1]=="\n":
            p = p[:-1]
        factures[nom]='int(p)'

#fonction pour remplir le fichier factures apres mise a jour 
def remplir():
    global factures
    fact = open("factures.txt","a")
    fact.close()
    fact = open("factures.txt","w")
    for i in factures:
        fact.write(strfact(i,factures[i])+"\n")
    fact.close()

def strfact(a,b):
    ch = a
    for i in range (0,27-len(a)):
        ch=ch+" "
    ch = ch +str(b)
    return ch


def strbien(ref,p1,p2,t,bid):
    ch = ref
    for i in range (0,17-len(ref)):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    

        
    ch = ch+str(p1)
    for i in range (0,12-len(str(p1))):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+str(p2)
    for i in range (0,15-len(str(p2))):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+t
    for i in range (0,15-len(t)):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+bid
    return ch

def strhisto(bid,p,t):
    ch = bidder
    for i in range (0,20-len(bid)):
        ch=ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch + str(p)
    for i in range (0,12-len(str(p))):
        ch = ch+" "
    ch = ch +"|"
    for i in range (0,4):
        ch = ch+" "
    ch = ch+t
    return ch
    
    
    
        



clients = {}
addresses = {}



HOST = '192.168.1.48'
PORT = 50000
BUFSIZ = 1024 #Nombre de bits par message 
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP
SERVER.bind(ADDR)

#SERVER.setblocking(0)
if __name__ == "__main__":
    while True :

        remplirfactures()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        m=menu()   
        
        SERVER.listen(5)
        ACCEPT_THREAD = Thread(target=accepter_connexions)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
