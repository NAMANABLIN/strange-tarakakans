import math
from random import randint, choice
from time import time

from config import *
from defs import change_brightness


class Particle(pg.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(particles_group, all_sprites)
        self.image = choice(bulls)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = gg_stand[0]
        self.rect = pg.Rect(x, y, *self.image.get_size())
        self.speed = 4.2
        self.button2cords = [(0, -self.speed), (0, self.speed),
                             (-self.speed, 0), (self.speed, 0)]

        self.player_weapon_copy = player_weapon

        # таймер нужен чтобы после получения урона игрок не сразу же получи ещё,
        # пока таймер не равен 0 - игрок не уязвим
        self.timer = 0

        self.hp = 1
        self.death = False

        self.kills = 0

        # анимация
        self.left = False
        self.right = False
        self.animCount = 0

        self.death_time = 0

    def handle_weapons(self, display):
        weapon_x = self.rect.x + 25
        weapon_y = self.rect.y + 25

        mouse_x, mouse_y = pg.mouse.get_pos()

        rel_x = mouse_x - weapon_x
        rel_y = mouse_y - weapon_y
        angle = round((180 / math.pi) * -math.atan2(rel_y, rel_x))

        if -90 <= angle <= 90:
            self.player_weapon_copy = pg.transform.rotate(player_weapon, angle)
        else:
            if not self.left and not self.right:
                self.image = pg.transform.flip(self.image, True, False)
            self.player_weapon_copy = pg.transform.rotate(player_weapon_reverse, angle)

        display.blit(self.player_weapon_copy, (
            weapon_x - int(player_weapon.get_width() / 2),
            weapon_y - int(self.player_weapon_copy.get_height() / 2)))

    def main(self, display):
        if self.timer == 0:
            if pg.sprite.spritecollideany(self, enemies_group):
                self.get_damage()
        else:
            self.timer -= 1

        if self.left:
            self.image = gg_left[self.animCount // 30]
        elif self.right:
            self.image = gg_right[self.animCount // 30]
        else:
            self.image = gg_stand[round(self.animCount / 60)]
        self.animCount += 1

        if self.animCount == 60:
            self.animCount = 0
        self.handle_weapons(display)

    def move(self, keys, axis):
        not_move = True
        for i, x in enumerate(axis):
            cords = self.button2cords[i]
            if keys[x]:
                cont = False
                a = self.rect.move(cords)
                if i == 2:
                    self.left, self.right = True, False
                elif i == 3:
                    self.left, self.right = False, True
                for xx in wall_group:
                    if xx.rect.colliderect(a):
                        cont = True
                        break
                if cont:
                    continue

                self.rect = a
                not_move = False
        if not_move:
            self.left, self.right = False, False

    def get_damage(self):
        self.hp -= 1
        self.timer = 60
        if self.hp == 0:
            self.death = True
            self.death_time = round(time())

    def status(self):
        return self.death

    def live_time(self, start_time):
        return self.death_time - start_time

    def get_kills(self):
        return self.kills

    def add_kills(self, kills):
        self.kills += kills

    def change_hp(self, hp):
        self.hp = hp


class PlayerBullet(pg.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y):
        super().__init__(bullets_group, all_sprites)
        self.image = bullet

        self.rect = pg.Rect(x, y, *bullet.get_size())

        self.speed = 10
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        rnd = randint(-15, 15) / 10
        self.x_vel = math.cos(self.angle) * self.speed + rnd
        self.y_vel = math.sin(self.angle) * self.speed + rnd

    def update(self, player):
        if pg.sprite.spritecollideany(self, enemies_group):
            for enemy in enemies_group:
                if self.rect.colliderect(enemy.rect):
                    self.kill()
                    create_particles((self.rect.x, self.rect.y))
                    if enemy.get_damage():
                        player.add_kills(1)
                    return
        if pg.sprite.spritecollideany(self, wall_group):
            self.kill()
            create_particles((self.rect.x, self.rect.y))
            return
        self.rect = self.rect.move(-self.x_vel, -self.y_vel)


class CockroachEnemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemies_group, all_sprites)
        self.image = tarakan_right[0]
        self.rect = pg.Rect(x, y, *self.image.get_size())
        self.hp = 5
        self.speed = 1.9

        self.nx, self.ny = 32 * 11, 32 * 19
        self.nw, self.nh = 32 * 22, 32 * 38

        # анимация
        self.left = False
        self.right = False
        self.animCount = 0

        self.timer = 0

    def update(self, player):
        rct = player.rect
        cx, cy = self.rect.x, self.rect.y
        en_rect = pg.Rect(cx - self.nx, cy - self.ny,
                          self.nw, self.nh)
        move = False
        reverse = False
        if en_rect.colliderect(rct):
            player_x, player_y = rct.x, rct.y

            if cx != player_x:
                if cx < player_x:
                    new_rect = self.rect.move(self.speed, 0)
                    if check_walls(new_rect):
                        self.rect = new_rect
                        move = True

                else:
                    new_rect = self.rect.move(-self.speed, 0)
                    if check_walls(new_rect):
                        self.rect = new_rect
                        move = True
                        reverse = True
            if cy != player_y:
                if cy < player_y:
                    new_rect = self.rect.move(0, self.speed)
                    if check_walls(new_rect):
                        self.rect = new_rect
                        move = True

                else:
                    new_rect = self.rect.move(0, -self.speed)
                    if check_walls(new_rect):
                        self.rect = new_rect
                        move = True

        if move:
            self.image = tarakan_right[self.animCount // 30].copy()
            if reverse:
                self.image = pg.transform.flip(self.image, True, False)
        else:
            self.image = tarakan_stand[round(self.animCount / 60)]


        if self.timer:
            self.image = change_brightness(self.image.copy(), 50)
            self.timer -= 1

        self.animCount += 1
        if self.animCount == 60:
            self.animCount = 0

    def get_damage(self):
        self.hp -= 1
        if not self.timer:
            self.image = change_brightness(self.image.copy(), 50)
            self.timer = 10
        if self.hp == 0:
            self.kill()
            return True


class Camera:
    def __init__(self, size):
        self.W, self.H = size
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.W // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.H // 2)


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_id: int, pos_x: int, pos_y: int):
        super().__init__(tiles_group, all_sprites)
        if tile_id != 5:
            self.add(wall_group)
        self.image = tiles[tile_id - 1]
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    player, x, y = None, None, None
    enemies = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            tile_id = level[y][x]
            if tile_id == 0:
                continue
            elif tile_id == 12:
                enemies += 1
                Tile(5, x, y)
                CockroachEnemy(tile_width * x, tile_height * y)
            elif tile_id == 15:
                Tile(5, x, y)
                player = Player(tile_width * x, tile_height * y)
            else:
                Tile(tile_id, x, y)

    return player, enemies


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 5
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))
