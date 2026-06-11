Some of the more basis stuff on how wire works



u are able to wrok with a total of 128 individual address using only two bi directional clock for the system the bus line clock scl and then the data (sda)



this is the same thing as the buffer which makes sense meaning that for each of the implementation u are going to have some kind of specific memory in this case around 128 on the stack and then u will be doing things inside of that memory







bein(int sda, int scl) -> sda is the standard data i/o

&#x09;		  scl is the standard clock



void TwoWire::begin(int sda, int scl, uint8\_t address)

{

&#x20;   default\_sda\_pin = sda; 			// sets the default data pin

&#x20;   default\_scl\_pin = scl; 			// sets the basics clock pin

&#x20;   twi\_setAddress(address);			// sets the twi slaves address

&#x20;   twi\_init(sda, scl);				// initalize the overall two wire

&#x20;   twi\_attachSlaveTxEvent(onRequestService);	// set the function called before

&#x09;					// slave write operates

&#x20;   twi\_attachSlaveRxEvent(onReceiveService);	// set function called before a slave

&#x09;					// read operates

&#x20;   flush();

}





for having the begin transmission is probably how the sdat is sent









void TwoWire::beginTransmission(uint8\_t address)

{

&#x20;   transmitting   = 1;		// sending the data

&#x20;   txAddress      = address;	// the address to send the data

&#x20;   txBufferIndex  = 0; 	// buffer index

&#x20;   txBufferLength = 0;		// lenght

}





// basics does it like a unsigned int as address cant be negitive

void TwoWire::beginTransmission(int address)

{

&#x20;   beginTransmission((uint8\_t)address);

}





for ending the overall transmission for the thing



uint8\_t TwoWire::endTransmission(uint8\_t sendStop)

{

&#x20;   int8\_t ret     = twi\_writeTo(txAddress, txBuffer, txBufferLength, sendStop);

&#x20;   txBufferIndex  = 0;

&#x20;   txBufferLength = 0;

&#x20;   transmitting   = 0;

&#x20;   return ret;

}



uint8\_t TwoWire::endTransmission(void)

{

&#x20;   return endTransmission(true);

}



everything makes sense for this one overall







writing everything



I2C\_BUFFER\_LENGTH -> 128 i think





size\_t TwoWire::write(uint8\_t data)

{

&#x20;   if (transmitting)

&#x20;   {

&#x20;       if (txBufferLength >= I2C\_BUFFER\_LENGTH)

&#x20;       {

&#x20;           setWriteError();

&#x20;           return 0;

&#x20;       }

&#x20;       txBuffer\[txBufferIndex] = data;

&#x20;       ++txBufferIndex;

&#x20;       txBufferLength = txBufferIndex;

&#x20;   }

&#x20;   else

&#x20;   {

&#x20;       twi\_transmit(\&data, 1);

&#x20;   }

&#x20;   return 1;

}





ye everyhting make sense for this oen as well ima make the overall thing for the brigness now i htink i should be able to do that



for reading and writing to the teensy

it just check the overall thing on the address and then will just get the value

```

void setDispalyBrightness(uint8\\\\\\\_t brightness){

\\\&#x20; Wire.beginTransmission(DISPALY\\\\\\\_ADDR); 

\\\&#x20; Wire.write(REG\\\\\\\_BRIGHTNESS); // the address 

\\\&#x20; Wire.write(brightness);     // writing the value to the address

\\\&#x20; Wire.endTransmission(); 

}





uint8\\\\\\\_t readDisplayBrightness(){

\\\&#x20; Wire.beginTransmission(DISPALY\\\\\\\_ADDR); 

\\\&#x20; Wire.write(REG\\\\\\\_BRIGHTNESS); 

\\\&#x20; Wire.endTransmission(false);        // make the overall buss active

\\\&#x20; Wire.requestFrom(DISPALY\\\\\\\_ADDR, 1);  // return the overall data for the specific size 

\\\&#x20; if(Wire.available())

\\\&#x20;     return Wire.read();             // reads the overall available



\\\&#x20; return 0xFF;                        // error

}



```



reading and writing the overall image for the thing



basics stuff just copy the image and then writes it into the right buffer

for checking the image will just read it into array cpy it and then compare the overall values



```

void sendImage(uint64\\\\\\\_t image){

\\\&#x20; uint8\\\\\\\_t bytes\\\\\\\[8];



\\\&#x20; // copys the value for the image in the overall bytes

\\\&#x20; memcpy(bytes, \\\\\\\&image, 8);

\\\&#x20; 

\\\&#x20; // being sending hte data

\\\&#x20; Wire.beginTransmission(DISPALY\\\\\\\_ADDR); 

\\\&#x20; Wire.write(REG\\\\\\\_PIXELS);  // finding where to send it

\\\&#x20; // doing the over sided loop cuz of little endian

\\\&#x20; for(int i = 7; i>=0; --i){

\\\&#x20;   Wire.write(bytes\\\\\\\[i]); 

\\\&#x20; }

\\\&#x20; Wire.endTransmission()

}







bool checkPixel(uint64\\\\\\\_t image){

\\\&#x20; 

\\\&#x20; Wire.beginTransmission(DISPALY\\\\\\\_ADDR); 

\\\&#x20; Wire.write(REG\\\\\\\_PIXELS); 

\\\&#x20; Wire.endTransmission(false); // same thing again make it so that the bus is active

\\\&#x20; 

\\\&#x20; Wire.requestFrom(DISPALY\\\\\\\_ADDR, 8); 

\\\&#x20; if(Wire.available() < 8)

\\\&#x20;   return false; 



\\\&#x20; uint8\\\\\\\_t read\\\\\\\[8]; 

\\\&#x20; for(int i = 7; i>=0; --i)

\\\&#x20;   read\\\\\\\[i] = Wire.read();  

\\\&#x20; 

\\\&#x20; uint64\\\\\\\_t rec; 

\\\&#x20; memcpy(\\\\\\\&rec, read, 8); 

\\\&#x20; return (rec == image); 

}



```

