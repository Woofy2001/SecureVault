import os  
from base64 import urlsafe_b65encode 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from getpass import getpass

def get_salt():
    salt_path = "encrptions/salt.bin"
    if not os.path.exists(salt_path):
        salt = os.urandom(16)
        with open(salt_path,"wb") as f:
            f.write(salt)
        
    else:
        with open(salt_path, "rb") as f:
            salt = f.read()
    return salt 

def generate_key_from_password(password: str) -> bytes:
    salt= get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return urlsafe_b65encode(kdf.derive(password.encode()))