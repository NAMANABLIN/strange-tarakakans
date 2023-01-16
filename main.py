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


def game():
    enemies = 0
    kills = 0
    start_time = round(time())
    keys_list = [letter2konst[control_list[i]] for i in range(4)]
    click_btn = control_list[4]
    mixer.music.play(-1)
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
                buttons_coord = [(W // 2 - 190 // 2, H - 100, 190, 50)]
                txt_coord = [(W // 2 - 190 // 2 + 45, H - 100, 190, 50)]
                txts = ['Выйти']
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            x = event.pos[0]
                            y = event.pos[1]
                            bt = buttons_coord[0]
                            if bt[0] <= x <= bt[0] + bt[2] and \
                                    bt[1] <= y <= bt[1] + bt[3]:
                                exit()

                updates(sc)
                sc.blit(game_over_image, (0, 0))
                if player.winner:
                    sc.blit(font.render(f"ВЫ ПОБЕДИЛИ!!!!", 2, WHITE), (30, 60))
                else:
                    sc.blit(font.render(f"ВЫ ПРОИГРАЛИ(", 2, WHITE), (30, 60))
                sc.blit(font.render(f"Убито тараканов: {player.get_kills()}", 2, WHITE), (100, 60))
                sc.blit(font.render(f"Потрачено время: {player.live_time(start_time)}", 2, WHITE), (100, 120))

                button(buttons_coord, txt_coord, txts, sc)

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
                    mixer.music.pause()
                    main_menu(False)
                    keys_list = [letter2konst[control_list[i]] for i in range(4)]
                    click_btn = control_list[4]
                    mixer.music.unpause()

                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)

                updates(sc, player)

                if enemies == player.get_kills():
                    if i == 3:
                        player.get_damage(False)
                    else:
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

                if count_reload:
                    count_reload -= 1

            pg.display.update()
            clock.tick(FPS)


game()
