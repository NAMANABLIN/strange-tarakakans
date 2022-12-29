import pygame as pg
import sys
import os


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

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


MALAHIT = (24, 161, 86)
BLACK = (0, 0, 0)
WHITE = (0, 0, 0)
GREY = (100, 100, 100)

gg = pg.transform.scale(load_image('gg.png'), (24, 52))
gg_reverse = pg.transform.flip(gg, True, False)

tarakan = pg.transform.scale(load_image('tarakan.png'), (14, 26))
tarakan_reverse = pg.transform.flip(tarakan, True, False)

bullet = load_image('bullet.png')
player_weapon = load_image('gun.png')
player_weapon_reverse = pg.transform.flip(player_weapon, False, True)

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')}

tile_width = tile_height = 50
pg.init()
font = pg.font.SysFont("Comic Sans MS", 30)
font_color = (0, 0, 0)

all_sprites = pg.sprite.Group()
enemys_group = pg.sprite.Group()
player_group = pg.sprite.Group()
bullets_group = pg.sprite.Group()
wall_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()

correct_radius = range(-90,90+1)
kills  = 0