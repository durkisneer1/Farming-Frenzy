import pygame as pg
import random
from settings import *
from backend import *
from animals import Chicken, Sheep, Cow
from UI import ChknStats, ShpStats, CowStats
from extras import Egg, BarnCollisions, AssemblyLine, Bucket

class ChickenPlot:
    def __init__(self, display_surf):

        self.display = display_surf
        self.animal_group = pg.sprite.Group()
        self.egg_group = pg.sprite.Group()
        self.sorted_animals = None
        self.sorted_eggs = None
        self.import_plot()

        self.egg_count = 1
        self.leg_count = 0
        self.cash_count = 0

        self.EGG_SPAWN = pg.USEREVENT + 1
        pg.time.set_timer(self.EGG_SPAWN, 10000) # set for 11000

        self.stats = ChknStats(self.display)

    def import_plot(self):

        self.grass = pg.image.load('assets/terrain/chicken/grass.png').convert()
        self.bg_fence = pg.image.load('assets/terrain/chicken/bg_fence.png').convert_alpha()
        self.fg_fence = pg.image.load('assets/terrain/chicken/fg_fence.png').convert_alpha()

    def spawn_chicken(self):

        Chicken(self.display, self.animal_group)
        self.egg_count -= 1
        self.stats.egg_count(self.egg_count)

    def kill_chicken(self, mpos):
        
        for sprite in reversed(self.sorted_animals):
            if sprite.rect.collidepoint(mpos):
                sprite.kill()
                self.leg_count += 1
                self.stats.leg_count(self.leg_count)
                break
    
    def collect_egg(self, mpos):

        for sprite in reversed(self.sorted_eggs):
            if sprite.rect.collidepoint(mpos):
                sprite.kill()
                self.egg_count += 1
                self.stats.egg_count(self.egg_count)
                break

    def input(self, events, mpos):

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.leg_count < 10:
                        if len(self.animal_group.sprites()) > 1:
                            self.kill_chicken(mpos)
                elif event.button == 3:
                    if self.egg_count < 10:
                        if self.egg_group.sprites() != []:
                            self.collect_egg(mpos)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if self.egg_count > 0 and len(self.animal_group.sprites()) < 10:
                        self.spawn_chicken()
                elif event.key == pg.K_SPACE:
                    if self.leg_count == 10:
                        self.cash_count += 2
                        self.stats.cash_count(self.cash_count)
                        self.leg_count = 0
                        self.stats.leg_count(self.leg_count)
            
            elif event.type == self.EGG_SPAWN:
                if len(self.egg_group) < 8:
                    if len(self.animal_group) < 4:
                        for sprite in random.sample(self.animal_group.sprites(), len(self.animal_group)):
                            Egg(self.display, sprite.rect.center, self.egg_group)
                    else:
                        for sprite in random.sample(self.animal_group.sprites(), 4):
                            Egg(self.display, sprite.rect.center, self.egg_group)

    def update(self, events, mpos):

        self.display.blit(self.grass, (0, 0))
        self.display.blit(self.bg_fence, (0, 0))

        self.input(events, mpos)

        self.sorted_animals = sorted(self.animal_group.sprites(), key = lambda a: a.rect.y)
        self.sorted_eggs = sorted(self.egg_group.sprites(), key = lambda a: a.rect.y)
        for animal in self.sorted_animals:
            animal.update()
        for egg in self.sorted_eggs:
            egg.update()

        self.display.blit(self.fg_fence, (0, 0))
        self.stats.update()

