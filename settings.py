import pygame as pg

WIDTH, HEIGHT = 64, 64

pg.mixer.pre_init(48000, -16, 2, 512)
pg.init()

screen = pg.display.set_mode((HEIGHT, WIDTH), pg.SCALED)
pg.display.set_caption('Farming Frenzy')
pg.display.set_icon(pg.image.load('assets/chicken/egg.png'))

clock = pg.time.Clock()
pg.mouse.set_visible(False)