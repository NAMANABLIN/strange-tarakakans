import math
from random import randrange

from config import *

class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(wall_group)
        self.image = tile_images[tile_type]
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = gg
        self.x = x
        self.y = y
        self.width, self.height = self.image.get_size()
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.speed = 5

        self.timer = 0
        self.hp = 3

    def handle_weapons(self, display):
        mouse_x, mouse_y = pg.mouse.get_pos()

        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pg.transform.rotate(player_weapon, angle)

        display.blit(player_weapon_copy, (
            self.rect.x + 15 - int(player_weapon.get_width() / 2),
            self.rect.y + 25 - int(player_weapon_copy.get_height() / 2)))

    def main(self, display):
        self.handle_weapons(display)

    def move(self, axis):  # True - лево, право; False - прямо, вперёд
        if axis == 'лево':
            for x in wall_group:
                if x.rect.colliderect(self.rect.move(-self.speed, 0)):
                    return
            self.rect = self.rect.move(-self.speed, 0)
        if axis == 'право':
            for x in wall_group:
                if x.rect.colliderect(self.rect.move(self.speed, 0)):
                    return
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

        if self.timer == 0:
            if pg.sprite.spritecollideany(self, enemys_group):
                self.get_damage()
        else:
            self.timer -= 1

    def get_damage(self):
        self.hp -= 1
        self.timer = 25
        if self.hp == 0:
            exit()


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
                self.rect = self.rect.move(1,0)
                self.image = tarakan
            elif cx > player_x:
                for x in wall_group:
                    if x.rect.colliderect(self.rect.move(-self.speed, 0)):
                        return
                self.image = tarakan_reverse
                self.rect = self.rect.move(-1,0)
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
