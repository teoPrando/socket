import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

primoNumero=float(input("inserisci il primo numero: "))
operazione=input("inserisci l'operazione (simbolo): ")
secondoNumero=float(input("inserisci il secondo numero: "))

messaggio={
    "primoNumero": primoNumero,
    "operazione": operazione,
    "secondoNumero":secondoNumero
}

messaggio=json.dumps(messaggio) #converte il dizionario in stringa
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(messaggio.encode(), (SERVER_IP, SERVER_PORT)) #invia la stringa al server
    risultato= sock.recv(1024) #riceve la risposta dal client

print(f"{primoNumero} {operazione} {secondoNumero} = {risultato.decode()}")