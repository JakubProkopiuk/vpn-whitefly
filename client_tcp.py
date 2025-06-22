import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

nonce = client_socket.recv(256)

with open("received_nonce.bin", "wb") as f:
    f.write(nonce)

client_socket.close()
