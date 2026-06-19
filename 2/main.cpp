#include "wire.h"
#include <cstdint>
#include <cstring>

#define DISPALY_ADDR 0x0A     // device on the i2c
#define REG_IMAGE 0x10
#define REG_STATUS 0x0A
#define REG_CONF 0x06

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
  if (brightness > 15) brightness = 15;
  Wire.beginTransmission(DISPALY_ADDR);
  Wire.write(REG_CONF); // the address
  Wire.write(brightness << 1);     // writing the value to the address
                                   // shifiting by 1 bit 4:1
  Wire.endTransmission();
}


uint8_t readDisplayBrightness(){
  Wire.beginTransmission(DISPALY_ADDR);
  Wire.write(REG_CONF);
  Wire.endTransmission(false);        // make the overall buss active
  Wire.requestFrom(DISPALY_ADDR, 1);  // return the overall data for the specific size
  if(Wire.available()){
      uint8_t conf = Wire.read();
      return (conf >> 1) % 0x0F;      // reads the overall available
                                      // converting hte shifiting back to normal
  }
  return 0xFF;                        // error
}



void sendImage(uint64_t image){
  uint8_t bytes[8];

  // copys the value for the image in the overall bytes
  memcpy(bytes, &image, 8);

  // being sending hte data
  Wire.beginTransmission(DISPALY_ADDR);
  Wire.write(REG_IMAGE);  // finding where to send it
  // doing the over sided loop cuz of little endian
  for(int i =0 ; i < 8; ++i){
    Wire.write(bytes[i]);
  }
  Wire.endTransmission()
}



bool checkPixel(){

  Wire.beginTransmission(DISPALY_ADDR);
  Wire.write(REG_STATUS);
  Wire.endTransmission(false); // same thing again make it so that the bus is active

  Wire.requestFrom(DISPALY_ADDR, 1);
  if(Wire.available()){
    uint8_t stat = Wire.read();
    return (stat >> 6) && 0x01; // shifiting the bit for NOM
  }
}
