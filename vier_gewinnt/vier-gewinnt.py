#!/usr/bin/env python
import pygame as pg, sys, os, time, collections

DEPTH = 5           # Suchtiefe
FPS = 60            # Frame/sec
OVER_TIME = 3       # Time für Gameover

MSG_GREET = 'Vier gewinnt - Dein Click! | [-] Irrtum'
MSG_OVER = '[n] Neues Spiel | [ESC] Spiel beenden'
MSG_PLAYER = ('Player', 'Computer')
MSG_JOB = ('Der Computer denkt nach...', 'Der Player ist am Zug...')
MSG_BACK = 'Na gut, du bist dran...'

PIC_PATH = './res'
PIC_BG = 'four_bg.png'

SPALTEN = 7
ZEILEN = 6
ZELLEN = SPALTEN * ZEILEN
RICHTUNGEN = [(-1,-1),(0,-1),(1,-1), (-1,0),(1,0), (-1,1),(0,1),(1,1)]

DISPLAY_WIDTH, DISPLAY_HEIGHT = (820, 768)
DISPLAY_COLOR = (245, 245, 220)

GRID_WIDTH = 800
GRID_HEIGHT = 700
GRID_CELLS = 100
GRID_LEFT = 10
GRID_TOP = 10
GRID_DX = GRID_CELLS // 2 + GRID_LEFT 
GRID_DY = GRID_CELLS // 2 + GRID_TOP 
GRID_GAMEOVER = (((DISPLAY_WIDTH - 400) // 2, (DISPLAY_HEIGHT - 300) // 2))

MSG_BOX_HIGHT = 48
MSG_POS = (20, 720)
MSG_BG_COLOR = (30,144,255)
MSG_COLOR = (255,255,255)

pos2Index = collections.defaultdict(list)   # Relation Index - Quads
spielfeld = {}                              # Key = (spalte,zeile), value = 'O' oder 'X'
screenList = []                             # Anzeige auf Screen - keine Sprites
histList = []                               # Zugpositionen für Rücknahme

class Enum(object):
  def __init__(self, tpList):
    self.tpList = tpList
  def __getattr__(self, name):
    return self.tpList.index(name)
STATUS = Enum(('LOOP', 'DRAW', 'WIN', 'LOS', 'OVER'))
BUTTON = Enum(('NO', 'LEFT', 'MIDD', 'RIGHT'))

def quadPositionen(pos, richtung):
    positionen = set()
    sp, ze = pos
    rsp, rze = richtung
    neue_sp, neue_ze = sp + rsp * 3, ze + rze * 3
    if neue_sp < 0 or neue_sp >= SPALTEN or neue_ze < 0 or neue_ze >= ZEILEN:
        return False
    for i in range(4):
        positionen.add((sp + rsp * i, ze + rze * i))
    return positionen

def quadsErmitteln():
    quads = {}
    bekannte_positionen = set()
    counter = 0
    for i in range(ZELLEN):
        for richtung in RICHTUNGEN:
            pos = (i % SPALTEN, i // SPALTEN)
            positionen = quadPositionen(pos, richtung)
            if not positionen or positionen in bekannte_positionen: continue
            quads[counter] = [0, 0] # Anzahl gelb -> [0], rot -> [1] im Quad
            for position in positionen:
                pos2Index[position].append(counter)
            bekannte_positionen.add(frozenset(positionen))
            counter += 1
    return quads

def findeTiefsteZeile(spalte):
    for zeile in reversed(range(ZEILEN)):
        if (spalte, zeile) not in spielfeld:
            return zeile

def spalteGueltig(spalte):
    if (spalte, 0) in spielfeld:
        return False
    if 0 <= spalte < SPALTEN:
        return True

def steinSetzen(pos, spieler, real = True):
    win = False
    x, y = pos
    if real:
        screenList.append({'scrpos': (x * GRID_CELLS + GRID_DX, y * GRID_CELLS + GRID_DY), 'val': not spieler})
        histList.append(pos)
    spielfeld[pos] = 'O' if spieler else 'X'
    for i in pos2Index[pos]:
        quads[i][spieler] += 1
        if quads[i][spieler] == 4:
            win = True
    return win    

def steinLoeschen(pos, spieler, real = True):
    del spielfeld[pos]
    if real:
        screenList.pop()
        histList.pop()
    for i in pos2Index[pos]:
        quads[i][spieler] -= 1

def bewerten():
    score = 0
    for pos in spielfeld:
        for i in pos2Index[pos]:
            gelb, rot = quads[i]
            if gelb > 0 and rot > 0: continue
            score += rot * 10
            score -= gelb * 10
    return score

def zugliste():
    zuege = []
    for spalte in range(SPALTEN):
        if not spalteGueltig(spalte): continue
        zeile = findeTiefsteZeile(spalte)
        zuege.append((spalte, zeile))
    return zuege

def human_gui(spieler, spalte):
    legal = False
    win = False
    if spalteGueltig(spalte):
        legal = True
        zeile = findeTiefsteZeile(spalte)
        win = steinSetzen((spalte, zeile), spieler)
    return (legal, win)

def computer(spieler):
    bewerte_zuege = []
    for zug in zugliste():
        win = steinSetzen(zug, spieler, False)
        score = minimax(DEPTH, -999999, 999999, spieler, win)
        steinLoeschen(zug, spieler, False)
        bewerte_zuege.append((score, zug))
    bewerte_zuege.sort(reverse = spieler)
    score, bester_zug = bewerte_zuege[0]
    win = steinSetzen(bester_zug, spieler)
    msgLine(globDict['player'], bester_zug[0])
    return win

def minimax(tiefe, alpha, beta, spieler, win):
    pg.event.pump()
    if win:
        return 999999 + tiefe if spieler else -999999 - tiefe
    if tiefe == 0 or len(spielfeld) == ZELLEN:
        return bewerten()
    spieler = not spieler
    value = -999999 if spieler else 999999
    for zug in zugliste():
        win = steinSetzen(zug, spieler)
        score = minimax(tiefe - 1, alpha, beta, spieler, win)
        steinLoeschen(zug, spieler)
        if spieler:
            value = max(value, score)
            alpha = max(value, alpha)
        else:
            value = min(value, score)
            beta = min(value, beta)
        if alpha >= beta:
            break
    return value

def msgLine(aGamer, aMove):
    global msg_txt, msg_font
    msg = "{:s}: Spalte{:2d} - {:s}".format(MSG_PLAYER[aGamer - 1], aMove  + 1, MSG_JOB[aGamer - 1])
    msg_txt = msg_font.render(msg, True, MSG_COLOR)

def goback():
    global globDict, msg_txt
    if globDict['working'] or len(histList) < 2:
        return
    pl, co = histList[-2:]
    steinLoeschen(co, False)
    steinLoeschen(pl, True)
    msg_txt = back_txt

def boardUpdate():
    screen.fill(DISPLAY_COLOR)
    pg.draw.rect(screen, MSG_BG_COLOR, (GRID_LEFT, GRID_HEIGHT + GRID_TOP, GRID_WIDTH, MSG_BOX_HIGHT))
    screen.blit(msg_txt, MSG_POS)
    if screenList:
        for i in screenList:
            screen.blit(clips[i['val']].convert_alpha(), i['scrpos']) 
    screen.blit(backGround.convert_alpha(), (GRID_LEFT, GRID_TOP)) 
    pg.display.flip()

def reset():
    global quads, globDict, msg_txt
    if globDict['status'] == STATUS.OVER:
        msg_txt = msg_font.render(MSG_GREET, True, MSG_COLOR)
        for key, value in quads.items():
            quads[key] = [0, 0]
        del screenList[:]
        del histList[:]
        spielfeld.clear()
        globDict['working'] = False
        globDict['player'] = True           
        globDict['status'] = STATUS.LOOP

quads = quadsErmitteln()

pg.init()
clock = pg.time.Clock()
window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

msg_caption = "*** GEWINNE GEGEN PUSSEL IN LEVEL {} ***".format(DEPTH)
pg.display.set_caption(msg_caption)
screen = pg.display.get_surface()
backGround = pg.image.load(os.path.join(PIC_PATH, PIC_BG))
clips = [ pg.image.load(os.path.join(PIC_PATH, "four_clip{}.png".format(x))) for x in [1, 2] ] 
goPics = [ pg.image.load(os.path.join(PIC_PATH, "four_game_over{}.png".format(x))) for x in [1, 2, 3] ]

msg_font = pg.font.SysFont(None, 36)
msg_txt = msg_font.render(MSG_GREET, True, MSG_COLOR)
wait_txt = msg_font.render(MSG_OVER, True, MSG_COLOR)
back_txt = msg_font.render(MSG_BACK, True, MSG_COLOR)

globDict = {'working': False, 'player': True, 'status': STATUS.LOOP}
markTime = 0
click = False
running = True
while running:
    if click:
        click = False
        if globDict['status'] == STATUS.LOOP:
            if not globDict['working']:
                mx, my = pg.mouse.get_pos()
                mx -= GRID_LEFT; my -= GRID_TOP
                if GRID_HEIGHT > my > 0 and GRID_WIDTH > mx > 0:
                    player_move = (mx - GRID_LEFT - (GRID_CELLS // 2)) // GRID_CELLS
                    legal, win = human_gui(globDict['player'], player_move)
                    if win:
                        globDict['status'] = STATUS.WIN
                        markTime = int(time.perf_counter())
                        continue
                    if not legal: continue
                    msgLine(globDict['player'], player_move)
                    boardUpdate()
                    globDict['working'] = True
                    globDict['player'] = not globDict['player']
                    win = computer(globDict['player']) 
                    if win:
                        globDict['status'] = STATUS.LOS
                        markTime = int(time.perf_counter())
                    elif len(spielfeld) == ZELLEN:
                        globDict['status'] = STATUS.DRAW
                        markTime = int(time.perf_counter())
                    globDict['player'] = not globDict['player']                   
                    globDict['working'] = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == BUTTON.LEFT:
                click = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_MINUS:
                goback()
            if event.key == pg.K_n:
                reset()

    screen.fill(DISPLAY_COLOR)
    pg.draw.rect(screen, MSG_BG_COLOR, (GRID_LEFT, GRID_HEIGHT + GRID_TOP, GRID_WIDTH, MSG_BOX_HIGHT))
    screen.blit(msg_txt, MSG_POS)
    if screenList:
        for i in screenList:
            screen.blit(clips[i['val']].convert_alpha(), i['scrpos']) 
    screen.blit(backGround.convert_alpha(), (GRID_LEFT, GRID_TOP)) 

    if STATUS.LOOP < globDict['status'] < STATUS.OVER:
        screen.blit(goPics[globDict['status'] - 1].convert_alpha(), GRID_GAMEOVER)
        if int(time.perf_counter()) - markTime > OVER_TIME:
            globDict['status'] = STATUS.OVER

    if globDict['status'] == STATUS.OVER:
        msg_txt = wait_txt
        
    pg.display.flip()
    clock.tick(FPS)
pg.quit()
sys.exit()
