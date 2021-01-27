#include <Arduino.h>

#define DEBUG 1                                       // Seriellen Port ein / aus
#define TOKENS ". _ .. __ . _ ."                      // Ausgabestring, max 39 Zeichen Zeile 20: szBuffer
#define HOLD_POINT 200                                // Wartezeiten in ms
#define HOLD_UNDER 600
#define HOLD_SPACE 300
#define HOLD_NEXT 1000                                // Pause
#define LED_PIN 12                                    // Pin -> LED

void setup() {
  #ifdef DEBUG                                        // Zeile 3 auskommentiert?
    Serial.begin(1200);
    Serial.println("Debug-Mode aktiv!");
  #endif
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  char szBuffer[40];                                  // Ausgabestring
  char* pszLoop = szBuffer;                           // Zeiger auf 1. Zeichen
  char token;                                         // aktuelles Zeichen
  sprintf(szBuffer, "%s", TOKENS);                    // String in Buffer kopieren
  unsigned long int uiHold = 0;                       // Wartezeit
  unsigned long int tick;                             // anstelle von delay
  while (1) {                                         // Endlosschleife starten
    tick = millis();
    if (tick > uiHold) {
      digitalWrite(LED_PIN, LOW);
      token = *pszLoop++;                             // Zeichen holen und Zeiger inkrementieren
      #ifdef DEBUG
        if (token) { Serial.print(token); }           // Endekennung nicht ausgeben
      #endif
      switch (token) {                                // Zeichen auswerten
        case '.':                                     // Punkt ?
          uiHold = tick + HOLD_POINT;                 // Wartezeit setzen
          digitalWrite(LED_PIN, HIGH);                // LED schalten
        break;  
        case '_':
          uiHold = tick + HOLD_UNDER;
          digitalWrite(LED_PIN, HIGH);
        break;  
        case ' ':
          uiHold = tick + HOLD_SPACE;
          digitalWrite(LED_PIN, LOW);
        break;  
        case '\0':                                    // Endekennung
          uiHold = tick + HOLD_NEXT;                  // Pause setzen
          digitalWrite(LED_PIN, LOW);
          pszLoop = szBuffer;                         // Zeiger auf Anfang
          #ifdef DEBUG
            Serial.println();                         // Zeilenschaltung
          #endif
        break;  
      }
    }
  }
}
