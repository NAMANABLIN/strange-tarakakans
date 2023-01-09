import math
from random import randrange

from config import *


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.x = 400
        self.y = 300
        self.width, self.height = gg.get_size()
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.speed = 5

        self.player_weapon_copy = player_weapon

        self.timer = 0
        self.hp = 3

        self.death = False

        self.left = False
        self.right = False
        self.animCount = 0

    def handle_weapons(self, display):
        mouse_x, mouse_y = pg.mouse.get_pos()

        rel_x, rel_y = mouse_x - self.rect.x+25 - int(
            player_weapon.get_width() / 2), mouse_y - self.rect.y+ 25 - int(self.player_weapon_copy.get_height() / 2)
        angle = round((180 / math.pi) * -math.atan2(rel_y, rel_x))
        # if int(angle) not in correct_radius:
        #     self.player_weapon_copy = pg.transform.rotate(player_weapon_reverse, angle)
        # else:
        if -90 <= angle <= 90:
            self.player_weapon_copy = pg.transform.rotate(player_weapon, angle)
        else:
            self.player_weapon_copy = pg.transform.rotate(player_weapon_reverse, angle)


        display.blit(self.player_weapon_copy, (
            self.rect.x +25 - int(player_weapon.get_width() / 2),
            self.rect.y+ 25 - int(self.player_weapon_copy.get_height() / 2)))

    def main(self, display):
        self.handle_weapons(display)
        if self.timer == 0:
            if pg.sprite.spritecollideany(self, enemys_group):
                self.get_damage()
        else:
            self.timer -= 1

    def draw(self, display):
        if self.left:
            display.blit(gg_left[self.animCount // 30], (self.rect.x, self.rect.y))
        elif self.right:
            display.blit(gg_right[self.animCount // 30], (self.rect.x, self.rect.y))
        else:
            display.blit(gg_stand[round(self.animCount / 60)], (self.rect.x, self.rect.y))
        self.animCount += 1

        if self.animCount == 60:
            self.animCount = 0

    def move(self, axis):  # True - лево, право; False - прямо, вперёд
        if axis == 'лево':
            for x in wall_group:
                if x.rect.colliderect(self.rect.move(-self.speed, 0)):
                    return
            self.left = True
            self.right = False
            self.rect = self.rect.move(-self.speed, 0)
        if axis == 'право':
            for x in wall_group:
                if x.rect.colliderect(self.rect.move(self.speed, 0)):
                    return
            self.left = False
            self.right = True
            self.rect = self.rect.move(self.speed, 0)
        if axis == 'вперёд':
            for x in wall_group:
                if x.rect.colliderect(self.rect.move(0, -self.speed)):
                    return
            self.rect = self.rect.move(0, -self.speed)
        if axis == 'назад':
            for x in wall_group:
                if x.rect.colliderect(self.rect.move(0, self.speed)):
                    return
            self.rect = self.rect.move(0, self.speed)

    def get_damage(self):
        self.hp -= 1
        self.timer = 60
        if self.hp == 0:
            self.death = True

    def alive(self):
        return self.death


class PlayerBullet(pg.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y):
        super().__init__(bullets_group, all_sprites)
        self.image = bullet
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        self.rect = pg.Rect(x, y, bullet.get_width(), bullet.get_height())

        self.speed = 10
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def update(self):
        if pg.sprite.spritecollideany(self, enemys_group):
            for enemy in enemys_group:
                if self.rect.colliderect(enemy.rect):
                    self.kill()
                    enemy.get_damage()
                    return
        if pg.sprite.spritecollideany(self, wall_group):
            self.kill()
            return

        self.rect = self.rect.move(-int(self.x_vel), -int(self.y_vel))


class TarakanEnemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemys_group, all_sprites)
        self.image = tarakan
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, tarakan.get_width(), tarakan.get_height())
        self.hp = 3
        self.reset_offset = 0
        self.speed = 1
        self.offset_x = randrange(-150, 150)
        self.offset_y = randrange(-150, 150)

    def update(self, player):
        player_x, player_y = player.rect.x, player.rect.y
        cx, cy = self.rect.x, self.rect.y
        if cx != player_x:
            if cx < player_x:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(self.speed, 0)):
                        return
                self.rect = self.rect.move(1, 0)
                self.image = tarakan
            elif cx > player_x:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(-self.speed, 0)):
                        return
                self.image = tarakan_reverse
                self.rect = self.rect.move(-1, 0)
        if cy != player_y:
            if cy < player_y:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(0, self.speed)):
                        return
                self.rect = self.rect.move(0, 1)
            elif cy > player_y:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(0, -self.speed)):
                        return
                self.rect = self.rect.move(0, -1)

    def get_damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()

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
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                player = Player(tile_width * x, tile_height * y)
            elif level[y][x] == 'e':
                Tile('empty', x, y)
                TarakanEnemy(tile_width * x, tile_height * y)
    return player, x, y
