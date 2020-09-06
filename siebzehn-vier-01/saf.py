#!/usr/bin/env python
import pygame as pg, sys, os, random

FPS = 24
PIC_FOLDER = 'res'
PICS_MAX = 7
CARDS_TOTAL = 52
CARDS_POS = [   [(50, 120), (130, 120), (210, 120), (290, 120), (370, 120), (450, 120), (530, 120)],
                [(50, 240), (130, 240), (210, 240), (290, 240), (370, 240), (450, 240), (530, 240)]]
RECT_M_POS = [ 530, 122, 326 ]
DISPLAY_WIDTH, DISPLAY_HEIGHT = (652, 510)
DISPLAY_COLOR = (0, 100, 0)
BU_LEFT, BU_RIGHT = (1, 3)
PLAYER, BANK, OVER = (0, 1, 2)
RESULT_COLOR = (255, 248, 220)
DANGER_COLOR = (220, 20, 60)

globVars = {
    'player': True,
    'status': PLAYER,
    'wins': [0, 0], 
    'count': [0, 0],
    'points': [0, 0]
    }
talon = []
pics_all = []
pics_out = [[], []]

def init():
    global pics_all, talon
    random.seed()
    reset()
    for h in range(100, 500, 100):
        for x in range(2, 15):
            pics_all.append(pg.image.load(os.path.join(PIC_FOLDER, "{}.png".format(h + x))))
    talon = newTalon()
    
def newTalon():
    c_vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 11] 
    li = [ (num, c_vals[num % 13]) for num in range(CARDS_TOTAL) ]
    random.shuffle(li)
    return li  

def reset():
    globVars['player'] = True
    globVars['status'] = PLAYER
    for i in [False, True]:
        del pics_out[i][:]
        globVars['count'][i] = 0
        globVars['points'][i] = 0

def drawPics():
    for player in [False, True]:
        if pics_out[player]:
            for loop, pic in enumerate(pics_out[player]):
                screen.blit(pic.convert_alpha(), CARDS_POS[player][loop])

def drawPoints(fnt):
    txt = "{:d} : {:d}".format(globVars['wins'][True], globVars['wins'][False])
    rendered = fnt.render(txt, True, RESULT_COLOR)
    rect = rendered.get_rect(center = (RECT_M_POS[2], 415))
    screen.blit(rendered, rect)
    for player in [False, True]:
        points = globVars['points'][player]
        if points:
            rc = RESULT_COLOR if points < 16 else DANGER_COLOR
            rendered = fnt.render(str(points), True, rc)
            rect = rendered.get_rect(center = (RECT_M_POS[player], 415))
            screen.blit(rendered, rect)

def getCard():
    global talon, globVars
    if not (talon):
        talon = newTalon()
    card = talon.pop()
    nr, val = card
    pl = globVars['player']
    globVars['points'][pl] += val
    globVars['count'][pl] += 1
    if globVars['count'][pl] <= PICS_MAX:
        pics_out[pl].append(pics_all[nr])
    pnt = globVars['points'][pl]
    if(((globVars['count'][pl] == 2) and (pnt == 22)) or (pnt == 21)):
        globVars['wins'][pl] += 1
        globVars['status'] = OVER
    elif pnt > 21:
        globVars['wins'][not pl] += 1
        globVars['status'] = OVER

def risiko():
    global globVars
    ris = 0
    points = globVars['points'][False]
    for i in talon:
        nr, val = i
        if points + val > 21:
            ris += 2
    return (ris > len(talon))

def bank():
    global globVars
    if not globVars['count'][True]:
        return
    globVars['status'] = BANK
    globVars['player'] = False
    getCard()

def nextCard():
    global globVars
    if risiko():
        globVars['status'] = OVER
        if globVars['points'][True] > globVars['points'][False]:
            globVars['wins'][True] += 1
        else:
            globVars['wins'][False] += 1
    else:
        getCard()
# -- main ---
pg.init()
init()
bg_table = pg.image.load(os.path.join(PIC_FOLDER, "table.png"))
font = pg.font.SysFont(None, 80)
clock = pg.time.Clock()
window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen = pg.display.get_surface()
pg.display.set_caption("Schlag den Pussel! [ESC] = Quit")

click = False
running = True
while running:
    if globVars['status'] == BANK:
        nextCard()
    if click:
        click = False
        mx, my = pg.mouse.get_pos()
        yOk = 380 < my < 500
        if yOk and (42 < mx < 202) and (globVars['status'] == PLAYER):
            getCard()
        if yOk and (240 < mx < 410) and (globVars['status'] == OVER):
            reset()
        if yOk and (450 < mx < 610) and (globVars['status'] == PLAYER):
            bank()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == BU_LEFT:
                click = True

    screen.fill(DISPLAY_COLOR)
    drawPics()
    drawPoints(font)
    screen.blit(bg_table.convert_alpha(),(0, 0))
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
sys.exit()
