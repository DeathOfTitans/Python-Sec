import socket
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Chargement des clés (à remplacer par vos propres clés)
with open("chemin_vers_votre_cle_privee.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

with open("chemin_vers_votre_cle_publique.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Fonctions pour chiffrer et déchiffrer les données
def decrypt(data):
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def encrypt(data):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Fonction de gestion du proxy
def handle_client(client_socket):
    with client_socket as sock:
        # Recevoir les données du client
        data = sock.recv(4096)
        decrypted_data = decrypt(data)

        # Connexion au serveur distant
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect(("adresse_du_serveur", port_du_serveur))
            server_socket.sendall(encrypted_data)

            # Recevoir la réponse du serveur
            server_response = server_socket.recv(4096)
            decrypted_response = decrypt(server_response)

            # Retourner la réponse au client
            sock.sendall(encrypt(decrypted_response))

# Configuration du socket d'écoute
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5020))
server.listen(5)

print("Le proxy est à l'écoute...")

# Boucle principale pour accepter les connexions
try:
    while True:
        client_sock, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock,))
        client_thread.start()
except KeyboardInterrupt:
    print("Arrêt du proxy")

server.close()
