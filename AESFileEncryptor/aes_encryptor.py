import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt_file(file_path, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(file_path, 'rb') as f:
        data = f.read()
    padded_data = pad(data)
    ciphertext = cipher.encrypt(padded_data)

    with open(file_path + ".enc", 'wb') as f:
        f.write(salt + iv + ciphertext)

def decrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        ciphertext = f.read()

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ciphertext).rstrip(b" ")

    original_path = file_path.replace(".enc", ".dec")
    with open(original_path, 'wb') as f:
        f.write(plaintext)
