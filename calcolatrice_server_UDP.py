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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))
print(f"Server in asocolto sulla porta {SERVER_PORT} ...")
while True:
    data, mittente= sock.recvfrom(1024)
    if not data:
        break
    data=data.decode() #da byte vengono trasformati in stringa
    data=json.loads(data) #trasforma la stringa in un dizionario 
    primo_numero=data["primoNumero"]
    secondo_numero=data["secondoNumero"]
    operazione=data["operazione"]

    sock.sendto(str(risultato(primo_numero,operazione,secondo_numero)).encode(), mittente)
    print("Risultato inviato al client!")


