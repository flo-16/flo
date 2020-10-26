#!/usr/bin/env python3
import sys

sailors = 0
try:
    sailors = int(sys.argv[1])
    if sailors < 3 or sailors > 7:
        sailors = 5
except: 
    sailors = 5
parts = [ (0) for _ in range(sailors) ]

nuts = 0; rest = 0 
while 1:
    nuts += 1
    rest = nuts
    stop = False
    for loop in range(sailors):
        if rest % sailors != 1:
            break        
        parts[loop] = rest // sailors
        rest = rest - parts[loop] - 1
        stop = loop == sailors - 1
    if stop and not (rest % sailors):
        break 

print("\nLösung mit {:d} Seeleuten".format(sailors))
print("\n{:>8s}{:>8s}{:>8s}".format('Seemann','Affe','Summe'))
for loop in range(sailors):
    print("{:8d}{:8d}{:8}".format(parts[loop], 1, parts[loop] + 1))
print("\n{:16s}{:8d}".format('Teilsumme', sum(parts) + sailors))
print("{:16s}{:8d}".format('Rest', rest))
print("{:16s}{:8d}\n".format('G e s a m t',nuts))
