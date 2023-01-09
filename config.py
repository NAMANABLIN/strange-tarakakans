import os
import sys

import pygame as pg


def load_image(name, colorkey=None):
    fullname = os.path.join('resources/images/png', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}'")
        sys.exit()
    image = pg.image.load(fullname)
    return image


def load_level(filename):
    filename = os.path.join(filename)
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден.\n Возможно этого уровня нет в папке 'levels'")
        sys.exit()
    else:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return level_map

size = W, H = 800, 600
speed = 15
FPS = 60

BLACK = (0, 0, 0)
WHITE = (0, 0, 0)
GREY = (100, 100, 100)

game_over_image = pg.Surface(size)
game_over_image.fill(BLACK)
game_over_image.set_alpha(100)

logo = pg.transform.scale(load_image('logo.png'), (32, 32))

gg_right = [load_image(f'gg_right_0{i}.png') for i in range(2, 4)]
gg_left = [load_image(f'gg_left_0{i}.png') for i in range(2, 4)]
gg_stand = [load_image(f'gg_stand_0{i}.png') for i in range(1, 3)]
gg = load_image('gg_right_01.png')
gg_reverse = pg.transform.flip(gg, True, False)

tarakan = pg.transform.scale(load_image('enemy_01.png'), (42, 62))
tarakan_reverse = pg.transform.flip(tarakan, True, False)

bullet = load_image('bullet.png')
player_weapon = load_image('gun.png')
player_weapon_reverse = pg.transform.flip(player_weapon, False, True)

tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png')}

tile_width = tile_height = 32
pg.init()
font = pg.font.SysFont("Comic Sans MS", 30)
font_color = (0, 0, 0)

all_sprites = pg.sprite.Group()
enemys_group = pg.sprite.Group()
player_group = pg.sprite.Group()
bullets_group = pg.sprite.Group()
wall_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()

correct_radius = range(-90, 90 + 1)
kills = 0

def updates(sc, player=None):
    tiles_group.draw(sc)
    wall_group.draw(sc)
    bullets_group.draw(sc)
    enemys_group.draw(sc)
    if player is not None:
        bullets_group.update()
        enemys_group.update(player)
        player.draw(sc)
