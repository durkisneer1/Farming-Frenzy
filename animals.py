import pygame as pg
import random
from settings import WIN_WIDTH, WIN_HEIGHT
from backend import circles_overlap, import_folder


class Chicken(pg.sprite.Sprite):
    def __init__(self, display_surf, group):
        super().__init__(group)

        self.display = display_surf
        self.sprite_list = []
        self.sprite_import("white")
        self.sprite_import("brown")
        self.sprite_import("gray")
        self.surf = self.sprite_list[random.randint(0, 2)]
        self.rect = self.surf.get_rect()
        self.size = self.surf.get_size()

        self.x_speed, self.y_speed = 0.2, 0.2
        self.pos = pg.Vector2(
            random.randint(0, WIN_WIDTH) - (self.size[0] / 2),
            random.randint(0, WIN_HEIGHT) - (self.size[1] / 2),
        )

    def sprite_import(self, filename):
        sprite = pg.transform.flip(
            pg.image.load(f"assets/chicken/{filename}.png").convert_alpha(), True, False
        )
        self.sprite_list.append(sprite)

    def update(self):
        self.pos.x += self.x_speed
        self.pos.y += self.y_speed
        self.rect.topleft = self.pos

        if self.rect.left < 4:
            self.pos.x = 4
            self.x_speed *= -1
            self.surf = pg.transform.flip(self.surf, True, False)
        elif self.rect.right > WIN_WIDTH - 4:
            self.pos.x = WIN_WIDTH - self.size[0] - 4
            self.x_speed *= -1
            self.surf = pg.transform.flip(self.surf, True, False)
        elif self.rect.bottom > WIN_HEIGHT - 4:
            self.pos.y = WIN_HEIGHT - self.size[1] - 4
            self.y_speed *= -1
        elif self.rect.top < 4:
            self.pos.y = 4
            self.y_speed *= -1

        self.display.blit(self.surf, self.rect)


class Sheep(pg.sprite.Sprite):
    def __init__(self, display, spawn_pos, group):
        super().__init__(group)
        self.display = display

        color = random.randint(100, 255)
        self.surf = pg.Surface((4, 4))
        self.surf.fill((color, color, color))
        self.rect = self.surf.get_rect()
        self.size = self.surf.get_size()

        self.face_surf = pg.image.load("assets/sheep/sheep_face.png").convert()

        self.speed = 0.25
        self.radius = 1.5
        self.pos = pg.Vector2(
            spawn_pos[0] - (self.size[0] / 2), spawn_pos[1] - (self.size[1] / 2)
        )
        self.vel = pg.Vector2(self.speed, 0)
        self.vel.rotate_ip(360 * random.random())

    def input(self, mpos, mradius):
        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.top <= 0:
            self.vel.y = abs(self.vel.y)
        elif self.rect.bottom >= WIN_HEIGHT:
            self.vel.y = -abs(self.vel.y)
        if self.rect.left <= 0:
            self.vel.x = abs(self.vel.x)
        elif self.rect.right >= WIN_WIDTH:
            self.vel.x = -abs(self.vel.x)

        if circles_overlap(self.pos, self.radius, mpos, mradius):
            new_vel = self.pos - mpos
            if new_vel.magnitude() > 0:
                new_vel.scale_to_length(self.speed)
                self.vel = new_vel

    def update(self, mpos, mradius):
        self.input(mpos, mradius)
        self.display.blit(self.surf, self.rect)
        self.surf.blit(self.face_surf, (1, 1))


class Cow(pg.sprite.Sprite):
    def __init__(self, display_surf, group):
        super().__init__(group)
        self.display = display_surf

        colors = ["black", "brown", "white"]
        color = colors[random.randint(0, 2)]
        self.surf_list = import_folder(f"assets/cow/{color}")
        self.rect = None

        self.current_frame = 0
        self.img = self.surf_list[self.current_frame]
        self.anim_speed = 0.2

        self.x = random.randint(0, WIN_WIDTH - 31)
        self.y = 0

    def cow_anim(self):
        frames = self.surf_list
        self.current_frame += self.anim_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        self.img = frames[int(self.current_frame)]
        self.rect = self.img.get_rect(bottomleft=(self.x, self.y))
        self.y += 1

    def update(self):
        self.cow_anim()
        self.display.blit(self.img, self.rect)
