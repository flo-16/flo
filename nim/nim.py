#!/usr/bin/env python3
import os, sys, time, random, copy, pygame as pg, button as bu

PIKES = 3
LIM_MIN, LIM_MAX = 1, 8
FPS = 60
# ---------------------------------------------
DISPLAY_CAPTION = 'Das grosse NIM-Spiel'
CTR_BUTTON_TXT = ("Ich habe fertig", "Weiter geht's", "Neues Spiel")
# ---------------------------------------------
PIC_WIDTH = 50
PIC_HIGHT = 100
DISPLAY_DIST = 40
MATCH_HEIGHT = ((PIKES * PIC_HIGHT + DISPLAY_DIST))
CTR_BUTTON_HIGHT = 40
DISPLAY_WIDTH = ((LIM_MAX * PIC_WIDTH) + (2 * DISPLAY_DIST))
DISPLAY_HEIGHT = (3 * DISPLAY_DIST + MATCH_HEIGHT + CTR_BUTTON_HIGHT)
DISPLAY_HALF_WIDTH = DISPLAY_WIDTH // 2
# ---------------------------------------------
NO_SELECT = -1
CTR_BUTTONS = 3
CTR_BUTTON_TOP = (2 * DISPLAY_DIST + MATCH_HEIGHT - (CTR_BUTTON_HIGHT // 2))
CTR_BUTTON_ABS = 20
CTR_BUTTON_WTDTH = 128
CTR_BUTTON_LEFT = (DISPLAY_HALF_WIDTH - ((CTR_BUTTONS * (CTR_BUTTON_WTDTH + CTR_BUTTON_ABS) - CTR_BUTTON_ABS) // 2)) 
CTR_BUTTON_X_POS = [( x * (CTR_BUTTON_WTDTH + CTR_BUTTON_ABS) + CTR_BUTTON_LEFT) for x in range(CTR_BUTTONS) ]      
# ---------------------------------------------
BG_COLOR = (47, 79, 79)
BU_BO_COLOR = (0, 0, 139)
BU_HO_COLOR = (0, 255, 255)
BU_COLOR = (30, 144, 255)
BU_TXT_COLOR = (255, 250, 250)

class Enum(object):
  def __init__(self, tpList):
    self.tpList = tpList
  def __getattr__(self, name):
    return self.tpList.index(name)
STATUS = Enum(('HIDDEN', 'INACT', 'ACTIV', 'OPPONENT', 'SELF'))
GAME = Enum(('INIT', 'PLAY', 'DEAL'))

def xyPos(nr):
    x = ( nr % LIM_MAX ) * PIC_WIDTH + DISPLAY_DIST
    y = ( nr // LIM_MAX ) * PIC_HIGHT + DISPLAY_DIST
    return (x, y)

class Match_Area:
    def __init__(self, screen):
        self._screen = screen
        self._globs = { 'game': GAME.INIT, 'row': NO_SELECT, 'count': 0, 'wins': [0, 0] }
        self._pics = []
        self._matches = []
        self._los = []
        self._actLos = []
        for x in range(1, 5):
            self._pics.append(pg.image.load(os.path.join('./res', "nim_{}_pse.png".format(x))))
        for x in range(PIKES * LIM_MAX):
            self._matches.append({'stat': STATUS.HIDDEN, 'pos': xyPos(x)})
        random.seed()
        self.newGame()  
    def draw(self):
        for x in range(PIKES * LIM_MAX):
            k = self._matches[x]['stat']
            if k:
                self._screen.blit(self._pics[k - 1].convert_alpha(),(self._matches[x]['pos']))    
    def newGame(self):
        if self._globs['game'] != GAME.INIT:
            return
        pg.display.set_caption(DISPLAY_CAPTION)
        for x in range(PIKES * LIM_MAX):
            self._matches[x]['stat'] = STATUS.HIDDEN
        self._los = [ random.randint(LIM_MIN, LIM_MAX) for x in range(PIKES) ]
        self._actLos = copy.deepcopy(self._los)
        for i, v in enumerate(self._actLos):
            b = i * LIM_MAX
            for x in range(b, b + v):
               self._matches[x]['stat'] = STATUS.ACTIV
        self._globs['game'] = GAME.PLAY
    def playerSelect(self, pos):
        if self._globs['game'] != GAME.PLAY:
            return
        col = (pos[0] - DISPLAY_DIST) // PIC_WIDTH 
        row = (pos[1] - DISPLAY_DIST) // PIC_HIGHT
        ind = LIM_MAX * row + col
        sta = self._matches[ind]['stat']
        if  sta > STATUS.INACT:
            if self._globs['row'] == NO_SELECT:
               self._globs['row'] = row
            if self._globs['row'] == row:   
                if sta == STATUS.ACTIV: 
                    self._matches[(self._globs['row'] * LIM_MAX + self._globs['count'])]['stat'] = STATUS.OPPONENT
                    self._globs['count'] += 1
                elif sta == STATUS.OPPONENT:
                    self._globs['count'] -= 1
                    self._matches[(self._globs['row'] * LIM_MAX + self._globs['count'])]['stat'] = STATUS.ACTIV
                    if not self._globs['count']:
                        self._globs['row'] = NO_SELECT
    def dealerSelect(self):
        if self._globs['game'] != GAME.PLAY or self._globs['row'] == NO_SELECT:
            return
        self._actLos[self._globs['row']] -= self._globs['count']
        if sum(x for x in self._actLos) == 0:
            self._globs['wins'][0] += 1
            self._globs['row'] = NO_SELECT
            self._globs['count'] = 0
            self._globs['game'] = GAME.INIT
            self.setCaption()
            return
        self._globs['game'] = GAME.DEAL    
        selList = [ x for x in range(PIKES) ]
        random.shuffle(selList)
        korr = 0
        xors = 0
        startpoint = 0
        for x in self._actLos:
            xors ^= x
        if xors:
            xorList = list(map(lambda x: x ^ xors, self._actLos))
            for x in selList:
                if xorList[x] < self._actLos[x]:
                    korr = self._actLos[x] - xorList[x]
                    self._actLos[x] = xorList[x]
                    break
        else:
            for x in selList:
                if self._actLos[x] > 0:
                    oldVal = self._actLos[x]
                    newVal = random.randint(0, self._actLos[x] - 1)
                    self._actLos[x] = newVal
                    korr = oldVal - self._actLos[x]
                    break
        startpoint = x * LIM_MAX
        if self._globs['row'] == x:
            startpoint += self._globs['count'] 
        for x in range(startpoint, startpoint + korr):
            self._matches[x]['stat'] = STATUS.SELF
        self._globs['row'] = NO_SELECT
        self._globs['count'] = 0
        if sum(x for x in self._actLos) == 0:
            self._globs['wins'][1] += 1
            self.setCaption()
    def result(self):
        if self._globs['game'] != GAME.DEAL:
            return
        for ind, val in enumerate(self._actLos):
            ul = ind * LIM_MAX
            ml = ul + val
            ol = ul + self._los[ind]
            for x in range(ul, ml):
                self._matches[x]['stat'] = STATUS.ACTIV
            for x in range(ml, ol):
                self._matches[x]['stat'] = STATUS.INACT
        if sum(x for x in self._actLos):
            self._globs['game'] = GAME.PLAY
        else:
            self._globs['game'] = GAME.INIT
    def setCaption(self):
        pg.display.set_caption("{} : {}".format(self._globs['wins'][0], self._globs['wins'][1]))

class CTR_Area:        
    def __init__(self, screen):
        self._screen = screen
        self._ctrButton = [ bu.Button(self._screen, CTR_BUTTON_X_POS[x], CTR_BUTTON_TOP, CTR_BUTTON_WTDTH, CTR_BUTTON_HIGHT,
            colour = BU_COLOR, text_colour = BU_TXT_COLOR, border_colour = BU_BO_COLOR, hover_colour = BU_HO_COLOR, 
            text = CTR_BUTTON_TXT[x], text_size = 16, bold_text = False)
            for x in range(CTR_BUTTONS)]  
    def draw(self):
        for object in self._ctrButton:
            object.draw()
            object.update()  
        
def main():
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen = pg.display.get_surface()
    board = Match_Area(screen)
    ctrl = CTR_Area(screen)
    running = True
    click = False
    while running:
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                running = False
            if evt.type == pg.KEYDOWN:
                if evt.key == pg.K_ESCAPE:
                    running = False
            if evt.type == pg.MOUSEBUTTONDOWN:
                if evt.button == 1:
                    click = True
        if click:
            click = False
            board.setCaption()
            mx, my = pg.mouse.get_pos()
            if DISPLAY_WIDTH - DISPLAY_DIST > mx > DISPLAY_DIST and MATCH_HEIGHT > my > DISPLAY_DIST:
                board.playerSelect((mx, my))
            if CTR_BUTTON_TOP + CTR_BUTTON_HIGHT > my > CTR_BUTTON_TOP:
                if CTR_BUTTON_X_POS[0] + CTR_BUTTON_WTDTH > mx > CTR_BUTTON_X_POS[0]: board.dealerSelect()
                if CTR_BUTTON_X_POS[1] + CTR_BUTTON_WTDTH > mx > CTR_BUTTON_X_POS[1]: board.result()
                if CTR_BUTTON_X_POS[2] + CTR_BUTTON_WTDTH > mx > CTR_BUTTON_X_POS[2]: board.newGame()
        screen.fill(BG_COLOR)
        board.draw()
        ctrl.draw()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()

if __name__ == "__main__":
    main()
    sys.exit()
