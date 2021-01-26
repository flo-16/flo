#include <Arduino.h>            // Achtung: Arduino-IDE: Diese Zeile auskommentieren !!! 

/******************************************************************************************
 * Snippet : Serieller Output - Text und Zahlen gemischt ausgeben                                 *
 *                                                                                        *
 * 26.01.2021                                                                             *
 * Uwe Hannen                                                                             *
 * ***************************************************************************************/

#define INTERVALL 1000                                  
#define CHAR_LENGTH 20                                  // Zeichenbreite

void setup() {
  Serial.begin(1200);
}

void loop() {
  static unsigned int uiCounter = 0;
  char szBuffer[CHAR_LENGTH];
  const char *szMsg = "Ein Text";
  if (millis() / INTERVALL > uiCounter) {               // delay - Ersatz
    sprintf(szBuffer, "%-14s%6i", szMsg, uiCounter++);  // Puffer füllen 14 + 6 = 20 !!!
    Serial.println(szBuffer);                           // und Ausgabe
  }
}