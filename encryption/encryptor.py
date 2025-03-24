from cryptography.fernet import Fernet
import os

# Generate and save a key (only once)
def generate_key():
    key = Fernet.generate_key()
    with open("encryption/secret.key", "wb") as key_file:
        key_file.write(key)

# Load the saved key
def load_key():
    return open("encryption/secret.key", "rb").read()

# Encrypt a file
def encrypt_file(file_path):
    key = load_key()
    f = Fernet(key)

    with open(file_path, "rb") as file:
        data = file.read()

    encrypted_data = f.encrypt(data)

    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted_data)

    print("✅ File encrypted successfully!")

# Decrypt a file
def decrypt_file(file_path):
    key = load_key()
    f = Fernet(key)

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    original_file = file_path.replace(".enc", "")
    with open(original_file, "wb") as file:
        file.write(decrypted_data)

    print("✅ File decrypted successfully!")


generate_key()
encrypt_file("my_secret.txt")
decrypt_file("my_secret.txt.enc")
