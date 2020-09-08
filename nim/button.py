import pygame as pg
vec = pg.math.Vector2


class Button:
    def __init__(self, surface, x, y, width, height, state = '', function = 0, colour = (255, 255, 255), hover_colour = (255, 255, 255),
                border = True, border_width = 2, border_colour = (0, 0, 0),
                text = '', font_name = 'FreeSans', text_size = 20, text_colour = (0, 0, 0), bold_text = False):
        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.width = width
        self.height = height
        self.surface = surface
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.state = state
        self.function = function
        self.colour = colour
        self.hover_colour = hover_colour
        self.border = border
        self.border_width = border_width
        self.border_colour = border_colour
        self.text = text
        self.font_name = font_name
        self.text_size = text_size
        self.text_colour = text_colour
        self.bold_text = bold_text
        self.hovered = False

    def update(self):
        pos = pg.mouse.get_pos()
        if self.mouse_hovering(pos):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self):
        if self.border:
            self.image.fill(self.border_colour), 
            p0, p1 = self.width - self.border_width * 2, self.height - self.border_width * 2
            p0, p1 = self.width - self.border_width * 2, self.height - self.border_width * 2
            if self.hovered:
                pg.draw.rect(self.image, self.hover_colour, (self.border_width, self.border_width, p0, p1))
            else:
                pg.draw.rect(self.image, self.colour, (self.border_width, self.border_width, p0, p1))
        else:
            self.image.fill(self.colour)
        if len(self.text) > 0:
            self.show_text()
        self.surface.blit(self.image, self.pos)

    def show_text(self):
        font = pg.font.SysFont(self.font_name, self.text_size, bold = self.bold_text)
        text = font.render(self.text, False, self.text_colour)
        size = text.get_size()
        x = self.width // 2 - size[0] // 2
        y = self.height // 2 - size[1] // 2
        pos = vec(x, y)
        self.image.blit(text, pos)

    def mouse_hovering(self, pos):
        if pos[0] > self.pos[0] and pos[0] < self.pos[0] + self.width:
            if pos[1] > self.pos[1] and pos[1] < self.pos[1] + self.height:
                return True
        return False                        
    
    def click(self):
        if self.function != 0:
            self.function()

    def getPos(self):
        return (self.x, self.x + self.width, self.y, self.y + self.height)
    