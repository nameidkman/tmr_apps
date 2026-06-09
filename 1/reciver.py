# so basically all that the reciver has to do is recive the array 
# meaning that i will just freaking give it the entire decode string 

import socket   
import struct
import random
from encoder import decode_rle_16bit
from checksum import verify_checksum

RECIVER_IP = ""
PORT = 5555
BUFFER_SIZE = 60465



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((RECIVER_IP, PORT))

smthing = 0
a = "sss"

while a:
    data, client = sock.recvfrom(BUFFER_SIZE)
    
    print(f"\nReceived {len(data)} compressed bytes from {client}")# 1. Receive the raw compressed binary packet
    if verify_checksum(data):
        data = data[:-2]
        smthing+=1
        print(smthing)
        decoded_list = decode_rle_16bit(data)

        print(f"First 5 items: {decoded_list[:100]}")
        if(smthing < 10): 
            continue
        else:
            a = 0
