#include <Arduino.h>
/******************************************************************************************
 * Praxistaugliche Blink-LED - ohne Verwendung der delay-Funktion                         *
 * !!! ACHTUNG:  Arduino-IDE: 1. Zeile( #include <Arduino.h> ) entfernen !!!              *
 *                                                                                        *
 * 25.01.2021                                                                             *
 * Uwe Hannen                                                                             *
 * ***************************************************************************************/

#define LED_PIN 12                                      // Pin am Arduino
#define INTERVALL 1000                                  // switchen in Millisekunden

unsigned long int ulTick;                               // globale Variable - Zeitstamp

void setup() {
  pinMode(LED_PIN, OUTPUT);                             // Ausgang initialisieren
  digitalWrite(LED_PIN, LOW);                           // LED ausschalten
  ulTick = INTERVALL;                                   // erste Zeit setzen
}

void loop() {
  if (millis() > ulTick) {                              // Zeit erreicht ?
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));       // ja -> LED switchen
    ulTick = millis() + INTERVALL;                      // und neue Zeit setzen
  }
}
