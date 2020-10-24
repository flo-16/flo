#!/usr/bin/env python3
import pygame as pg, sys, os, random
from itertools import combinations
from collections import defaultdict 

FPS = 60
PIC_FOLDER = 'res'

DISPLAY_WIDTH, DISPLAY_HEIGHT = (880, 630)
TOP_BOARD = 250
TOP_POKET = 270
TOP_BEST = 440
LEFT_BOARD = 240
LEFT_POKET = (28, 698)
LEFT_BEST = (28, 450)
GAUGE = (LEFT_BOARD, TOP_BOARD + 130)
MSG_RECT = (240, 560, 400, 62)

DISPLAY_CAPTION = "Poker-V1.1"
RAENGE = ['High Card', 'One Pair', 'Two Pair', 'Three', 'Straight', 'Flush', 'Full House',
         'Four', 'Straight Flush', 'Royal Flush']
GEWINNER = ['Player', 'Bank']

class Enum(object):
    def __init__(self, tpList):
        self.tpList = tpList
    def __getattr__(self, name):
        return self.tpList.index(name)
BUTTON = Enum(('NO', 'LEFT', 'MIDD', 'RIGHT'))

class Help(object):
    def __init__(self, scr):
        self._screen = scr
        self._help_pic = pg.image.load(os.path.join(PIC_FOLDER,'rules.jpg'))
        self._hide = True
        self.xPos = 538
    def draw(self):
        if self._hide:
            return
        self._screen.blit(self._help_pic.convert(), (self.xPos, 0))
    def switch(self):
        self._hide = not self._hide

