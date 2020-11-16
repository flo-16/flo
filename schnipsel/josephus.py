#!/usr/bin/env python3
from collections import deque
"""
Josephus-Problem(Wikipedia):
Das Josephus-Problem oder die Josephus-Permutation ist ein theoretisches Problem aus der Informatik oder Mathematik.
Es werden nummerierte Objekte im Kreis angeordnet; dann wird, beginnend mit der Nummer, jedes n-te Objekt entfernt,
wobei der Kreis immer wieder geschlossen wird.
"""

KANDIDATEN = 40
SELECTOR = 10

kandidaten = [(number) for number in range(1, KANDIDATEN + 1)]
quere = deque(kandidaten)
kandidaten.clear()
loop = 0
while quere:
    select = quere.popleft()
    loop += 1
    if loop % SELECTOR:
        quere.append(select)
    else:
        kandidaten.append(select)

print(kandidaten)