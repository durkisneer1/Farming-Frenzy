import pygame as pg
from backend import import_folder
import random
from settings import *

class Egg(pg.sprite.Sprite):
    def __init__(self, display_surf, pos, groups):
        super().__init__(groups)

        self.display = display_surf
        self.surf = pg.image.load(f'assets/chicken/egg.png').convert_alpha()
        self.rect = self.surf.get_rect(center = pos)

    def update(self):

        self.display.blit(self.surf, self.rect)

class BarnCollisions(pg.sprite.Sprite):
    def __init__(self, display_surf):

        self.display = display_surf
        self.surf1 = pg.Surface((20, 23))
        self.rect1 = self.surf1.get_rect(topright = (64, 0))
        self.surf2 = pg.Surface((20, 23))
        self.rect2 = self.surf2.get_rect(bottomright = (64, 64))

    def update(self):

        self.display.blit(self.surf1, self.rect1)
        self.display.blit(self.surf2, self.rect2)

class AssemblyLine:
    def __init__(self, display_surf):

        self.display = display_surf
        self.surf_list = import_folder(f'assets/terrain/cow/line')
        self.current_frame = 0
        self.anim_speed = 0.2
        self.rect = None

        self.x = random.randint(0, WIDTH - 31)
        self.y = 0

    def assembly_line_anim(self):

        frames = self.surf_list
        self.current_frame += self.anim_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        self.line_surf = frames[int(self.current_frame)]

    def update(self):
        
        self.assembly_line_anim()
        self.display.blit(self.line_surf, (WIDTH - 12, 0))

class Bucket(pg.sprite.Sprite):
    def __init__(self, display_surf, group):
        super().__init__(group)

        self.display = display_surf
        self.milked = False

        self.empty_surf = pg.image.load('assets/cow/buckets/empty.png').convert_alpha()
        self.milked_surf = pg.image.load('assets/cow/buckets/milked.png').convert_alpha()
        self.surf = self.empty_surf
        self.rect = self.surf.get_rect()

        self.pos = pg.Vector2(WIDTH - 6, 0)
    
    def grab(self, mpressed, mpos, cursor_rect):
        
        if not self.milked:
            if mpressed[0]:
                if self.rect.colliderect(cursor_rect):
                    self.pos.x, self.pos.y = mpos[0], mpos[1]
                    self.rect.center = self.pos
            else:
                if self.pos.x > WIDTH - 18:
                    self.pos.x = WIDTH - 6
                    self.pos.y += 0.4
                    self.rect.midbottom = self.pos

        else:
            self.surf = self.milked_surf
            if self.pos.x > WIDTH - 18:
                self.pos.x = WIDTH - 6
                self.pos.y += 0.4
                self.rect.midbottom = self.pos
            else:
                if mpressed[0]:
                    if self.rect.colliderect(cursor_rect):
                        self.pos.x, self.pos.y = mpos[0], mpos[1]
                        self.rect.center = self.pos

    def update(self, mpressed, mpos, cursor_rect):
        
        self.grab(mpressed, mpos, cursor_rect)
        self.display.blit(self.surf, self.rect)