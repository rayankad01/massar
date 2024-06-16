from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os



def encrypt_password(password):
    load_dotenv("../.venv")
    key = os.getenv('ENCRYPTION_KEY')
    cipher_suite = Fernet(key)

    return cipher_suite.encrypt(password.encode())


def decrypt_password(encrypted_password):
    load_dotenv("../.venv")
    key = os.getenv('ENCRYPTION_KEY')
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_password).decode()

