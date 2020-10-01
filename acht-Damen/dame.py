#!/usr/bin/env python3

FIELDS = 8
FREE = -999
BLANK = '|.' * FIELDS + '|'

yPos = [FREE for i in range(FIELDS)]
loop = 0

def solution():
    global loop
    loop += 1
    print(f" * Variante{loop:>3d} *")
    for index in yPos:
        k = 2 * index + 1
        print(BLANK[:k] + 'Q' + BLANK[k+1:])
    print()

def legal(x, y):
    for xi in range(FIELDS):
        if (yPos[xi] == y) or (xi + yPos[xi] == x + y) or (xi - yPos[xi] == x - y):
            return False
    return True

def main():
    for x in range(FIELDS):
        if yPos[x] == FREE:
            for y in range(FIELDS):
                if legal(x, y):
                    yPos[x] = y
                    main()
                    yPos[x] = FREE
            return 
    solution()

if __name__ == "__main__":
    main()


