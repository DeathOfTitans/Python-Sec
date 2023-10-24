import socket

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #AF_INT = ipv4

host = socket.gethostname() #modify for target ip
port = 666 #modify for target port

server.bind((host,port))
print(f"Running UDP server on {host}:{port}")
while True:
        message, address = server.recvfrom(1024)
        print(f"Received UDP from {address}:{message}")
        message = "Hello\r\n"
        server.sendto(message.encode('ascii'),address)
        print(f"Sent UDP {address}")