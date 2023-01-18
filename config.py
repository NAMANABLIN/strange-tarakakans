from defs import load_image
import pygame as pg

SIZE = W, H = 800, 600
FPS = 60

RAD2DEG = 360 / 3.14

GRAVITY = 0.5
SCREEN_RECT = (0, 0, W, H)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)

# клавиши управления сохраняются как заглавные латинские буквы,
# их нужно переобразовывать в кностанты из pygame
letter2konst = {
    'Q': pg.K_q, 'W': pg.K_w, 'E': pg.K_e, 'R': pg.K_r,
    'T': pg.K_t, 'Y': pg.K_y, 'U': pg.K_u, 'I': pg.K_i,
    'O': pg.K_o, 'P': pg.K_p, 'A': pg.K_a, 'S': pg.K_s,
    'D': pg.K_d, 'F': pg.K_f, 'G': pg.K_g, 'H': pg.K_h,
    'J': pg.K_j, 'K': pg.K_k, 'L': pg.K_l, 'Z': pg.K_z,
    'X': pg.K_x, 'C': pg.K_c, 'V': pg.K_v, 'B': pg.K_b,
    'N': pg.K_n, 'M': pg.K_m
}
mouse_buttons = {'ЛКМ': 0, 'ПКМ': 2}

game_over_image = pg.Surface(SIZE)
game_over_image.fill(BLACK)
game_over_image.set_alpha(100)

logo = pg.transform.scale(load_image('logo.png'), (32, 32))
fon = load_image('fon.png')

gg_right = [load_image(f'gg_right_0{i}.png') for i in range(2, 4)]
gg_left = [pg.transform.flip(x, True, False) for x in gg_right]
gg_stand = [load_image(f'gg_stand_0{i}.png') for i in range(1, 3)]

tarakan_right = [load_image(f'tarakan_right_0{i}.png') for i in range(2, 4)]
tarakan_stand = [load_image(f'tarakan_stand_0{i}.png') for i in range(1, 3)]

bulls = [load_image('particle.png')]
for scale in (7, 8, 10):
    bulls.append(pg.transform.scale(bulls[0], (scale, scale)))

bullet = load_image('bullet.png')
player_weapon = load_image('gun.png')
player_weapon_reverse = pg.transform.flip(player_weapon, False, True)

tiles = [load_image(f'tile_0{i}.png') for i in range(1, 11)]
tile_width = tile_height = 32

pg.init()
font = pg.font.SysFont("Comic Sans MS", 30)
font2 = pg.font.SysFont("Comic Sans MS", 50)
font_color = (203, 181, 128)
button_color = (28, 28, 28)

all_sprites = pg.sprite.Group()
enemies_group = pg.sprite.Group()
player_group = pg.sprite.Group()
bullets_group = pg.sprite.Group()
wall_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()
particles_group = pg.sprite.Group()

mixer = pg.mixer
mixer.init()
sound_path = 'resources/audio/sound/'
sounds = {'win': mixer.Sound(sound_path + 'victory_sJDDywi.wav'),
          'click': mixer.Sound(sound_path + 'sqek.wav'),
          'hit': mixer.Sound(sound_path + 'inecraft_hit_sound--online-audio-convert.com.wav'),
          'death': mixer.Sound(sound_path + 'inecraft_death--online-audio-convert.com.wav'),
          'save': mixer.Sound(sound_path + 'undertale-save.wav')}
mixer.music.load('resources/audio/music/Toby-Fox-Amalgam.wav')

def updates(sc, player=None):
    tiles_group.draw(sc)
    bullets_group.draw(sc)
    wall_group.draw(sc)
    enemies_group.draw(sc)
    particles_group.draw(sc)
    if player is not None:
        enemies_group.update(player)
        bullets_group.update(player)
        particles_group.update()
        player_group.draw(sc)


def clear():
    for x in [tiles_group, bullets_group, enemies_group, bullets_group,
              player_group, particles_group, wall_group, all_sprites]:
        x.empty()


def check_walls(new_rect):
    for x in wall_group:
        if x.rect.colliderect(new_rect):
            return False
    return True


def change_volume(volume):
    s, m = volume
    for x in sounds.keys():
        sounds[x].set_volume(s)
    mixer.music.set_volume(m)
