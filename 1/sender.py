import socket   


TARGET_IP = "127.0.0.1"
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 
sock.sendto("baa".encode(), (TARGET_IP, PORT))
