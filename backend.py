from os import walk
import pygame as pg


def circle_contains_point(c_xy, radius, xy):
    return c_xy.distance_to(xy) <= radius


def circles_overlap(c_xy1, radius1, c_xy2, radius2):
    return get_circle_overlap_dist(c_xy1, radius1, c_xy2, radius2) > 0


def get_circle_overlap_dist(c_xy1, radius1, c_xy2, radius2):
    dist = c_xy1.distance_to(c_xy2)
    return radius1 + radius2 - dist


def blit_text(display, text, pos, font):
    word_height = None
    words = [word.split(" ") for word in text.splitlines()]
    space = font.size(" ")[0]
    max_width = display.get_width()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, "white")
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            display.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height


def import_folder(path):
    surf_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = path + "/" + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)
    return surf_list
