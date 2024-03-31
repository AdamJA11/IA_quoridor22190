
import json
import socket
adress = ('192.168.1.2', 3000)
request = {
   "request": "subscribe",
   "port": 8888,
   "name": "fun_name_for_the_client",
   "matricules": ["12345", "67890"]
}
with socket.socket() as s:
   s.connect(adress)
   s.send(json.dumps(request).encode())
