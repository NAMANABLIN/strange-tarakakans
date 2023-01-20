import json
import os
import sys
import pygame as pg


# список lst делится на n, функция возращает генератор
def split_list(lst: list, n: int) -> list:
    for x in range(0, len(lst), n):
        e_c = lst[x: n + x]

        if len(e_c) < n:
            e_c = e_c + [None] * (n - len(e_c))
        yield e_c


def load_image(name: str) -> pg.image.load:
    fullname = os.path.join('resources/images/png', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pg.image.load(fullname)
    return image


def load_level(filename: str) -> list:
    filename = os.path.join('resources/levels', filename)
    if not os.path.isfile(filename):
        sys.exit()
    else:
        layers = json.load(open(filename, 'r', encoding='utf-8'))['layers'][0]
        level_map = list(split_list(layers['data'], layers['width']))
    return level_map


# осветление картинки
def change_brightness(image: pg.image.load, extent: int) -> pg.image.load:
    brightness_multiplier = 1.0
    brightness_multiplier += (extent / 100)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            cord = (x, y)
            pixel = image.get_at(cord)
            if pixel[3] != 0:
                p1 = int(pixel[0] * brightness_multiplier)
                p2 = int(pixel[1] * brightness_multiplier)
                p3 = int(pixel[2] * brightness_multiplier)
                new_pixel = (p1 if p1 < 255 else 255,
                             p2 if p2 < 255 else 255,
                             p3 if p3 < 255 else 255,
                             255)
                image.set_at(cord, new_pixel)
    return image
