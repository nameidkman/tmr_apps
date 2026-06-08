import struct
import random

def encode_rle_16bit(data: list[int]) -> bytes:
    if not data:
        return b""
        
    packed_bytes = bytearray()
    
    current_val = data[0]
    count = 1
    
    for val in data[1:]:
        if val == current_val and count < 255:
            count += 1
        else:
            # '!BH' = 1-byte unsigned count, 2-byte unsigned short value
            packed_bytes.extend(struct.pack('!BH', count, current_val))
            current_val = val
            count = 1
            
    packed_bytes.extend(struct.pack('!BH', count, current_val))
    return bytes(packed_bytes)


def decode_rle_16bit(byte_stream: bytes) -> list[int]:
    decoded_array = []
    index = 0
    stream_length = len(byte_stream)
    
    while index < stream_length:
        count, val = struct.unpack('!BH', byte_stream[index:index+3])
        decoded_array.extend([val] * count)
        index += 3
        
    return decoded_array
