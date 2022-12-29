from classes import *
from config import *

pg.init()
main_menu()

size = W, H = 800, 600
sc = pg.display.set_mode((800, 600))
pg.display.set_caption('Тараканы!')

clock = pg.time.Clock()
FPS = 60

speed = 15

camera = Camera(size)

player, level_x, level_y = generate_level(load_level('kek.txt'))

while True:
    sc.fill(BLACK)

    if player.alive():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        tiles_group.draw(sc)
        wall_group.draw(sc)
        bullets_group.draw(sc)
        enemys_group.draw(sc)
        lol = pg.Surface(size)
        lol.fill((0, 0, 0))
        lol.set_alpha(100)
        sc.blit(lol, (0, 0))
        pg.display.update()
        clock.tick(FPS)

        continue
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                PlayerBullet(player.rect.x + 40, player.rect.y - 30, mouse_x, mouse_y)

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] or keys[pg.K_a]:
        player.move('лево')
    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        player.move('право')
    if keys[pg.K_UP] or keys[pg.K_w]:
        player.move('вперёд')
    if keys[pg.K_DOWN] or keys[pg.K_s]:
        player.move('назад')

    bullets_group.update()
    enemys_group.update(player)
    tiles_group.draw(sc)
    wall_group.draw(sc)
    bullets_group.draw(sc)
    enemys_group.draw(sc)
    player_group.draw(sc)

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    player.main(sc)

    lol = 10
    for x in range(player.hp):
        pg.draw.rect(sc, (255, 0, 0), (lol, 10, 30, 30))
        lol += 35

    pg.display.update()
    clock.tick(FPS)
