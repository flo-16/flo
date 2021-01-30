#include <Arduino.h>

#define SERIAL_SPEED 9600
const uint8_t LED_PIN = 12;

void setup() {
  Serial.begin(SERIAL_SPEED);
  Serial.println("Serieller Port aktiv!");

  pinMode(LED_PIN, OUTPUT);
  unsigned long long tick;                             
  unsigned int uiCount = 0;
  char szDummys[][12] = {"Willibald", "Isolde"};
  char buffer[40];
  while(1) {                                      
    tick = millis();
    if(tick / 1000 > uiCount) {
      sprintf(buffer, "%6u. %-14s%4lu", uiCount + 1, szDummys[uiCount % 2], random(1000));
      Serial.println(buffer);
      digitalWrite(LED_PIN, uiCount % 2);
      uiCount++;
    }
  }
}

void loop() {
}
