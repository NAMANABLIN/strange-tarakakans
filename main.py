from classes import *
from menu_1 import main_menu
from random import randint

main_menu()

sc = pg.display.set_mode(size)
pg.display.set_caption('Тараканы!')
pg.display.set_icon(logo)
clock = pg.time.Clock()

camera = Camera(size)


def game():
    enemys = 0
    kills = 0
    for i in range(1, 4):
        player, enemys1 = generate_level(load_level(f'level{i}.json'))
        player.add_kills(kills)
        enemys += enemys1
        timer = 0
        exit_time = 3
        running = True
        while running:
            sc.fill(BLACK)
            if player.status():
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pass

                updates(sc)
                sc.blit(game_over_image, (0, 0))
                sc.blit(font.render(f"Убито тараканов: {player.get_kills()}", 2, WHITE), (60, 60))

            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            PlayerBullet(player.rect.x + 25, player.rect.y + 25,
                                         *event.pos)

                keys = pg.key.get_pressed()

                player.move([keys[pg.K_w], keys[pg.K_s],
                             keys[pg.K_a], keys[pg.K_d]])
                if keys[pg.K_ESCAPE]:
                    main_menu(False)

                updates(sc, player)
                if enemys == player.get_kills():
                    txt = font.render(f"Вы прошли уровень!", 1, WHITE)
                    sc.blit(txt, (W // 2 - txt.get_width() // 2, 60))
                    txt2 = font.render(f'Вы перенесётесь на следующий уровень через {exit_time} секунд', 1, WHITE)
                    sc.blit(txt2, (W // 2 - txt2.get_width() // 2, 70 + txt.get_height()))

                    timer += 1
                    if timer == 60:
                        timer = 0
                        exit_time -= 1
                        if exit_time == 0:
                            running = False
                            kills = player.get_kills()
                            clear()
                            break

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


game()
