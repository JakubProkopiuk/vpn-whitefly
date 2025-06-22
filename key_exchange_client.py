import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open("client_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12346))

encrypted_key = client_socket.recv(256)
client_socket.close()

session_key = private_key.decrypt(
    encrypted_key,
    padding.PKCS1v15()
)

with open("session.key", "wb") as f:
    f.write(session_key)

print(f"Session key saved, {len(session_key)} bytes.")
