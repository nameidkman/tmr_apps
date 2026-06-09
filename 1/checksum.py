
def calculate_checksum(data: bytes) -> int:
    """Calculates the 16-bit Internet Checksum for a given block of data."""
    # Pad with a zero byte if the data has an odd length
    if len(data) % 2 == 1:
        data += b'\x00'
    
    total = 0
    
    # Process data in 16-bit (2-byte) chunks
    for i in range(0, len(data), 2):
        # Combine two bytes into a single 16-bit word (Big-Endian)
        word = (data[i] << 8) + data[i+1]
        total += word
    
    # Fold 32-bit sum into 16 bits (carry-overs wrap around)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
        
    # Take the 1's complement (flip the bits) and mask to 16 bits
    checksum = ~total & 0xFFFF
    return checksum


def verify_checksum(packet: bytes) -> bool:
    """Verifies the packet. Returns True if data is intact."""
    total = 0
    
    # Sum up all 16-bit words, including the checksum field
    for i in range(0, len(packet), 2):
        word = (packet[i] << 8) + packet[i+1]
        total += word
        
    # Fold carry bits
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
        
    # If the data is correct, the final sum must be 0xFFFF
    return (total & 0xFFFF) == 0xFFFF


