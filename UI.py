import pygame as pg

class ChknStats:
    def __init__(self, display):
        self.display = display

        self.yolk_surf = pg.image.load(f'assets/chicken/yolk.png').convert_alpha()
        self.yolk_rect = self.yolk_surf.get_rect(topleft = (1, 3))
        self.leg_surf = pg.image.load(f'assets/chicken/leg.png').convert_alpha()
        self.leg_rect = self.leg_surf.get_rect(topleft = (20, 1))
        self.cash_surf = pg.image.load(f'assets/chicken/cash.png').convert_alpha()
        self.cash_rect = self.cash_surf.get_rect(topleft = (1, 11))

        self.font = pg.font.Font('fonts/m5x7.ttf', 15)
        self.yk_count_surf = self.font.render('1', False, 'white')
        self.yk_count_rect = self.yk_count_surf.get_rect(topleft = (8, -2))
        self.lg_count_surf = self.font.render('0', False, 'white')
        self.lg_count_rect = self.yk_count_surf.get_rect(topleft = (30, -2))
        self.cs_count_surf = self.font.render('$0', False, 'white')
        self.cs_count_rect = self.cs_count_surf.get_rect(topleft = (13, 8))
    
    def egg_count(self, count):
        self.yk_count_surf = self.font.render(f'{count}', False, 'white')

    def leg_count(self, count):
        self.lg_count_surf = self.font.render(f'{count}', False, 'white')

    def cash_count(self, count):
        self.cs_count_surf = self.font.render(f'${count}', False, 'white')

    def update(self):
        self.display.blit(self.yk_count_surf, self.yk_count_rect)
        self.display.blit(self.lg_count_surf, self.lg_count_rect)
        self.display.blit(self.cs_count_surf, self.cs_count_rect)
        self.display.blit(self.yolk_surf, self.yolk_rect)
        self.display.blit(self.leg_surf, self.leg_rect)
        self.display.blit(self.cash_surf, self.cash_rect)

class ShpStats:
    def __init__(self, display, max):
        self.display = display
        self.max = max

        self.font = pg.font.Font('fonts/m5x7.ttf', 15)
        self.shp_count_surf = self.font.render(f'0/{self.max}', False, 'white')
        self.shp_count_rect = self.shp_count_surf.get_rect(topleft = (2, 0))

    def shp_count(self, collected, max):
        self.max = max
        self.shp_count_surf = self.font.render(f'{collected}/{self.max}', False, 'white')

    def update(self):
        self.display.blit(self.shp_count_surf, self.shp_count_rect)

class CowStats:
    def __init__(self, display, start_count):
        self.display = display

        self.cash_surf = pg.image.load(f'assets/chicken/cash.png').convert_alpha()
        self.cash_rect = self.cash_surf.get_rect(topleft = (1, 1))
        self.face_surf = pg.image.load(f'assets/cow/face_icon.png').convert_alpha()
        self.face_rect = self.face_surf.get_rect(topleft = (3, 9))

        self.font = pg.font.Font('fonts/m5x7.ttf', 15)
        self.cw_count_surf = self.font.render(f'{start_count}', False, 'white')
        self.cw_count_rect = self.cw_count_surf.get_rect(topleft = (13, 7))
        self.cs_count_surf = self.font.render('$0', False, 'white')
        self.cs_count_rect = self.cs_count_surf.get_rect(topleft = (13, -2))

    def cow_count(self, count):
        self.cw_count_surf = self.font.render(f'{count}', False, 'white')

    def cash_count(self, count):
        self.cs_count_surf = self.font.render(f'${count}', False, 'white')
    
    def update(self):
        self.display.blit(self.cw_count_surf, self.cw_count_rect)
        self.display.blit(self.cs_count_surf, self.cs_count_rect)
        self.display.blit(self.cash_surf, self.cash_rect)
        self.display.blit(self.face_surf, self.face_rect)

class Button:
    def __init__(self, display):
        self.display = display

        font = pg.font.Font('fonts/m5x7.ttf', 15)
        self.txt_surf = font.render('Hit ENTER', False, 'black')
        x, y = self.txt_surf.get_size()
        self.txt_size = self.width, self.height = x + 3, y + 2
        self.pos = (8, 43)

    def update(self):
        pg.draw.rect(self.display, 'white', pg.Rect((self.pos[0] - 2, self.pos[1] - 1), self.txt_size))
        pg.draw.rect(self.display, 'black', pg.Rect((self.pos[0] - 2, self.pos[1] - 1), self.txt_size), 1)
        self.display.blit(self.txt_surf, self.pos)