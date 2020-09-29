#!/usr/bin/env python3
import argparse
from typing import TypeVar, Generic, List

ANZAHL: int = 3

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, required=False, help="Anzahl der Scheiben default=3 max=8")
args = parser.parse_args()
anz = args.n
scheiben = anz if anz != None and 2 < anz < 9 else ANZAHL

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self, id: str) -> None:
        self._container: List[T] = []
        self._id = id

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)
    @property
    def id(self) -> str:
        return self._id

tower_a: Stack[int] = Stack('A')       
tower_b: Stack[int] = Stack('B')       
tower_c: Stack[int] = Stack('C')       

for i in range(scheiben, 0, -1):
    tower_a.push(i)

def hanoi(source: Stack[int], dest: Stack[int], tmp: Stack[int], num: int) -> None:
    if num == 1:
        tmp = source.pop()
        dest.push(tmp)
        print(f"Scheibe {tmp:d} von {source.id:s} nach {dest.id:s}")
    else:
        hanoi(source, tmp, dest, num - 1)
        hanoi(source, dest, tmp, 1)
        hanoi(tmp, dest, source, num - 1)

if __name__ == "__main__":
    hanoi(tower_a, tower_c, tower_b, scheiben)  