class SheepPlot:
    def __init__(self, display_surf):

        self.display = display_surf
        self.sheep_group = pg.sprite.Group()

        self.level = 1
        self.spawn()
        self.import_plot()
        self.barn_collision = BarnCollisions(self.display)

        self.mouse_pos = pg.Vector2(0, 0)
        self.mouse_radius = 4

        self.score = 0

        self.shp_stats = ShpStats(self.display, 10)

    def import_plot(self):

        self.grass = pg.image.load('assets/terrain/sheep/grass.png').convert()
        self.barn = pg.image.load('assets/terrain/sheep/barn.png').convert_alpha()
        self.goal = pg.image.load('assets/sheep/goal.png').convert_alpha()

        self.barn_rect = self.barn.get_rect(topleft=(44, 3))
        self.goal_rect = self.goal.get_rect(topleft=(45, 23))

    def spawn(self):
        
        if self.level == 1:
            for _ in range(10):
                pos = (random.randint(2, WIDTH-23), random.randint(2, HEIGHT-4))
                Sheep(self.display, pos, self.sheep_group)
        elif self.level == 2:
            self.score = 0
            self.shp_stats.shp_count(self.score, 25)
            for _ in range(25):
                pos = (random.randint(2, WIDTH-23), random.randint(2, HEIGHT-4))
                Sheep(self.display, pos, self.sheep_group)
        elif self.level == 3:
            self.score = 0
            self.shp_stats.shp_count(self.score, 50)
            for _ in range(50):
                pos = (random.randint(2, WIDTH-23), random.randint(2, HEIGHT-4))
                Sheep(self.display, pos, self.sheep_group)

    def collect_score(self):

        for sprite in self.sheep_group:
            if sprite.rect.colliderect(self.goal_rect):
                if (sprite.rect.right >= self.goal_rect.right
                    or sprite.rect.top <= self.goal_rect.top
                    or sprite.rect.bottom >= self.goal_rect.bottom):
                    sprite.kill()
                    self.score += 1

                    if self.level == 1:
                        self.shp_stats.shp_count(self.score, 10)
                        if self.score == 10:
                            self.level = 2
                            self.spawn()
                    elif self.level == 2:
                        self.shp_stats.shp_count(self.score, 25)
                        if self.score == 25:
                            self.level = 3
                            self.spawn()
                    elif self.level == 3:
                        self.shp_stats.shp_count(self.score, 50)
                        if self.score == 50:
                            self.level = 4 # end

    def collisions(self):

        for sprite1 in self.sheep_group:
            for sprite2 in self.sheep_group:
                if sprite1 is not sprite2:
                    # they're overlapping
                    if circles_overlap(sprite1.pos, sprite1.radius, sprite2.pos, sprite2.radius):
                        norm = sprite1.pos - sprite2.pos

                        if norm.magnitude() > 0:
                            # push them apart so they're not overlapping
                            overlap_dist = get_circle_overlap_dist(sprite1.pos, sprite1.radius, sprite2.pos, sprite2.radius)
                            sprite1.pos += norm.normalize() * overlap_dist / 2
                            sprite2.pos -= norm.normalize() * overlap_dist / 2
                            # adjust velocities so they bounce
                            sprite1.vel = sprite1.vel.reflect(norm)
                            sprite2.vel = sprite2.vel.reflect(norm)

            if sprite1.rect.colliderect(self.barn_collision.rect1):
                if sprite1.rect.right >= self.barn_collision.rect1.left:
                    sprite1.vel.x = -abs(sprite1.vel.x)
            elif sprite1.rect.colliderect(self.barn_collision.rect2):
                if sprite1.rect.right >= self.barn_collision.rect2.left:
                    sprite1.vel.x = -abs(sprite1.vel.x)

    def cursor_push(self, events):

        new_mouse_pos = None
        for event in events:
            if event.type == pg.MOUSEMOTION:
                new_mouse_pos = pg.Vector2(event.pos)
        
        if new_mouse_pos is not None:
            self.mouse_pos = new_mouse_pos

    def update(self, events):

        self.cursor_push(events)
        self.barn_collision.update()
        self.collect_score()

        self.display.blit(self.grass, (0, 0))
        self.display.blit(self.goal, self.goal_rect)

        self.collisions()
        for sprite in self.sheep_group:
            sprite.update(self.mouse_pos, self.mouse_radius)

        self.display.blit(self.barn, self.barn_rect)
        self.shp_stats.update()

class CowPlot:
    def __init__(self, display_surf):

        self.display = display_surf
        self.cow_group = pg.sprite.Group()
        self.bucket_group = pg.sprite.Group()
        self.assembly_line = AssemblyLine(self.display)
        Bucket(self.display, self.bucket_group)

        self.points = 0
        self.cows_left = 35
        self.cow_stats = CowStats(self.display, self.cows_left)
        self.final_cow = False

        self.COW_SPAWN = pg.USEREVENT + 2
        pg.time.set_timer(self.COW_SPAWN, 850) # set for 1000

    def cow_manager(self, events):

        if self.cows_left > 0:
            for event in events:
                if event.type == self.COW_SPAWN:
                    Cow(self.display, self.cow_group)
                    self.cows_left -= 1
                    self.cow_stats.cow_count(self.cows_left)
        else:
            if len(self.cow_group) == 1:
                for sprite in self.cow_group:
                    if sprite.rect != None:
                        if sprite.rect.top > HEIGHT:
                            self.final_cow = True

        for sprite in self.cow_group:
            if sprite.rect != None:
                if sprite.rect.top > HEIGHT:
                    sprite.kill()

    def bucket_manager(self, mpressed, mpos):

        for sprite in self.bucket_group:
            if sprite.rect.top > HEIGHT:
                sprite.kill()
                if sprite.milked:
                    self.points += 5
                    self.cow_stats.cash_count(self.points)
            if not sprite.milked:
                for cow in self.cow_group:
                    if cow.rect != None:
                        if sprite.rect.colliderect(cow.rect):
                            if sprite.rect.collidepoint(mpos):
                                if not mpressed[0]:
                                    sprite.milked = True
            if sprite.milked and len(self.bucket_group) < 1 or len(self.bucket_group) == 0:
                Bucket(self.display, self.bucket_group)

    def update(self, events, mpressed, mpos, cursor_rect):
        
        self.display.fill((135, 100, 22))
        self.cow_manager(events)
        self.bucket_manager(mpressed, mpos)
        
        for sprite in self.cow_group:
            sprite.update()
        self.assembly_line.update()
        for sprite in self.bucket_group:
            sprite.update(mpressed, mpos, cursor_rect)
        self.cow_stats.update()