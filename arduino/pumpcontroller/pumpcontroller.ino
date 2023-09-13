#include <Arduino_BuiltIn.h>
#include <Wire.h>

const int NUMBER_OF_PUMPS = 8;
long timeouts[NUMBER_OF_PUMPS]{};

// Board 1 has address 4, board 2 has address 5
void setup() {
  const int boardAddress = 4;
  Wire.begin(boardAddress);     // join i2c bus with address
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output

  for (int i=0; i<NUMBER_OF_PUMPS; i++) {
    const int pumpNumber = i+1;
    pinMode(pumpNumber+1, OUTPUT);
    stopPump(pumpNumber);
  }
  
  Serial.println("Waiting for master");
}

void loop() {
  delay(10);
  stopPumpIfTimeout();
}

void stopPumpIfTimeout() {
  const long now = millis();
  for (int i=0; i<NUMBER_OF_PUMPS; i++) {
    if (timeouts[i] && timeouts[i] < now) {
      stopPump(i+1);
      timeouts[i] = 0;
    }
  }
}

void startPump(int pumpNumber) {
  // Pumps are connected to pumpNumber + 1, i.e. pump1 is on PIN 2
  digitalWrite(pumpNumber+1, LOW);
  Serial.print("Starting pump ");
  Serial.println(pumpNumber);
}

void stopPump(int pumpNumber) {
  digitalWrite(pumpNumber+1, HIGH);
  Serial.print("Stopping pump ");
  Serial.println(pumpNumber);
}

void startTimer(int pumpNumber, int milliseconds) {
  const long now = millis();
  timeouts[pumpNumber-1] = now + milliseconds;
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
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
  int pumpNumber = Wire.read();
  int milliseconds = Wire.read();
  milliseconds = milliseconds << 8;
  int lsb = Wire.read();
  milliseconds = milliseconds + lsb;

  Serial.print("Pump number ");
  Serial.print(pumpNumber);
  Serial.print(": ");
  Serial.print(milliseconds);
  Serial.println("ms");

  startPump(pumpNumber);
  startTimer(pumpNumber, milliseconds);  
}
