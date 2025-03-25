import os  
from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from getpass import getpass

def get_salt():
    salt_path = "encryption/salt.bin"
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
    return urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(file_path, password):
    key= generate_key_from_password(password)
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        data = file.read()
        

    encrypted_data = fernet.encrypt(data)

    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted_data)

    print("✅ File eecrypted using password!")

def decrypt_file(file_path, password):
    key= generate_key_from_password(password)
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    output_path = file_path.replace(".enc","")

    with open(output_path, "wb") as file:
        file.write(decrypted_data)

    print("✅ File decrypted using password!")

#Test(CLI)

if __name__ == "__main__":
    choice = input("🔐 (E)ncrypt or (D)ecrypt? ").lower()
    file=input("📂 Enter file path: ")
    password = getpass("🔑 Enter your password: ")

    if choice == "e":
        encrypt_file(file, password)
    elif choice == "d":
        decrypt_file(file, password)
    else :
        print("❌ Invalid choice.")
    