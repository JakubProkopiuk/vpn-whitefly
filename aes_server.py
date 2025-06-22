import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

with open("session.key", "rb") as f:
    session_key = f.read()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12347))
server_socket.listen(1)

conn, addr = server_socket.accept()
data = conn.recv(1024)
conn.close()
server_socket.close()

iv = data[:16]
ciphertext = data[16:]

cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
decryptor = cipher.decryptor()
padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
padding_len = padded_plaintext[-1]
plaintext = padded_plaintext[:-padding_len]

print(f"Received message: {plaintext.decode()}")
