# utils.py
import json
import hashlib
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_text):
    return fernet.decrypt(encrypted_text.encode()).decode()

def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)
