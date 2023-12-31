#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#define PIN 4
// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(24, PIN, NEO_GRB + NEO_KHZ800);
// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.
void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code
  Serial.begin(9600);
  strip.begin();
  strip.setBrightness(50);
  strip.show(); // Initialize all pixels to 'off'
  initI2c();
}
const int IDLE=0;
const int STARTING=1;
const int PUMPING=2;
const int FINISHED=3;

int state = IDLE;

volatile long pumpStopTime = 0;

void pulsate(uint32_t c, uint8_t wait) {
  strip.setBrightness(1);
  // Set color on all
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
  }
  uint8_t brigthness = 1;
  int increment = 1;
  while (IDLE == state) {
    strip.setBrightness(brigthness);
    strip.show();
    brigthness = brigthness + increment;
    if (50 == brigthness) {
      increment = -1;
    }
    if (1 == brigthness) {
      increment = 1;
    }
    /*
      for(uint16_t i=0; i<strip.numPixels(); i++) {
        strip.setPixelColor(i, c);
        strip.show();
      }
      */
   // Serial.println(brigthness);
    delay(100);
  }
}
// Spins around with given color
void spin(uint32_t c, uint8_t waitXX) {

  uint8_t wait = 60;
  uint8_t finalSpins = 10;
  while (STARTING == state && finalSpins > 0) {
    for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      if (i==0) {
        strip.setPixelColor(strip.numPixels()-1, 0);
      } else {
        strip.setPixelColor(i-1, 0);
      }
      strip.show();
      delay(wait);
      
    }
    if (wait > 10) {
      wait = wait - 10;
    } else {
      finalSpins--;
    }
  }
  if (STARTING == state) {
    // Transit to next state
    state = PUMPING;
  }
}

uint32_t getProgressColor(int pixels, int iteration)
{
  int colorG = (128 / (pixels) * (iteration + 1)) + 128;
  return strip.Color(40, 40, colorG); 
}

void countUp() {
  const long now = millis();
  // Require at least 10 milliseconds to do countUp
  if (now > (pumpStopTime - 10)) {
    // Ups - we have already timed out - bail out!
    state = IDLE;
    return;
  }

  colorWipe(strip.Color(0,   0,   0), 0); // Wipe all colroos
  const int pixels = strip.numPixels();
  const int delayPerIteration = (pumpStopTime - now  - 10) / pixels;  
 
 for (int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    int32_t color = getProgressColor(pixels, i);
    for (int j=0; j< i; j++) {
      strip.setPixelColor(j, color);  
    }
    strip.setPixelColor(i, color);
    strip.show();   
    if (PUMPING != state) { 
      return;
    }
    delay(delayPerIteration);
  }

  state = FINISHED;
}

void initI2c() {
  const int boardAddress = 6;
  Wire.begin(boardAddress);     // join i2c bus with address
  Wire.onReceive(receiveEvent); // register event
}

void loop() {  
  if (IDLE == state) {
    pulsate(strip.Color(0, 255, 0), 50); // Green
  }
  if (STARTING == state) {
    spin(strip.Color(255, 0, 0), 10); // Green
  }
  if (PUMPING == state) {
    countUp();
  }
  if (FINISHED == state) {
   theaterChase(strip.Color(0, 255, 0), 50); 
   theaterChase(strip.Color(0, 255, 0), 50); 
   theaterChase(strip.Color(0, 255, 0), 50); 
   state = IDLE;
  }
}

void receiveEvent(int howMany)
{
  // We need to empty the buffer!
  if (howMany != 5) {
    Serial.println("Garbage - expected 5 bytes, recevied:");
    Serial.println(howMany);
    while (Wire.available()) {
      Wire.read();
    }
    return;
  }
  int garbage1 = Wire.read();
  int garbage2 = Wire.read();
  // Serial.print("Two garbage bytes: ");
  // Serial.print(garbage1);
  // Serial.println(garbage2);
  int command = Wire.read();
  if (65 != command) {
    Serial.print("Unknown command: ");
    Serial.println(command);
    Wire.read();
    Wire.read();
    return;
  }
  int milliseconds = Wire.read();
  milliseconds = milliseconds << 8;
  int lsb = Wire.read();
  milliseconds = milliseconds + lsb;

  pumpStopTime = millis() + milliseconds;

  state = STARTING;
}


/* From example for light below */
// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}
void rainbow(uint8_t wait) {
  uint16_t i, j;
  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;
  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}
//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();
      delay(wait);
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}
//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
      }
      strip.show();
      delay(wait);
      for (uint16_t i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}
// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}