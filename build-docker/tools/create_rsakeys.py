import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


def generate_key(public_exponent=65537, key_size=2048) -> RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=public_exponent, key_size=key_size)


def save_keys(key: RSAPrivateKey, path: str = "") -> None:
    paths = {'private': 'signer_key.pem', 'public': 'signer.pem'}

    if path:
        os.makedirs(path, exist_ok=True)
        paths['private'] = os.path.join(path, paths['private'])
        paths['public'] = os.path.join(path, paths['public'])

    with open(paths['private'], 'wb') as f:
        f.write(key.private_bytes(encoding=serialization.Encoding.PEM,
                                  format=serialization.PrivateFormat.PKCS8,
                                  encryption_algorithm=serialization.NoEncryption()))

    with open(paths['public'], 'wb') as f:
        f.write(key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))


if __name__ == '__main__':
    private_key = generate_key()
    out_path = sys.argv[1] if len(sys.argv) > 1 else "/srv/praktomat/mailsign"
    save_keys(private_key, path=out_path)