class Msgbox(object):
    def __init__(self, scr, rect):
        self._screen = scr
        self._rect = rect
        self._patt = False
        self._inRect = (self._rect[0] + 1, self._rect[1] + 1, self._rect[2] - 2, self._rect[3] - 2)
        self._visible = False
        self._render = None
        self._pos = None
        self._font = pg.font.Font(None, 40)
    def draw(self):
        if not self._visible:
            return    
        pg.draw.rect(self._screen, (0,0,0), self._rect)
        pg.draw.rect(self._screen, (255,255,255), self._inRect)
        self._screen.blit(self._render, self._pos)
    def setMsg(self, win, r0, r1):
        if self._patt:
            s = "Unentschieden"
            c = (0,0,0)
        else:
            s = "{:s} <-> {:s}".format(RAENGE[r0], RAENGE[r1])
            c = (255, 0, 0) if win else (0, 128, 0)
        self._render = self._font.render(s, True, c)
        x, y, w, h = self._render.get_rect()
        self._pos = ((DISPLAY_WIDTH - w) // 2, y + 578, w, h)
        self._visible = True
    @property
    def patt(self):
        return self._patt
    @patt.setter
    def patt(self, val):
        self._patt = val

class Money(object):
    def __init__(self, scr, pos, limes = 200):
        self._screen = scr
        self._pos = pos
        self._limes = limes
        self._saldo = limes // 2
        self.outRect = pg.Rect(self._pos[0] - 1, self._pos[1] - 1, 2 * (self._limes + 1), 22)
        self.inRect = pg.Rect(self._pos[0], self._pos[1], 2 * (self._limes), 20)
        self.saldoRect = (self._pos[0], self._pos[1], 2 * (self._saldo), 20)
    def draw(self):
        if not self._saldo:
            return
        pg.draw.rect(self._screen, (0,0,0), self.outRect)
        pg.draw.rect(self._screen, (255,0,0), self.inRect)
        pg.draw.rect(self._screen, (0,128,0), self.saldoRect)
    def saldo(self, val):
        bank, betrag = val
        if bank:
            self._saldo -= betrag
        else:
            self._saldo += betrag
        if self._saldo < 0:
            self._saldo = 0
        if self._saldo > self._limes:
            self._saldo = self._limes
        self.saldoRect = (self._pos[0], self._pos[1], 2 * (self._saldo), 20)
    saldo = property(None, saldo)

class Card(object):
    def __init__(self, number):
        self._val = number % 13 + 2
        self._color = number // 13 + 1
        fileName = os.path.join(PIC_FOLDER, "{:d}.png".format(self._color * 100 + self._val))
        self._pic = pg.image.load(fileName)
    def __repr__(self):
        karten_namen = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        farbe = ['Kreuz', 'Grün', 'Herz', 'Karo']
        name = str(self._val) if self._val < 10 else karten_namen[self._val]
        return "{:s} {:s}".format(farbe[self._color - 1], name)
    @property
    def val(self):
        return self._val
    @property
    def color(self):
        return self._color
    @property
    def pic(self):
        return self._pic

class Game(object):
    def __init__(self, scr):
        self._screen = scr
        self._money = Money(self._screen, GAUGE)
        self._msg = Msgbox(self._screen, MSG_RECT)
        self._cards = [ (Card(x)) for x in range(52) ]
        self._deck = []
        self._dealer = False
        self._winner = False
        self._lock = False
        self._board = []
        self._dummy_pic = pg.image.load(os.path.join(PIC_FOLDER,'000.png'))
        self._data = { False: {'poket': [], 'best_Card': [], 'best_Rang': -1 }, 
                        True: {'poket': [], 'best_Card': [], 'best_Rang': -1 }}

    def findWinner(self):
        if self._data[False]['best_Rang'] > self._data[True]['best_Rang']:
            self._winner = False
        elif self._data[False]['best_Rang'] < self._data[True]['best_Rang']:
            self._winner = True
        else:
            #self._winner = True
            for x in range(5):
                if self._data[False]['best_Card'][x].val != self._data[True]['best_Card'][x].val:
                    self._winner = False if self._data[False]['best_Card'][x].val > \
                    self._data[True]['best_Card'][x].val else True
                    return
            self._msg.patt = True
    def newGame(self):
        self._msg.patt = False
        if len(self._deck) < 10:
            nd = [ (x) for x in range(52) ]
            random.shuffle(nd)
            self._deck = nd
        l = []
        for _ in range(9):
            l.append(self._cards[self._deck.pop()])
        self._board = l[:5] 
        self._data[False]['poket'] = l[5:7] 
        self._data[True]['poket'] = l[7:9] 
        for x in [False, True]:
            self._data[x]['best_Card'] = []
            self._data[x]['best_Rang'] = -1
            self.beste_5_aus_7_ermitteln(x)
        self.findWinner()
        r0 = self._data[False]['best_Rang']
        r1 = self._data[True]['best_Rang']
        self._msg.setMsg(self._winner, r0, r1)
        self._dealer = False
        
    def biet(self, val):
        if not self._dealer:
            self._lock = False
            self._money.saldo = (self._winner, val)
            self._dealer = True

    def draw(self):
        if not self._board:
            return
        self._money.draw() 
        for counter, item in enumerate(self._board):
            self._screen.blit(item.pic.convert_alpha(), (counter * 82 + LEFT_BOARD, TOP_BOARD))
        for counter, item in enumerate(self._data[False]['poket']):
            self._screen.blit(item.pic.convert_alpha(), (counter * 82 + LEFT_POKET[0], TOP_POKET))
        for x in range(2):
            self._screen.blit(self._dummy_pic.convert_alpha(),(x * 82 + LEFT_POKET[1], TOP_POKET))  
        if self._dealer:
            for counter, item in enumerate(self._data[False]['best_Card']):
                self._screen.blit(item.pic.convert_alpha(), (counter * 82 + LEFT_BEST[0], TOP_BEST))
            for counter, item in enumerate(self._data[True]['poket']):
                self._screen.blit(item.pic.convert_alpha(), (counter * 82 + LEFT_POKET[1], TOP_POKET))
            for counter, item in enumerate(self._data[True]['best_Card']):
                self._screen.blit(item.pic.convert_alpha(), (counter * 82 + LEFT_BEST[1], TOP_BEST))
            self._msg.draw()

    def bewerte5(self, karten5):
        wert2karten = defaultdict(list)
        anz2karten = defaultdict(list)
        for k in karten5:
            wert2karten[k.val].append(k)
        for v in wert2karten.values():
            anz2karten[len(v)] += v
        werte = { k.val for k in karten5 }  
        straight = (len(werte) == 5 and max(werte) - min(werte) == 4) or (werte == { 5, 4, 3, 2, 14 })
        farben = { k.color for k in karten5 }
        flush = len(farben) == 1            
        #Royal Flush
        if straight and flush and min(werte) == 10:
            return 9, karten5
        #Straight Flush
        if straight and flush:  
            if werte == {5, 4, 3, 2, 14}:
                karten5 = karten5[1:]+karten5[:1]
            return 8, karten5  
        #Four of a Kind
        if 4 in anz2karten:
            return 7, anz2karten[4] + anz2karten[1]  
        #Full House
        if 3 in anz2karten and 2 in anz2karten:
            return 6, anz2karten[3] + anz2karten[2]  
        #Flush
        if flush:
            return 5, karten5
        #Straight
        if straight:
            if werte == { 5, 4, 3, 2, 14 }:
                karten5 = karten5[1:]+karten5[:1]
            return 4, karten5
        #Tree of a Kind
        if 3 in anz2karten:
            return 3, anz2karten[3] + anz2karten[1]  
        #Two Pair
        if 2 in anz2karten and len(anz2karten[2]) == 4:
            return 2, anz2karten[2] + anz2karten[1]  
        #One Pair
        if 2 in anz2karten:
            return 1, anz2karten[2] + anz2karten[1]  
        #High Card
        return 0, karten5

    def beste_5_aus_7_ermitteln(self, player):
        karten7 = self._data[player]['poket'] + self._board
        karten7 = sorted(karten7, key=lambda k:k.val, reverse = True)
        bester_rang = -1
        for karten5 in combinations(karten7, 5):
            rang,karten = self.bewerte5(karten5)
            if rang > bester_rang:
                bester_rang = rang
                beste_karten = karten
        self._data[player]['best_Rang'] = bester_rang
        self._data[player]['best_Card'] = beste_karten   

    @property
    def dealer(self):
        return self._dealer
    @dealer.setter
    def dealer(self, val):
        self._dealer = val
    @property
    def lock(self):
        return self._lock
    @lock.setter
    def lock(self, val):
        self._lock = val

def main():
    random.seed()
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pg.display.set_caption(DISPLAY_CAPTION)
    screen = pg.display.get_surface()
    bg_pic = pg.image.load(os.path.join(PIC_FOLDER,'bg_poker1.jpg'))
    game = Game(screen)
    help = Help(screen)
    click = False
    running = True
    while running:
        if click:
            click = False
            mx, my = pg.mouse.get_pos()
            if not (560 < my < 620):
                continue
            if (30 < mx < 180) and not game.lock:
                game.lock = True
                game.newGame()
            elif (240 < mx < 300):
                game.biet(1)
            elif (326 < mx < 386):
                game.biet(3)
            elif (410 < mx < 470):
                game.biet(5)
            elif (500 < mx < 560):
                game.biet(10)
            elif (580 < mx < 640):
                game.biet(25)
            elif (700 < mx < 850):
                help.switch()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == BUTTON.LEFT:
                    click = True
        screen.blit(bg_pic.convert(),(0, 0))
        game.draw()
        help.draw()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()

if __name__ == "__main__":
    main()
    sys.exit()
