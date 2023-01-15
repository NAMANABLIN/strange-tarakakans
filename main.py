from classes import *
from menu_1 import main_menu, control_list, button
from defs import load_level
import sys

main_menu()

sc = pg.display.set_mode(SIZE)
pg.display.set_caption('Тараканы!')
pg.display.set_icon(logo)
clock = pg.time.Clock()

camera = Camera(SIZE)
keys_list = [keys_list[control_list[i]] for i in range(4)]
click_btn = control_list[4]


def game():
    enemies = 0
    kills = 0
    start_time = round(time())
    for i in range(1, 4):
        player, new_enemies = generate_level(load_level(f'level{i}.json'))
        player.add_kills(kills)
        enemies += new_enemies
        timer = 0
        exit_time = 3
        count_reload = 0
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
                sc.blit(font.render(f"Потрачено время: {player.live_time(start_time)}", 2, WHITE), (60, 120))

                buttons_coord = [(W // 2 - 190 // 2, H - 100, 190, 50)]
                button(buttons_coord, sc)

            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == mouse_buttons[click_btn]:
                            if not count_reload:
                                PlayerBullet(player.rect.x + 15, player.rect.y + 15,
                                             *event.pos)
                                count_reload = 10

                keys = pg.key.get_pressed()

                player.move(keys, keys_list)
                if keys[pg.K_ESCAPE]:
                    main_menu(False)

                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)

                updates(sc, player)
                if enemies == player.get_kills():
                    txt = font.render(f"Вы прошли уровень!", 1, WHITE)

                    sc.blit(txt, (W // 2 - txt.get_width() // 2, 60))

                    txt2 = font.render(f'Вы перенесётесь на следующий уровень через {exit_time} секунд',
                                       1, WHITE)

                    sc.blit(txt2, (W // 2 - txt2.get_width() // 2, 70 + txt.get_height()))

                    timer += 1
                    if timer == 60:
                        timer = 0
                        exit_time -= 1
                        if exit_time == 0:
                            running = False
                            kills = player.get_kills()
                            clear()

                player.main(sc)
                # отображение hp игрока
                x_hp_sqr = 10
                for x in range(player.hp):
                    pg.draw.rect(sc, RED, (x_hp_sqr, 10, 30, 30))
                    x_hp_sqr += 35

                if count_reload:
                    count_reload -= 1

            pg.display.update()
            clock.tick(FPS)


game()
