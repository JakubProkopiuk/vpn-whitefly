import os
import fcntl
import struct
import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

with open("session.key","rb") as f:
    key = f.read()

def decrypt(blob):
    iv = blob[:16]
    ct = blob[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ct) + decryptor.finalize()
    pad_len = padded[-1]
    return padded[:-pad_len]

tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tun1', IFF_TUN|IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
os.system("ip addr add 10.0.0.2/24 dev tun1")
os.system("ip link set tun1 up")

sock = socket.socket()
sock.connect(("192.168.64.5",12348))

login = b"jakub"
password = b"devops123"
sock.sendall(len(login).to_bytes(1, "big") + login)
sock.sendall(len(password).to_bytes(1, "big") + password)
result = sock.recv(2)
if result != b"OK":
    print("Login failed")
    exit(1)

def from_tcp():
    while True:
        size = int.from_bytes(sock.recv(2),"big")
        blob = sock.recv(size)
        pkt = decrypt(blob)
        os.write(tun, pkt)

def from_tun():
    while True:
        pkt = os.read(tun,2048)
        iv = os.urandom(16)
        pad_len = 16 - (len(pkt)%16)
        padded = pkt + bytes([pad_len])*pad_len
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded) + encryptor.finalize()
        blob = iv + ct
        sock.sendall(len(blob).to_bytes(2,"big") + blob)

threading.Thread(target=from_tcp,daemon=True).start()
threading.Thread(target=from_tun,daemon=True).start()

while True:
    pass
