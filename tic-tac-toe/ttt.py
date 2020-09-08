#!/usr/bin/python3

import pygame as pg, sys, os
from minimax import find_best_move
from tictactoe import TTTBoard
from board import Move, Board

PIC_PATH = './res'
PLAYER, COMPUTER = (1, 2)
DISPLAY_CAPTION = 'TIC - TAC - TOE'
CELLS, CELLS_X, CELLS_Y = (9, 3, 3)
CELL_WIDTH, CELL_HEIGHT = (200, 200)
CELL_MATRIX = CELLS_X * CELL_WIDTH, CELLS_Y * CELL_HEIGHT
DISPLAY_WIDTH, DISPLAY_HEIGHT = CELL_MATRIX
FPS = 24
# ---------------------------------------------
MATRIX_COLOR = (47, 79, 79)
GRID_COLOR = (255, 255, 0)
GRID_WIDTH = 2
# ---------------------------------------------
HIDE, DRAW, WIN, LOS = (0, 1, 2, 3)
BU_LEFT, BU_RIGHT = (1, 3)

class Grid:
    def __init__(self, screen):
        self._screen = screen
        self._items = [ 0 for x in range(CELLS) ]
        self.grid_lines = [ ((0, y * CELL_HEIGHT), (CELLS_X * CELL_WIDTH, y * CELL_HEIGHT)) for y in range(1, CELLS_Y) ]
        self.grid_lines.extend( [ ((x * CELL_WIDTH, 0), (x * CELL_WIDTH, CELLS_Y * CELL_HEIGHT)) for x in range(1, CELLS_X) ])
        self.pic_list = [ pg.image.load(os.path.join(PIC_PATH, "tictactoe{}.png".format(x))) for x in range(1, 3) ] 
        self.pic_pos = [ ( ( x % CELLS_X ) * CELL_WIDTH, ( x // CELLS_Y ) * CELL_HEIGHT) for x in range(CELLS) ]                  
    def draw(self):
        for line in self.grid_lines:
            pg.draw.line(self._screen, GRID_COLOR, line[0], line[1], GRID_WIDTH)
        for pos, val in enumerate(self._items):
            if not val:
                continue
            self._screen.blit(self.pic_list[val - 1].convert_alpha(), self.pic_pos[pos]) 
    def pic(self, act_pic, act_nr):
        self._items[act_nr] = act_pic
    def reset(self):
        self._items = [ 0 for x in range(CELLS) ]

class MsgBox:
    def __init__(self, screen):
        self._screen = screen
        self._active = HIDE
        self.pic_list = [ pg.image.load(os.path.join(PIC_PATH, "game_over{}.jpg".format(x))) for x in range(1, 4) ] 
        self.pic_pos = (DISPLAY_WIDTH - CELL_WIDTH, DISPLAY_HEIGHT - 80)
    @property
    def active(self):
        return self._active
    @active.setter
    def active(self, value):
        self._active = value
    def draw(self):
        if not self._active: return
        self._screen.blit(self.pic_list[self._active - 1].convert(), (self.pic_pos))

class GuiBoard():
    def __init__(self, screen):
        self._screen = screen
        self._board = TTTBoard()
        self._grid = Grid(self._screen)
        self._msgBox = MsgBox(self._screen)
        self._msgStatus = HIDE
        self._game_over = False
    def draw(self):
        self._grid.draw()
        self._msgBox.draw()
    def setMove(self, value):
        mx, my = value
        player_move = (my // CELL_HEIGHT * 3) + (mx // CELL_WIDTH)
        if player_move in self._board.legal_moves:
            self._board = self._board.move(Move(player_move))
            self._grid.pic(PLAYER, player_move)
            if self._board.is_win:
                self._game_over = True
                self._msgBox.active = WIN
            elif self._board.is_draw:
                self._game_over = True
                self._msgBox.active = DRAW
            if not self._game_over:
                computer_move = find_best_move(self._board)
                self._board = self._board.move(Move(computer_move))
                self._grid.pic(COMPUTER, computer_move)
                if self._board.is_win:
                    self._game_over = True
                    self._msgBox.active = LOS
                elif self._board.is_draw:
                    self._game_over = True
                    self._msgBox.active = DRAW
    def reset(self):
        self._board.reset()
        self._grid.reset()
        self._msgBox.active = HIDE
        self._game_over = False
    @property
    def game_over(self):
        return self._game_over

def main():
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pg.display.set_caption(DISPLAY_CAPTION)
    screen = pg.display.get_surface()
    guiBoard = GuiBoard(screen)
    click = False; reset = False
    running = True
    while running:
        if click:
            click = False
            if not guiBoard.game_over:
                guiBoard.setMove((pg.mouse.get_pos()))
        if reset:
            reset = False
            if guiBoard.game_over:
                guiBoard.reset()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == BU_LEFT:
                    click = True
                if event.button == BU_RIGHT:
                    reset = True
        screen.fill(MATRIX_COLOR)
        guiBoard.draw()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()

if __name__ == "__main__":
    main()
    sys.exit()
