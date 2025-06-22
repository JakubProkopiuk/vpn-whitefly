import socket
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open("client_public.pem", "rb") as f:
    client_public_key = serialization.load_pem_public_key(f.read())

session_key = os.urandom(32)

with open("session.key", "wb") as f:
    f.write(session_key)

encrypted_key = client_public_key.encrypt(
    session_key,
    padding.PKCS1v15()
)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12346))
server_socket.listen(1)

conn, addr = server_socket.accept()
conn.sendall(encrypted_key)
print("Session key sent to client.")
conn.close()
server_socket.close()
