import socket   
import struct
import random
import time 


from encoder import encode_rle_16bit
PORT = 5555
BROADCAST_IP = "255.255.255.255"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


while True: 
    a = []
    for _ in range(100):
        a.append(random.getrandbits(16))

    compressed_bytes = encode_rle_16bit(a)


    print(f"Original Array Length: {len(a)}")
    print(f"Compressed Bytes Size: {len(compressed_bytes)} bytes")

    print("Sample of Original:", a[:100])
    sock.sendto(compressed_bytes, (BROADCAST_IP, PORT))
    time.sleep(1)
