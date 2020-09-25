#!/usr/bin/env python
import pygame as pg, sys, os

FPS = 60
PIC_FOLDER = 'res'

DISPLAY_WIDTH, DISPLAY_HEIGHT = (1000, 1000)
DELTA_X, DELTA_Y = (100, 100)
DISPLAY_CAPTION = "Das Acht-Damen-Problem"
FIELDS = 8
FIELD_LEN = 100
FREE = -999

class Queen(object):
    def __init__(self):
        self._screen = 0
        self._pic = 0
        self._posi = 0
        self._positionen = dict({})
        yPos = list([(FREE) for i in range(FIELDS)])
        def legal(x, y):
            for xi in range(FIELDS):
                if (yPos[xi] == y) or (xi + yPos[xi] == x + y) or (xi - yPos[xi] == x - y):
                    return False
            return True
        def solution():
            li = []
            po = []
            for x, y in enumerate(yPos):
                li.append((x, y))
            for key in li:
                x, y = key
                po.append((x * FIELD_LEN + DELTA_X, y * FIELD_LEN + DELTA_Y))
                self._positionen[key] = po
        def generate():
            for x in range(FIELDS):
                if yPos[x] == FREE:
                    for y in range(FIELDS):
                        if legal(x, y):
                            yPos[x] = y
                            generate()
                            yPos[x] = FREE
                    return 
            solution()
        generate()
    def draw(self):
        if not self._posi:
            return
        for x in self._positionen[self._posi]: 
            self._screen.blit(self._pic.convert_alpha(), x)
    def const(self, val):
        self._screen = val[0]
        self._pic = val[1]
    def posi(self, val):
        t = ((val[0] // FIELD_LEN) - 1, (val[1] // FIELD_LEN) - 1)
        self._posi = t if t in self._positionen else 0
    const = property(None, const)
    posi = property(None, posi)

def main():
    queen = Queen()
    pg.init()
    sur_board = pg.image.load(os.path.join(PIC_FOLDER, "bg_queen.png"))
    clock = pg.time.Clock()
    window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pg.display.set_caption(DISPLAY_CAPTION)
    screen = pg.display.get_surface()
    queen.const = ((screen, pg.image.load(os.path.join(PIC_FOLDER, "vg_queen.png"))))
    running = True
    click = False
    while running:
        if click:
            click = False
            queen.posi = (pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        screen.blit(sur_board.convert_alpha(),(0, 0))
        queen.draw()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()

if __name__ == "__main__":
    main()
    sys.exit()
