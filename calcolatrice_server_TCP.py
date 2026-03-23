import socket
import json

def risultato(a,op,b):
    if(op=="+"):
        return a+b
    elif(op=="-"):
        return a-b
    elif(op=="*"):
        return a*b
    elif(op=="/"):
        return a/b
    
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

# Creazione della socket del server con il costrutto with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server: #sock_server ascolta, quello per comunicare è sock_client (vedi sotto)
    
    # Binding della socket alla porta specificata
    sock_server.bind((SERVER_IP, SERVER_PORT))
    
    # Metti la socket in ascolto per le connessioni in ingresso
    sock_server.listen()

    print(f"Server in asocolto sulla porta {SERVER_PORT} ...")
    # Loop principale del server
    while True:
        # accetta le connessioni
        sock_service, address_client = sock_server.accept() #accept() ritorna il nuovo socket con cui il server potrà comunicare con il client, e l'indirizzo del client (IP,porta)
        
        with sock_service as sock_client:
            # Leggi i dati inviati dal client
            data = sock_client.recv(1024).decode() #recv() ritorna i dati in byte, encode() li converte in stringa json
            data=json.loads(data) #trasforma la stringa json in un dizionario 
            ris=risultato(data["primoNumero"],data["operazione"], data["secondoNumero"])
            sock_client.sendall(str(ris).encode()) #invia il risultato al client
            print("Risultato inviato al client!")

