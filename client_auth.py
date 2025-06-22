from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

with open("received_nonce.bin", "rb") as f:
    nonce = f.read()

signature = private_key.sign(
    nonce,
    padding.PKCS1v15(),
    hashes.SHA256()
)

with open("signature.bin", "wb") as sig_file:
    sig_file.write(signature)
