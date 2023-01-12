from classes import *
from menu_1 import main_menu
from random import randint
main_menu()

sc = pg.display.set_mode(size)
pg.display.set_caption('Тараканы!')
pg.display.set_icon(logo)
clock = pg.time.Clock()

camera = Camera(size)
player, level_x, level_y = generate_level(load_level('level1.json'))
while True:
    sc.fill(BLACK)
    if player.status():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        updates(sc)
        sc.blit(game_over_image, (0, 0))
        sc.blit(font.render(f"Убито тараканов: {player.get_kills()}", 1, WHITE), (60,60))

    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    PlayerBullet(player.rect.x + 25, player.rect.y + 25,
                                 mouse_x, mouse_y)

        keys = pg.key.get_pressed()


        check_move = True
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            player.move('лево')
            check_move = False
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            player.move('право')
            check_move = False
        if keys[pg.K_UP] or keys[pg.K_w]:
            player.move('вперёд')
            check_move = False
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            player.move('назад')
            check_move = False
        if check_move:
            player.left = False
            player.right = False
        if keys[pg.K_ESCAPE]:
            main_menu(False)

        updates(sc, player)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        player.main(sc)
        # отображение hp игрока
        x_hp_sqr = 10
        for x in range(player.hp):
            pg.draw.rect(sc, (255, 0, 0), (x_hp_sqr, 10, 30, 30))
            x_hp_sqr += 35

    pg.display.update()
    clock.tick(FPS)
