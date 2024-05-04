
import socket
import json
from collections import deque
Verif1 = False
PAWN1 = 0
PAWN2 = 1
EMPTY_PAWN = 2
EMPTY_BLOCKER = 3
BLOCKER = 4
IMP = 5

def subscribe_to_server(server_address, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(server_address)
            s.sendall(json.dumps(request).encode())
            response = s.recv(2048).decode()
            response_json = json.loads(response)
            if response_json["response"] == "ok":
                return True
            else:
                print("Erreur lors de l'inscription:", response_json.get("error", "Erreur inconnue"))
                return False
        except Exception as e:
            print("Erreur lors de la connexion au serveur:", e)
            return False

def handle_client(client_socket):
    try:
        message = client_socket.recv(16600).decode()
        if message:
            message_json = json.loads(message)
            if message_json["request"] == "play":
                #moveplayer(message_json)
                print(message_json["state"]["current"])
                
                
                the_move_played = {"type": "blocker","position": [[1,8],[1,10]]  }
                a = {"response": "move","move": the_move_played,"message": "Fun message"}
                client_socket.send(json.dumps(a).encode())
                
            elif message_json["request"] == "ping":
                client_socket.send(json.dumps({"response": "pong"}).encode())
    except Exception as e:
        print("Une erreur s'est produite:", e)

def start_server(server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(server_address)
            s.listen()
            while True:
                client_socket, client_address = s.accept()
                print("Connexion avec", client_address)
                with client_socket:
                    handle_client(client_socket)
        except Exception as e:
            print("Une erreur", e)
def moveplayer(etat):
    if Verif1 == False:
        etatprecedent = etat
        reponse = {"response": "move","move":  {"type": "pawn","position": [[0,8]] },"message": "Fun message"}
        return 
    
import numpy as np

from collections import deque

moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]

def is_valid_move(matrix, row, col, visited):
    rows = len(matrix)
    cols = len(matrix[0])
    if not (0 <= row < rows and 0 <= col < cols):
        return False
    if visited[row][col]:
        return False
    if matrix[row][col] == 4:
        return False
    # Vérifie si la case contient un chiffre 2 et qu'aucune case adjacente ne contient de 4
    if matrix[row][col] == 2:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < rows and 0 <= adj_col < cols and matrix[adj_row][adj_col] == 4:
                return False
    return True

def shortest_path(matrix):
    # Taille de la matrice
    rows = len(matrix)
    cols = len(matrix[0])

    # Recherche de la première occurrence de 0 dans la matrice
    start_row, start_col = None, None
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0:
                start_row, start_col = i, j
                break
        if start_row is not None:
            break

    if start_row is None or start_col is None:
        print("Aucun zéro trouvé dans la matrice.")
        return -1
    
    visited = [[False] * cols for _ in range(rows)]
    
    queue = deque([(start_row, start_col, 0)])  # (row, col, distance)
    visited[start_row][start_col] = True
    
    while queue:
        row, col, distance = queue.popleft()
        
        if row == rows - 1:  # Atteint le bas de la matrice
            return distance
        
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(matrix, new_row, new_col, visited):
                queue.append((new_row, new_col, distance + 1))
                visited[new_row][new_col] = True
    
    return -1  # Aucun chemin trouvé
def is_valid_movefor1(matrix, row, col, visited):
    rows = len(matrix)
    cols = len(matrix[0])
    if not (0 <= row < rows and 0 <= col < cols):
        return False
    if visited[row][col]:
        return False
    if matrix[row][col] == 4:
        return False
    # Vérifie si la case contient un chiffre 2 et qu'aucune case adjacente ne contient de 4
    if matrix[row][col] == 2:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < rows and 0 <= adj_col < cols and matrix[adj_row][adj_col] == 4:
                return False
    return True

def shortest_pathfor1(matrix):
    # Taille de la matrice
    rows = len(matrix)
    cols = len(matrix[0])

    # Recherche de la première occurrence de 1 dans la matrice
    start_row, start_col = None, None
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                start_row, start_col = i, j
                break
        if start_row is not None:
            break

    if start_row is None or start_col is None:
        print("Aucun un trouvé dans la matrice.")
        return -1
    
    visited = [[False] * cols for _ in range(rows)]
    
    queue = deque([(start_row, start_col, 0)])  # (row, col, distance)
    visited[start_row][start_col] = True
    
    while queue:
        row, col, distance = queue.popleft()
        
        if row == 0:  # Atteint le haut de la matrice
            return distance
        
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if is_valid_movefor1(matrix, new_row, new_col, visited):
                queue.append((new_row, new_col, distance + 1))
                visited[new_row][new_col] = True
    
    return -1  # Aucun chemin trouvé


if __name__ == "__main__":
    server_address = ('localhost', 4000)
    subscription_request = {
        "request": "subscribe",
        "port": 4000,
        "name": "fun_name_for_the_client",
        "matricules": ["12345", "67890"]
    }
    if subscribe_to_server(('localhost', 3000), subscription_request):
        start_server(server_address)
