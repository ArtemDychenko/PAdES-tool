from hashlib import sha256

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

RSA_KEY_SIZE = 4096


def get_pin_from_user():
    pin = input("Enter a PIN for private key: ")

    while input("Confirm PIN: ") != pin:
        print("PINs do not match. Please try again.")
        pin = input("Enter a PIN for private key: ")

    return pin


private_key = rsa.generate_private_key(
    public_exponent=65537,  # industry standard
    key_size=RSA_KEY_SIZE,
)

pin = get_pin_from_user()
pin_hash = sha256(pin.encode()).digest()

with open("private-key.pem", "wb") as f:
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(pin_hash),  # OpenSSL backend uses 'aes-256-cbc' as BestAvailableEncryption
    )
    f.write(pem)

public_key = private_key.public_key()

with open("public-key.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
