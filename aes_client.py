import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

with open("session.key", "rb") as f:
    session_key = f.read()

iv = os.urandom(16)
plaintext = b"Hello from client!"
padding_len = 16 - len(plaintext) % 16
plaintext += bytes([padding_len]) * padding_len

cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12347))
client_socket.sendall(iv + ciphertext)
client_socket.close()
