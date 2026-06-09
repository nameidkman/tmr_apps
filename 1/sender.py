import socket   
import struct
import random
import time 

from checksum import calculate_checksum
from encoder import encode_rle_16bit


BROADCAST_IP = "255.255.255.255"
PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)



while True: 
    a = []
    for _ in range(100):
        a.append(random.getrandbits(16))

    compressed_bytes = encode_rle_16bit(a)


    print(f"Original Array Length: {len(a)}")
    print(f"Compressed Bytes Size: {len(compressed_bytes)} bytes")

    checksum = calculate_checksum(compressed_bytes)
    checksum_bytes = bytes([checksum >> 8, checksum & 0xFF])
    transmitted_packet = compressed_bytes + checksum_bytes
    print("Sample of Original:", a[:100])
    sock.sendto(transmitted_packet, (BROADCAST_IP, PORT))
    time.sleep(1)
