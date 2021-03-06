#!/usr/bin/env python3

ANZAHL = 3

def hanoi(anzahl, von, temp, ziel):
  if anzahl > 0:
    hanoi(anzahl - 1, von, ziel, temp)
    print(f'Scheibe {anzahl} von {von} nach {ziel}')
    hanoi(anzahl - 1, temp, von, ziel) 

hanoi(ANZAHL, 'A', 'B', 'C')