
import socket
import json
from collections import deque
import numpy as np
q = 2
n = 1
p = 1
position = None


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
        message = client_socket.recv(16600000).decode()
        if message:
            message_json = json.loads(message)
            if message_json["request"] == "play":
                a = moveplayer(message_json["state"])
                #pourri = np.array(message_json["state"]["board"])
                #print(pourri.shape)
                
                client_socket.send(json.dumps(a).encode())
                
            elif message_json["request"] == "ping":
                client_socket.send(json.dumps({"response": "pong"}).encode())
    except Exception as e:
        print("Une erreur s'est :", e)
        
        matrix = np.array(message_json["state"]["board"])
        print(matrix.shape)
        if message_json["state"]["current"] == 1 and shortest_path1(matrix)[0] < shortest_path0(matrix)[0] or message_json["state"]["blockers"][1] ==0:
            client_socket.send(json.dumps({"response": "move","move": {"type": "pawn", "position": [list(shortest_path1(matrix)[1][p])]},"message": "le temps des humains est revolu"}).encode())    
        else:
            client_socket.send(json.dumps({"response": "move","move": {"type": "pawn", "position": [list(shortest_path0(matrix)[1][n])]},"message": "le temps des humains est revolu"}).encode())

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
            print("Une putain d erreur erreur", e)
def moveplayer(etat):
    global position
    global q 
    global n 
    global p
    matrix = np.array(etat["board"])

    try:
        if shortest_path1(matrix)[1][1][1] == 16 and etat["current"] == 0:
                matrix[shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1] - 2] = 4
                matrix[shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1] ] = 4
                position = [[shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1] - 2,shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1]]]


        elif etat["current"] == 0:
                matrix[shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1] + 2] = 4
                matrix[shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1] ] = 4
                position = [[shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1] + 2], [shortest_path1(matrix)[1][1][0] - 1, shortest_path1(matrix)[1][1][1]]]
        
        if etat ["current"] == 0 and shortest_path0(matrix)[0] >= shortest_path1(matrix)[0] and etat["blockers"][0] > 0 and shortest_path1(matrix) !=  (-1, []):
            return  {"response": "move","move": {"type": "blocker", "position": position},"message": "le temps des humains est revolu"}


        elif etat["current"] == 0:
                
            if matrix[shortest_path0(matrix)[1][p][0],shortest_path0(matrix)[1][p][1]] == 1 and etat["current"] ==0   :
                print(matrix[shortest_path0(matrix)[1][p][0],shortest_path0(matrix)[1][p][1]])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path0(matrix)[1][q]) ]},"message": "le temps des humains est revolu"}

                    
            elif etat["current"] ==0  :
                print([list(shortest_path0(matrix)[1][p])])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path0(matrix)[1][p])]},"message": "le temps des humains est revolu"}


        

    
        

        
            
            
        if shortest_path0 == 16 and etat["current"] == 1:
            matrix[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] - 2] = 4
            matrix[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] ] = 4
            position = [[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] - 2],[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] ]]

        elif etat["current"] == 1 :
            matrix[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] + 2] = 4
            matrix[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] ] = 4
            position = [[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] + 2],[shortest_path0(matrix)[1][1][0]+1, shortest_path0(matrix)[1][1][1] ]]

        if etat["current"]== 1 and shortest_path0(matrix)[0] <= shortest_path1(matrix)[0] and etat["blockers"][1] > 0 and shortest_path0(matrix) != (-1,[]):
            return  {"response": "move","move": {"type": "blocker", "position": position},"message": "le temps des humains est revolu"}

        elif etat["current"] == 1:
                
            if matrix[shortest_path1(matrix)[1][p][0],shortest_path1(matrix)[1][p][1]] == 0 and etat["current"] ==1:
                print(matrix[shortest_path1(matrix)[1][p][0],shortest_path1(matrix)[1][p][1]])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path1(matrix)[1][q]) ]},"message": "le temps des humains est revolu"}
                    

            elif etat["current"] == 1 :
                print([list(shortest_path1(matrix)[1][p])])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path1(matrix)[1][p])]},"message": "le temps des humains est revolu"}    
    except Exception as e:  
        print("erreur dans moveplayer", e)
        if matrix[shortest_path1(matrix)[1][p][0],shortest_path1(matrix)[1][p][1]] == 0 and etat["current"] ==1:
                print(matrix[shortest_path1(matrix)[1][p][0],shortest_path1(matrix)[1][p][1]])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path1(matrix)[1][q]) ]},"message": "le temps des humains est revolu"}
                    

        elif etat["current"] == 1 :
                print([list(shortest_path1(matrix)[1][p])])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path1(matrix)[1][p])]},"message": "le temps des humains est revolu"}    
        if matrix[shortest_path0(matrix)[1][p][0],shortest_path0(matrix)[1][p][1]] == 1 and etat["current"] ==0   :
                print(matrix[shortest_path0(matrix)[1][p][0],shortest_path0(matrix)[1][p][1]])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path0(matrix)[1][q]) ]},"message": "le temps des humains est revolu"}

                    
        elif etat["current"] ==0  :
                print([list(shortest_path0(matrix)[1][p])])
                return {"response": "move","move": {"type": "pawn", "position": [list(shortest_path0(matrix)[1][p])]},"message": "le temps des humains est revolu"}
            


    

moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]

def is_valid_move1(matrix, row, col, visited):
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

def shortest_path1(matrix):
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
    path = {(start_row, start_col): None}  # Dictionnaire pour enregistrer les coordonnées du chemin

    while queue:
        row, col, distance = queue.popleft()
        
        if row == 0:  # Atteint le haut de la matrice
            # Reconstruire le chemin le plus court
            shortest_path = []
            current = (row, col)
            while current is not None:
                shortest_path.append(current)
                current = path[current]
            shortest_path.reverse()
            return distance, shortest_path
        
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if is_valid_move1(matrix, new_row, new_col, visited):
                queue.append((new_row, new_col, distance + 1))
                visited[new_row][new_col] = True
                path[(new_row, new_col)] = (row, col)
    
    return -1, []  # Aucun chemin trouvé
moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]

def is_valid_move0(matrix, row, col, visited):
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

def shortest_path0(matrix):
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
    path = {(start_row, start_col): None}  # Dictionnaire pour enregistrer les coordonnées du chemin

    while queue:
        row, col, distance = queue.popleft()
        
        if row == rows - 1:  # Atteint le bas de la matrice
            # Reconstruire le chemin le plus court
            shortest_path = []
            current = (row, col)
            while current is not None:
                shortest_path.append(current)
                current = path[current]
            shortest_path.reverse()
            return distance, shortest_path
        
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if is_valid_move0(matrix, new_row, new_col, visited):
                queue.append((new_row, new_col, distance + 1))
                visited[new_row][new_col] = True
                path[(new_row, new_col)] = (row, col)
    
    return -1, []  # Aucun chemin trouvé



if __name__ == "__main__":
    server_address = ('localhost', 4000)
    subscription_request = {
        "request": "subscribe",
        "port":4000,
        "name": "fun_",
        "matricules": ["12295", "60010"]
    }
    if subscribe_to_server(('localhost', 3000), subscription_request):
        start_server(server_address)
