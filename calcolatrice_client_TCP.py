import socket,json

HOST = '127.0.0.1' # Indirizzo del server
PORT = 5005      # Porta usata dal server

primoNumero=float(input("inserisci il primo numero: "))
operazione=input("inserisci l'operazione (simbolo): ")
secondoNumero=float(input("inserisci il secondo numero: "))

messaggio={
    "primoNumero": primoNumero,
    "operazione": operazione,
    "secondoNumero":secondoNumero
}

messaggio=json.dumps(messaggio) #converte il dizionario in stringa

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
    sock_service.connect((HOST, PORT))
    sock_service.sendall(messaggio.encode()) # invio direttamente in formato byte
    risultato = sock_service.recv(1024) # il parametro indica la dimensione massima dei dati ricevibili in una sola volta

print(f"{primoNumero} {operazione} {secondoNumero} = {risultato.decode()}")