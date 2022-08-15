import pygame as pg
from UI import Button

class TitleScreen:
    def __init__(self, display_surf):
        
        self.display = display_surf
        self.surf = pg.image.load('assets/title/title.png').convert_alpha()
        self.bg = pg.image.load('assets/title/bg.png').convert()
        self.bg = pg.transform.scale(self.bg, (64, 64))

        self.button = Button(self.display)

    def update(self):

        self.display.blit(self.bg, (0, 0))
        self.display.blit(self.surf, (7, 4))
        self.button.update()