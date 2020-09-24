#!/usr/bin/env python
import pygame as pg, sys, os
from collections import deque

FPS = 60
PIC_FOLDER = 'res'
DISPLAY_WIDTH, DISPLAY_HEIGHT = (440, 230)
DISPLAY_COLOR = (198,183,107)
DISPLAY_CAPTION = "Die Türme von Hanoi"

DISCS       = 4
DISCHEIGHT  = 30
XBORDER     = 20
YBORDER     = 50
YMOVING     = 22
STEP        = 4

class Enum(object):
  def __init__(self, tpList):
    self.tpList = tpList
  def __getattr__(self, name):
    return self.tpList.index(name)

MOVE = Enum(('STAY', 'UP', 'DOWN', 'LEFT', 'RIGHT'))

class Manag(object):
  def __init__(self):
    self.deq = deque()
    self.x_Pos = { 'A': 20, 'B': 160, 'C': 300 }
    self.y_Pos = { 'A': 50, 'B': 170, 'C': 170 }
    self.hanoi(DISCS, 'A', 'B', 'C')
  def hanoi(self, anzahl, von, temp, ziel):
    if anzahl > 0:
      self.hanoi(anzahl - 1, von, ziel, temp)
      self.deq.append((anzahl, von, ziel))
      self.hanoi(anzahl - 1, temp, von, ziel) 
  def next(self):
    if not self.deq:
      return False
    id, source, dest = self.deq.popleft() 
    data = {'id': id, 'deltaX': self.x_Pos[dest], 'deltaY': self.y_Pos[dest]}
    self.y_Pos[dest] -= DISCHEIGHT
    self.y_Pos[source] += DISCHEIGHT
    return data

class Disk(object):
  def __init__(self, screen, id):
    self._screen = screen
    self._id = id
    self._data = 0
    self._mvStatus = MOVE.STAY 
    self._pic = pg.image.load(os.path.join(PIC_FOLDER, "disc{}.png".format(self._id)))
    self._pos = (XBORDER, DISCHEIGHT * self._id + YBORDER)
  def draw(self):
    self._screen.blit(self._pic.convert_alpha(),self._pos) 
  def initMove(self, data):
    if data['id'] != self._id: return
    self._data = data
    self._mvStatus = MOVE.UP
  def move(self):
    if self._mvStatus == MOVE.STAY: return False
    x_pos, y_pos = self._pos
    if self._mvStatus == MOVE.UP:
      y_pos -= STEP
      if y_pos < YMOVING:
        y_pos = YMOVING
        self._mvStatus = MOVE.LEFT if x_pos > self._data['deltaX'] else MOVE.RIGHT
    elif self._mvStatus == MOVE.LEFT:
      x_pos -= STEP
      if x_pos < self._data['deltaX']:
        x_pos = self._data['deltaX']       
        self._mvStatus = MOVE.DOWN
    elif self._mvStatus == MOVE.RIGHT:
      x_pos += STEP
      if x_pos > self._data['deltaX']:
        x_pos = self._data['deltaX']        
        self._mvStatus = MOVE.DOWN
    elif self._mvStatus == MOVE.DOWN:
      y_pos += STEP
      if y_pos > self._data['deltaY']:
        self._pos = (x_pos, self._data['deltaY'])
        self._mvStatus = MOVE.STAY
        return False
    self._pos = (x_pos, y_pos)  
    return True

def main():
    manag = Manag()
    pg.init()
    bg_table = pg.image.load(os.path.join(PIC_FOLDER, "hanoi_table.png"))
    clock = pg.time.Clock()
    window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pg.display.set_caption(DISPLAY_CAPTION)
    screen = pg.display.get_surface()
    allDisks = [ (Disk(screen, loop)) for loop in range(4, 0, -1) ]
    running = True
    while running:
      moves = 0
      for actDisk in allDisks: moves += actDisk.move()
      if not moves:
        initDict = manag.next()
        if initDict:
          for actDisk in allDisks: actDisk.initMove(initDict)
      for event in pg.event.get():
          if event.type == pg.QUIT:
              running = False
          if event.type == pg.KEYDOWN:
              if event.key == pg.K_ESCAPE:
                  running = False
      screen.fill(DISPLAY_COLOR)
      screen.blit(bg_table.convert_alpha(),(0, 0))
      for actDisk in allDisks: actDisk.draw()
      pg.display.flip()
      clock.tick(FPS)
    pg.quit()

if __name__ == "__main__":
    main()
    sys.exit()

