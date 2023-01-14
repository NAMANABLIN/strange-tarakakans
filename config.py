import json
import os
import sys

import pygame as pg


def split_list(lst: list, n: int):  # список lst делится на n, функция возращает генератор
    for x in range(0, len(lst), n):
        e_c = lst[x: n + x]

        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


def load_image(name: str):
    fullname = os.path.join('resources/images/png', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}'")
        sys.exit()
    image = pg.image.load(fullname)
    return image


def load_level(filename: str) -> list:
    filename = os.path.join('resources/levels', filename)
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден.\n Возможно этого уровня нет в папке 'levels'")
        sys.exit()
    else:
        layers = json.load(open(filename, 'r', encoding='utf-8'))['layers'][0]
        level_map = list(split_list(layers['data'], layers['width']))
    return level_map


def change_brightness(image, extent):
    brightness_multiplier = 1.0
    brightness_multiplier += (extent / 100)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            cord = (x, y)
            pixel = image.get_at(cord)
            if pixel[3] != 0:
                new_pixel = (int(pixel[0] * brightness_multiplier),
                             int(pixel[1] * brightness_multiplier),
                             int(pixel[2] * brightness_multiplier),
                             255)
                image.set_at(cord, new_pixel)
    return image


# def load_control(filename: str) -> list:
#     if not os.path.isfile(filename):
#         print(f"Файл '{filename}' не найден.")
#         sys.exit()
#     else:
#         control_list =
#     return level_map


size = W, H = 800, 600
speed = 15
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

RAD2DEG = 360 / 3.14
keys = {
    'Q': pg.K_q, 'W': pg.K_w, 'E': pg.K_e, 'R': pg.K_r,
    'T': pg.K_t, 'Y': pg.K_y, 'U': pg.K_u, 'I': pg.K_i,
    'O': pg.K_o, 'P': pg.K_p, 'A': pg.K_a, 'S': pg.K_s,
    'D': pg.K_d, 'F': pg.K_f, 'G': pg.K_g, 'H': pg.K_h,
    'J': pg.K_j, 'K': pg.K_k, 'L': pg.K_l, 'Z': pg.K_z,
    'X': pg.K_x, 'C': pg.K_c, 'V': pg.K_v, 'B': pg.K_b,
    'N': pg.K_n, 'M': pg.K_m
}

game_over_image = pg.Surface(size)
game_over_image.fill(BLACK)
game_over_image.set_alpha(100)

logo = pg.transform.scale(load_image('logo.png'), (32, 32))

gg_right = [load_image(f'gg_right_0{i}.png') for i in range(2, 4)]
gg_left = [load_image(f'gg_left_0{i}.png') for i in range(2, 4)]
gg_stand = [load_image(f'gg_stand_0{i}.png') for i in range(1, 3)]

tarakan_right = [load_image(f'tarakan_right_0{i}.png') for i in range(2, 4)]
tarakan_stand = [load_image(f'tarakan_stand_0{i}.png') for i in range(1, 3)]

bullet = load_image('bullet.png')
player_weapon = load_image('gun.png')
player_weapon_reverse = pg.transform.flip(player_weapon, False, True)

fon = load_image('fon.png')
tiles = [load_image(f'tile_0{i}.png') for i in range(1, 11)]

tile_width = tile_height = 32
pg.init()
font = pg.font.SysFont("Comic Sans MS", 30)
font_color = (192, 165, 97)

all_sprites = pg.sprite.Group()
enemys_group = pg.sprite.Group()
player_group = pg.sprite.Group()
bullets_group = pg.sprite.Group()
wall_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()


def updates(sc, player=None):
    tiles_group.draw(sc)
    wall_group.draw(sc)
    bullets_group.draw(sc)
    enemys_group.draw(sc)
    if player is not None:
        bullets_group.update(player)
        enemys_group.update(player)
        player_group.draw(sc)


def clear():
    tiles_group.empty()
    wall_group.empty()
    bullets_group.empty()
    enemys_group.empty()
    bullets_group.empty()
    player_group.empty()
