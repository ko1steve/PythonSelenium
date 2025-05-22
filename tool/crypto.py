import os
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def get_cipher():
    key = os.getenv("Python Encrypt Key")
    cipher = Fernet(key)
    return cipher

def encrypt(t):
    cipher = get_cipher()
    return cipher.encrypt(t.encode())

def decrypt(encrypted):
    cipher = get_cipher()
    return cipher.decrypt(encrypted).decode()
