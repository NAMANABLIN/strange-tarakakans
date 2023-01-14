import math
from random import randrange, randint
from config import *


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = gg_stand[0]
        self.rect = pg.Rect(x, y, *self.image.get_size())
        self.speed = 4.5
        self.button2cords = [(0, -self.speed), (0, self.speed),
                             (-self.speed, 0), (self.speed, 0)]

        self.player_weapon_copy = player_weapon

        # таймер нужен чтобы после получения урона игрок не сразу же получи ещё,
        # пока таймер не равен 0 - игрок не уязвим
        self.timer = 0

        self.hp = 3
        self.death = False

        self.kills = 0

        # анимация
        self.left = False
        self.right = False
        self.animCount = 0

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
            if pg.sprite.spritecollideany(self, enemys_group):
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

    def move(self, axis):
        not_move = True
        for i, x in enumerate(axis):
            cords = self.button2cords[i]
            if x:
                cont = False
                a = self.rect.move(cords)
                for xx in wall_group:
                    if xx.rect.colliderect(a):
                        cont = True
                        break
                if cont:
                    continue
                elif i == 2:
                    self.left, self.right = True, False

                elif i == 3:
                    self.left, self.right = False, True

                self.rect = a
                self.rect.move(cords)
                not_move = False
        if not_move:
            self.left, self.right = False, False

    def get_damage(self):
        self.hp -= 1
        self.timer = 60
        if self.hp == 0:
            self.death = True

    def status(self):
        return self.death

    def get_kills(self):
        return self.kills

    def add_kills(self, n):
        self.kills += n


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
        if pg.sprite.spritecollideany(self, enemys_group):
            for enemy in enemys_group:
                if self.rect.colliderect(enemy.rect):
                    self.kill()
                    if enemy.get_damage():
                        player.add_kills(1)
        self.rect = self.rect.move(-self.x_vel, -self.y_vel)
        if pg.sprite.spritecollideany(self, wall_group):
            self.kill()

class TarakanEnemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemys_group, all_sprites)
        self.image = tarakan_right[0]
        self.rect = pg.Rect(x, y, *self.image.get_size())
        self.hp = 3
        self.reset_offset = 0
        self.speed = 1
        self.offset_x = randrange(-150, 150)
        self.offset_y = randrange(-150, 150)

        # анимация
        self.left = False
        self.right = False
        self.animCount = 0

        self.timer = 0

    def update(self, player):
        player_x, player_y = player.rect.x, player.rect.y
        cx, cy = self.rect.x, self.rect.y
        if self.timer:
            self.image = change_brightness(tarakan_right[self.animCount // 30].copy(), 50)
            self.timer -= 1
        else:
            self.image = tarakan_right[self.animCount // 30].copy()

        if cx != player_x:
            if cx < player_x:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(self.speed, 0)):
                        return
                self.rect = self.rect.move(self.speed, 0)
            elif cx > player_x:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(-self.speed, 0)):
                        return
                self.rect = self.rect.move(-self.speed, 0)
                self.image = pg.transform.flip(self.image, True, False)

        if cy != player_y:
            if cy < player_y:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(0, self.speed)):
                        return
                self.rect = self.rect.move(0, self.speed)
            elif cy > player_y:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(0, -self.speed)):
                        return
                self.rect = self.rect.move(0, -self.speed)
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
    enemys = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            tile_id = level[y][x]
            if tile_id == 0:
                continue
            elif tile_id == 12:
                enemys += 1
                Tile(5, x, y)
                TarakanEnemy(tile_width * x, tile_height * y)
            elif tile_id == 15:
                Tile(5, x, y)
                player = Player(tile_width * x, tile_height * y)
            else:
                Tile(tile_id, x, y)

    return player, enemys
