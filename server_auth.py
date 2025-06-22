from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

with open("nonce.bin", "rb") as f:
    nonce = f.read()

with open("signature.bin", "rb") as sig_file:
    signature = sig_file.read()

try:
    public_key.verify(
        signature,
        nonce,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("Signature is valid. Client is authenticated.")
except Exception:
    print("Invalid signature. Client cannot be trusted.")
