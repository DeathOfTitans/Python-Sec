import os
import shutil
import hashlib
import cryptography.hazmat.primitives.asymmetric.rsa as rsa
import cryptography.hazmat.primitives.serialization as serialization
import cryptography.hazmat.primitives.asymmetric.padding as padding
import cryptography.hazmat.primitives.hashes as hashes

def gen_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("private_key.pem", "wb") as f:
        f.write(pem_private)
    with open("public_key.pem", "wb") as f:
        f.write(pem_public)

    return private_key, public_key


def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted_data = key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

def decrypt_file(file_path, encrypted_data, key):
    decrypted_data = key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(file_path, "wb") as f:
        f.write(decrypted_data)

def recursive_encrypt(dir, key):
    for root, dirs, files in os.walk(dir):
        for name in files:
            file_path = os.path.join(root, name)
            encrypted_data = encrypt_file(file_path, key)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)

def recursive_decrypt(dir, key):
    for root, dirs, files in os.walk(dir):
        for name in files:
            file_path = os.path.join(root, name)
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            decrypt_file(file_path, encrypted_data, key)

def main():
    private_key, public_key = gen_keys()

    client_dir = os.path.join(os.getcwd(), "Dossier_Client")
    server_dir = os.path.join(os.getcwd(), 'server')
    
    if not os.path.exists(client_dir):
        print("Le dossier 'Dossier_Client' est introuvable.")
        return

    shutil.copytree(client_dir, server_dir)
    recursive_encrypt(client_dir, public_key)

    decrypt = input("Do you want to decrypt the files in Dossier_Client? (yes/no): ")
    if decrypt.lower() == 'yes':
        recursive_decrypt(client_dir, private_key)

if __name__ == "__main__":
    main()