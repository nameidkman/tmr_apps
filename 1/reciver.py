import socket

RECIVER_IP = "127.0.0.1"
PORT = 5555
BUFFER_SIZE = 32

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((RECIVER_IP, PORT))

smthing = 0
a = "sss"

while a: 
    data, client = sock.recvfrom(BUFFER_SIZE)
    print(f"REcived {data.decode()} from {client}")
    smthing += 1
    print(smthing)
    if(smthing < 10): 
       continue
    else:
        a = 0
