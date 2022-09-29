import pygame as pg

class Cursor:
    def __init__(self, display_surf):
        self.display = display_surf
        
        self.surf = pg.image.load('assets/controls/Hand.png').convert_alpha()
        self.rect = self.surf.get_rect()
    
    def tracking(self, mpos):
        x, y = mpos
        self.rect.topleft = x - 4, y - 2

    def update(self, mpos):
    
        self.tracking(mpos)
        self.display.blit(self.surf, self.rect)