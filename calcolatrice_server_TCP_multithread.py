#IL SERVER PUO' GESTIRE PIU' CLIENT CONTEMPORANEAMENTE

import socket
import json
from threading import Thread

# Funzione eseguita da ogni thread (un client = un thread)
def ricevi_comandi(sock_service, addr_client): 
    print(f"[+] Connesso a {addr_client}")

    try:
        while True:
            dati = sock_service.recv(1024).decode() #riceve i dati dal client e li decodifica in stringa json
            if not dati:
                break

            data = json.loads(dati) #converte la stringa in dizionario

            a = data["primoNumero"]
            op = data["operazione"]
            b = data["secondoNumero"]

            # Calcolo
            if op == "+":
                risultato = a + b
            elif op == "-":
                risultato = a - b
            elif op == "*":
                risultato = a * b
            elif op == "/":
                risultato = a / b if b != 0 else "Errore: divisione per 0"
            else:
                risultato = "Operazione non valida"

            # Invio risultato
            sock_service.sendall(str(risultato).encode())

    except Exception as e:
        print("Errore:", e)

    finally:
        print(f"[-] Disconnesso {addr_client}")
        sock_service.close() #chiusura del socket una volta inviati i dati o in caso di errore


# Funzione che accetta connessioni e crea thread
def ricevi_connessioni(sock_listen):
    sock_service, address_client = sock_listen.accept() #accetta una nuova connessione
    #una volta accettata la connessione, crea un thread
    try:
        Thread(
            target=ricevi_comandi, #la funzione che deve eseguire il thread
            args=(sock_service, address_client) #parametri della funzione (il socket appena creato al momento dell'accettazione e l'inidirzzo del client)
        ).start() #avvia il thread
    except Exception as e:
        print("Errore thread:", e)


# Funzione principale del server
def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:

        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock_server.bind((indirizzo, porta))
        sock_server.listen(5)

        print(f"Server in ascolto su {indirizzo}:{porta}")

        while True:
            ricevi_connessioni(sock_server)


# MAIN
IP = "127.0.0.1"
PORTA = 5005

"""
ORDINE:
1)avvia_server(): associa un indirizzo al socket e rimane in ascolto
2)ricevi_connessioni(): accetta la richiesta di connessione da parte del client e avvia un thread per la funzione ricevi_comandi
3)ricevi_comandi(): una volta stabilita la connessione, riceve i dati, fa i calcoli e invia il risultato al client
"""
avvia_server(IP, PORTA) 