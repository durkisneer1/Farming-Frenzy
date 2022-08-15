import pygame as pg
from settings import *
from plots import ChickenPlot, SheepPlot, CowPlot
from trans import Transition, LevelInfo
from cursor import Cursor
from screens import TitleScreen

pg.mixer.pre_init(48000, -16, 2, 512)
pg.init()
screen = pg.display.set_mode((HEIGHT, WIDTH), pg.SCALED)
pg.display.set_caption('Farmer Frenzy')
pg.display.set_icon(pg.image.load('assets/chicken/egg.png'))
clock = pg.time.Clock()
pg.mouse.set_visible(False)

class Game:
    def __init__(self):
        
        self.chicken_plot = ChickenPlot(screen)
        self.sheep_plot = SheepPlot(screen)
        self.cow_plot = CowPlot(screen)

        self.trans_fade = Transition(screen)
        self.level_info = LevelInfo(None, screen, None)
        self.cursor = Cursor(screen)

        self.title_screen = TitleScreen(screen)

        self.current_time = 0
        
        self.music_played = False
        pg.mixer.music.set_volume(0.5)

    def menu(self):

        pg.mixer.music.unload()
        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.main()
            
            self.title_screen.update()
            self.cursor.update(pg.mouse.get_pos())

            pg.display.flip()
            clock.tick(30)

    def main(self):

        screen.fill('black')
        self.trans_fade.alpha = 255
        self.transition('  SELL\nCHICKEN!!', (9, 14))

        level_1 = True
        level_2 = False
        level_3 = False
        back_to_menu = False
        running = True
        while running:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

            mpos = pg.mouse.get_pos()
            mpressed = pg.mouse.get_pressed()

            if level_1:
                if self.music_played == False:
                    pg.mixer.music.unload()
                    pg.mixer.music.load('audio/music/Lay Down And Egg.mp3')
                    pg.mixer.music.play(-1)
                    self.music_played = True

                self.chicken_plot.update(events, mpos)
                self.trans_fade.update('out')
                if self.chicken_plot.cash_count == 20: # set for 20
                    level_1 = False
                    self.transition(' Herd\nSheep!!', (15, 14))
                    level_2 = True
                    self.music_played = False
            elif level_2:
                if self.music_played == False:
                    pg.mixer.music.unload()
                    pg.mixer.music.load('audio/music/Peace Be Herd.mp3')
                    pg.mixer.music.play(-1)
                    self.music_played = True

                self.sheep_plot.update(events)
                self.trans_fade.update('out')
                if self.sheep_plot.level == 4: # set for 4
                    level_2 = False
                    self.transition(' Milk\nCows!!', (18, 14))
                    level_3 = True
                    self.music_played = False
            elif level_3:
                if self.music_played == False:
                    pg.mixer.music.unload()
                    pg.mixer.music.load('audio/music/Rush Hour.mp3')
                    pg.mixer.music.play(-1)
                    self.music_played = True

                self.cow_plot.update(events, mpressed, mpos, self.cursor.rect)
                self.trans_fade.update('out')
                if self.cow_plot.points == 50: # set for 50
                    level_3 = False
                    self.transition(' You\nWon !!', (17, 14))
                    back_to_menu = True
                elif self.cow_plot.final_cow:
                    level_3 = False
                    self.transition(' You\nLost .', (17, 14))
                    back_to_menu = True
                    self.music_played = False
            elif back_to_menu:
                self.chicken_plot = ChickenPlot(screen)
                self.sheep_plot = SheepPlot(screen)
                self.cow_plot = CowPlot(screen)
                running = False
                
            self.cursor.update(mpos)

            pg.display.flip()
            clock.tick(30)

    def transition(self, txt, pos):
        
        pg.mixer.music.unload()
        trans_time = 0
        check = True
        transitioning = True
        while transitioning:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

            self.current_time = pg.time.get_ticks()
            if trans_time == 0:
                self.trans_fade.update('in')
            else:
                if self.current_time - trans_time > 3000: # set for 3000
                    transitioning = False

            if self.trans_fade.alpha == 255:
                if check == True:
                    trans_time = pg.time.get_ticks()
                    check = False
                self.level_info = LevelInfo(screen, txt, pos)
                self.level_info.update()
            
            pg.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    launch = Game()
    launch.menu()