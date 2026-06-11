#include "wire.h"
#include <cstdint>
#include <cstring>


#define DISPALY_ADDR 0x0A     // device on the i2c 
#define REG_BRIGHTNESS 0x00    
#define REG_PIXELS 0x01


void sendImage(uint64_t image); 
bool checkPixel(uint64_t image); 
void setDispalyBrightness(uint8_t brightness); 
uint8_t readDisplayBrightness(); 



void setup(){


  // this sets up the overall i2c things 
  // sda -> 18 
  // scl -> 19 
  // the overall thing are setup inside of the function which then leads 
  // to twi_init which then leads to a 
  // simple digital write whihc just puts both of them into high
  Wire.begin(); 
  Wire.setClock(400000); // 400hz fast mode
  
  // define image and brightness
  uint64_t image; 
  uint8_t brightness; 

  sendImage(image); 
  checkPixel(image); 
  setDispalyBrightness(brightness); 
  readDisplayBrightness(); 


}



void loop(){
}




// Write display brightness
// on the address REG_BRIGHTNESS
void setDispalyBrightness(uint8_t brightness){
  Wire.beginTransmission(DISPALY_ADDR); 
  Wire.write(REG_BRIGHTNESS); // the address 
  Wire.write(brightness);     // writing the value to the address
  Wire.endTransmission(); 
}


uint8_t readDisplayBrightness(){
  Wire.beginTransmission(DISPALY_ADDR); 
  Wire.write(REG_BRIGHTNESS); 
  Wire.endTransmission(false);        // make the overall buss active
  Wire.requestFrom(DISPALY_ADDR, 1);  // return the overall data for the specific size 
  if(Wire.available())
      return Wire.read();             // reads the overall available

  return 0xFF;                        // error
}



void sendImage(uint64_t image){
  uint8_t bytes[8];

  // copys the value for the image in the overall bytes
  memcpy(bytes, &image, 8);
  
  // being sending hte data
  Wire.beginTransmission(DISPALY_ADDR); 
  Wire.write(REG_PIXELS);  // finding where to send it
  // doing the over sided loop cuz of little endian
  for(int i = 7; i>=0; --i){
    Wire.write(bytes[i]); 
  }
  Wire.endTransmission()
}



bool checkPixel(uint64_t image){
  
  Wire.beginTransmission(DISPALY_ADDR); 
  Wire.write(REG_PIXELS); 
  Wire.endTransmission(false); // same thing again make it so that the bus is active
  
  Wire.requestFrom(DISPALY_ADDR, 8); 
  if(Wire.available() < 8)
    return false; 

  uint8_t read[8]; 
  for(int i = 7; i>=0; --i)
    read[i] = Wire.read();  
  
  uint64_t rec; 
  memcpy(&rec, read, 8); 
  return (rec == image); 
}
