import socket
import os

nonce = os.urandom(32)

with open("nonce.bin", "wb") as f:
    f.write(nonce)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(1)

conn, addr = server_socket.accept()
conn.sendall(nonce)
conn.close()
server_socket.close()
