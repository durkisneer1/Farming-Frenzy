import pygame as pg

pg.mixer.pre_init(48000, -16, 2, 512)
pg.init()

WIN_WIDTH, WIN_HEIGHT = 64, 64
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.SCALED)
pg.display.set_caption("Farming Frenzy")
icon_img = pg.transform.scale_by(pg.image.load("assets/chicken/egg.png"), 4)
pg.display.set_icon(icon_img)

clock = pg.time.Clock()
pg.mouse.set_visible(False)
