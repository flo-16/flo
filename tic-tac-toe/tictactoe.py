# tictactoe.py

from typing import List
from enum import Enum
from board import Piece, Board, Move

FIELDS = 9

class TTTPiece(Piece, Enum):
    X = "X"
    O = "O"
    E = " " # Platzhalter für leer

    @property
    def opposite(self):
        if self == TTTPiece.X:
            return TTTPiece.O
        elif self == TTTPiece.O:
            return TTTPiece.X
        else:
            return TTTPiece.E

    def __str__(self):
        return self.value


class TTTBoard(Board):
    def __init__(self, position = [TTTPiece.E] * FIELDS, turn = TTTPiece.X):
        self.position: List[TTTPiece] = position
        self._turn: TTTPiece = turn

    def reset(self):
        self.position = [ TTTPiece.E for x in range(FIELDS) ]
        self._turn = TTTPiece.X 

    @property
    def turn(self):
        return self._turn

    def move(self, location: Move):
        temp_position: List[TTTPiece] = self.position.copy()
        temp_position[location] = self._turn
        return TTTBoard(temp_position, self._turn.opposite)

    @property
    def legal_moves(self):
        return [Move(l) for l in range(len(self.position)) if self.position[l] == TTTPiece.E]

    @property
    def is_win(self):
        # 3 Zeilen, 3 Spalten und dann 2 Diagonalen - geht auch anders!
        return bool(self.position[0] == self.position[1] and self.position[0] == self.position[2] and self.position[0] != TTTPiece.E or \
                    self.position[3] == self.position[4] and self.position[3] == self.position[5] and self.position[3] != TTTPiece.E or \
                    self.position[6] == self.position[7] and self.position[6] == self.position[8] and self.position[6] != TTTPiece.E or \
                    self.position[0] == self.position[3] and self.position[0] == self.position[6] and self.position[0] != TTTPiece.E or \
                    self.position[1] == self.position[4] and self.position[1] == self.position[7] and self.position[1] != TTTPiece.E or \
                    self.position[2] == self.position[5] and self.position[2] == self.position[8] and self.position[2] != TTTPiece.E or \
                    self.position[0] == self.position[4] and self.position[0] == self.position[8] and self.position[0] != TTTPiece.E or \
                    self.position[2] == self.position[4] and self.position[2] == self.position[6] and self.position[2] != TTTPiece.E)

    def evaluate(self, player: Piece):
        if self.is_win and self.turn == player:
            return -1
        elif self.is_win and self.turn != player:
            return 1
        else:
            return 0

    def __repr__(self):
        return f"""{self.position[0]}|{self.position[1]}|{self.position[2]}
-----
{self.position[3]}|{self.position[4]}|{self.position[5]}
-----
{self.position[6]}|{self.position[7]}|{self.position[8]}"""
