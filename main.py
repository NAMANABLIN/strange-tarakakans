from classes import *
from config import *
from menu_1 import main_menu

main_menu()

sc = pg.display.set_mode(size)
pg.display.set_caption('Тараканы!')
pg.display.set_icon(logo)
clock = pg.time.Clock()


camera = Camera(size)

player, level_x, level_y = generate_level(load_level('kek.txt'))
while True:
    sc.fill(BLACK)

    if player.alive():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        updates(sc)
        sc.blit(game_over_image, (0, 0))
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
                PlayerBullet(player.rect.x + 20, player.rect.y + 20, mouse_x + randrange(-10, 10), mouse_y+ randrange(-10, 10))

    keys = pg.key.get_pressed()


    check_move = False
    if keys[pg.K_LEFT] or keys[pg.K_a]:
        player.move('лево')
        check_move = True
    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        player.move('право')
        check_move = True
    if keys[pg.K_UP] or keys[pg.K_w]:
        player.move('вперёд')
        check_move = True
    if keys[pg.K_DOWN] or keys[pg.K_s]:
        player.move('назад')
        check_move = True
    if not check_move:
        player.left = False
        player.right = False
    if keys[pg.K_ESCAPE]:
        main_menu(False)


    updates(sc, player)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    player.main(sc)

    x_hp_sqr = 10
    for x in range(player.hp):
        pg.draw.rect(sc, (255, 0, 0), (x_hp_sqr, 10, 30, 30))
        x_hp_sqr += 35

    pg.display.update()
    clock.tick(FPS)
