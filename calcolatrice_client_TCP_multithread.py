# Client TCP multithread che invia NUM_WORKERS richieste contemporanee al server
# Ogni richiesta contiene un'operazione aritmetica da eseguire

import socket         # Per la comunicazione di rete
import json           # Per la codifica/decodifica JSON
import random         # Per generare numeri casuali
import time           # Per misurare i tempi di esecuzione
import threading      # Per gestire l'esecuzione parallela (multithreading)

# --- Configurazione ---
HOST = "127.0.0.1"           # IP del server
PORT = 5005                # Porta del server (assicurarsi che il server stia ascoltando su questa)
NUM_WORKERS = 15            # Numero di richieste (thread) da inviare in parallelo
OPERAZIONI = ["+", "-", "*", "/"]  # Lista delle operazioni consentite

#1 funzione che verrà eseguita in ogni thread
def genera_richieste(address, port):
    #2 creazione del socket con il costrutto with
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))  # Connessione al server

        #3 Genera tre numeri casuali, dei quali uno (da 0 a 3) è l'indice posizionale per accedere all'operazione da fare
        primoNumero = random.randint(0, 100)
        operazione = OPERAZIONI[random.randint(0, 3)]  # Scegli operazione a caso (tra le prime 4)
        secondoNumero = random.randint(0, 100)

        #4 creazione del dizionario con i vallori
        messaggio = {
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }
        # casting del dizionario in una stringa json
        messaggio = json.dumps(messaggio)

        ##5 invio dei dati al server (prima di essere inviati devono essere codificati in byte (.encode()))
        sock_service.sendall(messaggio.encode("UTF-8"))

        #6 Fa partire il tempo di esecuzione del thread
        start_time_thread = time.time()

        #7 riceve la risposta del server
        data = sock_service.recv(1024)

    #8 stoppa il timer di esecuzione
    end_time_thread = time.time()
    #stampa il risultato
    print("Received: ", data.decode())
    #stampa il nome del thread e la sua durata di esecuzione
    print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)

# --- Punto di ingresso del programma ---
if __name__ == "__main__":
    start_time = time.time()  # Tempo di inizio totale

    #9 crea 15 thread che eseguono la funzione genera_richieste (NUM_WORKERS=15)
    threads = [
        threading.Thread(target=genera_richieste, args=(HOST, PORT))
        for _ in range(NUM_WORKERS)
    ]

    #10 i 15 thread presenti nella lista vengono avviati in parallelo
    [thread.start() for thread in threads]

    #11 attende la fine dell'esecuzione di tutti i thread
    [thread.join() for thread in threads]

    end_time = time.time()  # Tempo di fine totale

    # Stampa il tempo complessivo impiegato per eseguire tutte le richieste
    print("Tempo totale impiegato = ", end_time - start_time)