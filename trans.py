import pygame as pg
from settings import *
from backend import *

class Transition:
    def __init__(self, display_surf):

        self.display = display_surf

        self.surf = pg.Surface((WIDTH, HEIGHT))
        self.surf.fill('black')

        self.speed = 5
        self.alpha = 0
        self.surf.set_alpha(self.alpha)

    def fadein(self):

        if self.alpha < 255:
            self.alpha += self.speed
            self.alpha = min(self.alpha, 255)
            self.surf.set_alpha(self.alpha)

    def fadeout(self):

        if self.alpha > 0:
            self.alpha -= self.speed
            self.alpha = min(self.alpha, 255)
            self.surf.set_alpha(self.alpha)
    
    def update(self, type):
        
        if type == 'in':
            self.fadein()
        elif type == 'out':
            self.fadeout()
        self.display.blit(self.surf, (0, 0))

class LevelInfo:
    def __init__(self, display_surf, txt, pos):

        self.display = display_surf
        self.font = pg.font.Font('fonts/m5x7.ttf', 16)

        self.txt = txt
        self.pos = pos

    def update(self):

        blit_text(self.display, self.txt, self.pos, self.font)