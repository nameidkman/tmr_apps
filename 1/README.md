The first thing which i wanted to work on was the overall encoder and a decoder for the data 

this is the only way i would be able to make a bit of security happen and at the same time have it working nicely 

for the encoder and decoder i just made a simple rli it works as converting everything during the runtime to specific encoded byte 

and then there is a decoder for the reciver the other thing is that it also helps with a bit of memory which is nice





the overall structure for the encode is like this

you feed a list of data into the encode and then it will feed a list of 16 bit integers out



``` python code (encoder) 

encode_rle_16bit(data: list[int]) -> bytes

decode_rle_16bit(byte_stream: bytes) -> list[int]

```

&#x20;



NOw working with the single transmission what i ended up looking into is the DHCP protocol where the dhcp decivs ur ip and then it send a 

broadcasting to the overall every single computer connected on the server. The way this works is that you have the overall 255.255.255.255

which is hard set value for overall network in a dhcp protocol. i will be looking into this a bit more but basically how it works is that 

it will send the data as a limited overall sequence to everything that is connected onto the sever. 



``` python (how i set up the socket constraints

sock = socket.socket(socket.AF\_INET, socket.SOCK\_DGRAM); 

sock.setsockopt(socket.SOL\_SOCKET, socket.SO\_BROADCAST, 1)

```



For check the integrity for the data what i ended up doing is implementing a simple check sum for the overall thing which just 

make a checksum for a some kind of bytes and then it check if that works out and if that does then it goes one and gets it to work  





``` python (checksum)

calculate\_checksum(data: bytes) -> int

verify\_checksum(packet: bytes) -> bool

```

