
import socket
import sys
import time
import json

import socket
import sys
import time
import json

def subscribe_to_server(server_address, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(server_address)
            s.sendall(json.dumps(request).encode())
            response = s.recv(2048).decode()
            response_json = json.loads(response)
            if response_json["response"] == "ok":
                print("Inscription réussie.")
                return True
            else:
                print("Erreur lors de l'inscription:", response_json.get("error", "Erreur inconnue"))
                return False
        except Exception as e:
            print("Erreur lors de la connexion au serveur:", e)
            return False

def handle_client(client_socket):
    # ne pas oublier de rajouter un while true et un timeout 
    try:
        message = client_socket.recv(1024).decode()
        if message:
            message_json = json.loads(message)
            print("Reçu:", message_json)
            if message_json["request"] == "ping":
                client_socket.send(json.dumps({"response": "pong"}).encode())
    except Exception as e:
        print("Une erreur s'est produite lors du traitement du message du client:", e)

def start_server(server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(server_address)
            s.listen()
            print("Serveur en attente de connexions...")
            
            while True:
                client_socket, client_address = s.accept()
                print("Connexion établie avec:", client_address)
                handle_client(client_socket)
        except Exception as e:
            print("Une erreur s'est produite lors de l'exécution du serveur:", e)

if __name__ == "__main__":
    server_address = ('localhost', 4000)
    subscription_request = {
        "request": "subscribe",
        "port": 4000,  # Changer le port du serveur ici
        "name": "fun_name_for_the_client",
        "matricules": ["12345", "67890"]
    }
    if subscribe_to_server(('localhost', 3000), subscription_request):
        start_server(server_address)