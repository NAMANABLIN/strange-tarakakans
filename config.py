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


MALAHIT = (24, 161, 86)
BLACK = (0, 0, 0)
WHITE = (0, 0, 0)
GREY = (100, 100, 100)

gg = pg.transform.scale(load_image('gg.png'), (24, 52))
tarakan = pg.transform.scale(load_image('tarakan.png'), (14, 26))
tarakan_reverse = pg.transform.flip(tarakan, True, False)


bullet = load_image('bullet.png')
player_weapon = load_image('gun.png')

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