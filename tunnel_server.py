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
ifr = struct.pack('16sH', b'tun0', IFF_TUN|IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
os.system("ip addr add 10.0.0.1/24 dev tun0")
os.system("ip link set tun0 up")

srv = socket.socket()
srv.bind(("0.0.0.0",12348))
srv.listen(1)
conn, _ = srv.accept()

login_len = conn.recv(1)[0]
login = conn.recv(login_len)
password_len = conn.recv(1)[0]
password = conn.recv(password_len)
if login != b"jakub" or password != b"devops123":
    conn.sendall(b"NO")
    conn.close()
    exit(1)
conn.sendall(b"OK")

def from_tcp():
    while True:
        size = int.from_bytes(conn.recv(2),"big")
        blob = conn.recv(size)
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
        conn.sendall(len(blob).to_bytes(2,"big") + blob)

threading.Thread(target=from_tcp,daemon=True).start()
threading.Thread(target=from_tun,daemon=True).start()

while True:
    pass
