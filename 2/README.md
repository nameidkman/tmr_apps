Some of the more basic stuff on how Wire works:

You are able to work with a total of 128 individual addresses using only two bidirectional lines for the system:
the bus line clock SCL and the data line SDA.

This is the same thing as the buffer, which makes sense — meaning that for each implementation you will have some kind of specific memory, in this case around 128 bytes on the stack, and then you will be doing things inside that memory.

begin(int sda, int scl)
sda is the standard data I/O
scl is the standard clock


for the main begin 
```
void TwoWire::begin(int sda, int scl, uint8_t address)
{
    default_sda_pin = sda;                 // sets the default data pin
    default_scl_pin = scl;                 // sets the default clock pin
    twi_setAddress(address);               // sets the TWI slave address
    twi_init(sda, scl);                    // initialize the two-wire interface
    twi_attachSlaveTxEvent(onRequestService); // function called before slave write
    twi_attachSlaveRxEvent(onReceiveService); // function called before slave read
    flush();
}
```

for how the teensy will overall do teh transmission for the thing
```
void TwoWire::beginTransmission(uint8_t address)
{
    transmitting   = 1;        // sending data
    txAddress      = address;  // address to send to
    txBufferIndex  = 0;        // buffer index
    txBufferLength = 0;        // length
}

void TwoWire::beginTransmission(int address)
{
    beginTransmission((uint8_t)address);
}

```

how the endTransmission is happening for the thing 
```
void TwoWire::beginTransmission(uint8_t address)
{
    transmitting   = 1;        // sending data
    txAddress      = address;  // address to send to
    txBufferIndex  = 0;        // buffer index
    txBufferLength = 0;        // length
}

void TwoWire::beginTransmission(int address)
{
    beginTransmission((uint8_t)address);
}
```
writing data 
```
size_t TwoWire::write(uint8_t data)
{
    if (transmitting)
    {
        if (txBufferLength >= I2C_BUFFER_LENGTH)
        {
            setWriteError();
            return 0;
        }
        txBuffer[txBufferIndex] = data;
        ++txBufferIndex;
        txBufferLength = txBufferIndex;
    }
    else
    {
        twi_transmit(&data, 1);
    }
    return 1;
}
```






