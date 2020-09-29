#!/usr/bin/env python3
import pygame as pg, sys, os

FPS = 60

DISPLAY_WIDTH, DISPLAY_HEIGHT = (200, 200)
DISPLAY_CAPTION = "Pygame-Basic"

class Enum(object):
  def __init__(self, tpList):
    self.tpList = tpList
  def __getattr__(self, name):
    return self.tpList.index(name)
BUTTON = Enum(('NO', 'LEFT', 'MIDD', 'RIGHT'))

def main():
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pg.display.set_caption(DISPLAY_CAPTION)
    screen = pg.display.get_surface()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == BUTTON.LEFT:
                    pass
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()

if __name__ == "__main__":
    main()
    sys.exit()
