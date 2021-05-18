
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

test = True

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            msg_list.insert(tkinter.END,"The server just crashed")
            
            break


def send():  
    msg = my_msg.get()
    my_msg.set("")  
    client_socket.send(bytes(msg, "utf8"))

def exitc(event=None):
    #client_socket.close()
    scene.quit()



def close_window ():
    
    scene.destroy()


# definition des elements de notre  interface 
scene = tkinter.Tk()
scene.title("Vente aux enchere - Application")

messages_frame = tkinter.Frame(scene)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("name")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)


msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(scene, textvariable=my_msg)
entry_field.bind("<Return>", send) #Return=la clé entrer du clavier #elle déclenche la méthode send
entry_field.pack()
send_button = tkinter.Button(scene, text="Envoyer", command=send)
send_button.pack()
button = tkinter.Button (scene, text = "Quitter", command = close_window)
button.pack()




HOST = '192.168.1.48'
if not HOST:
    HOST= '192.168.1.48'
PORT = 50000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
try:
    client_socket = socket(AF_INET, SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP
    client_socket.connect(ADDR)
    test = True
except :
    print("Serveur est déconnecté")
    test = False
if test :
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()
