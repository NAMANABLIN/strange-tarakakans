from classes import *
from menu_1 import main_menu, button, sleep
from defs import load_level
import sys

s = float(open('sound').read().strip().split()[0])
m = float(open('sound').read().strip().split()[2])
change_volume((s, m))
main_menu()

sc = pg.display.set_mode(SIZE)
pg.display.set_caption('Тараканы!')
pg.display.set_icon(logo)

camera = Camera(SIZE)

def game():
    # очистка всех спрайтовых групп, нужна в случае если игра запускается после проигрыша/выигрыша
    clear()

    clock = pg.time.Clock()
    enemies = 0
    kills = 0
    start_time = round(time())
    control_list = open('control', encoding='UTF-8').read().strip().split()
    keys_list = [letter2konst[control_list[i]] for i in range(4)]
    click_btn = control_list[4]
    mixer.music.play(-1)
    for i in range(1, 4):
        # на каждом уровне игрок создаётся заново, поэтому нужно закидывать новые значения в класс игрока
        player, new_enemies = generate_level(load_level(f'level{i}.json'))
        player.add_kills(kills)
        enemies += new_enemies

        timer = 0  # счётчик кадров для текста во время перехода обновляется раз в секунду
        exit_time = 3  # секунды до перехода на следующий уровень
        count_reload = 0  # счетчик кадров для выстрела, если =0 то выстрелить можно
        running = True
        while running:
            sc.fill(BLACK)
            if player.status():  # если игрок проиграл/выиграл
                buttons_coord = [(W // 2 - 190 // 2, H - 160, 190, 50), (W // 2 - 115, H - 100, 220, 50)]
                txt_coord = [(W // 2 - 190 // 2 + 45, H - 160, 190, 50), (W // 2 - 110, H - 100)]
                txts = ['Выйти', "Выйти в меню"]
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            x = event.pos[0]
                            y = event.pos[1]
                            bt, bt2 = buttons_coord
                            if bt[0] <= x <= bt[0] + bt[2] and \
                                    bt[1] <= y <= bt[1] + bt[3]:
                                sounds['click'].play()
                                sleep(0.1)
                                pg.quit()
                                sys.exit()
                            elif bt2[0] <= x <= bt2[0] + bt2[2] and \
                                    bt2[1] <= y <= bt2[1] + bt2[3]:
                                sounds['click'].play()
                                mixer.stop()
                                main_menu()
                                txts, txt_coord, player, enemies, new_enemies, clock, click_btn, keys_list, \
                                    control_list, start_time, kills, timer, exit_time, \
                                    count_reload, running = [0] * 15
                                game()

                updates(sc)
                sc.blit(game_over_image, (0, 0))
                if player.winner:
                    txt = font2.render(f"ВЫ ПОБЕДИЛИ!!!!", 2, WHITE)
                else:
                    txt = font2.render(f"ВЫ ПРОИГРАЛИ(", 2, WHITE)
                sc.blit(txt, (W / 2 - txt.get_width() / 2, 40))
                sc.blit(font.render(f"Убито тараканов: {player.get_kills()}", 2, WHITE), (60, 130))
                sc.blit(font.render(f"Потрачено время: {player.live_time(start_time)}", 2, WHITE), (60, 190))

                button(buttons_coord, txt_coord, txts, sc)

            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()

                a = pg.mouse.get_pressed(3)
                keys = pg.key.get_pressed()
                if a[mouse_buttons[click_btn]]:  # выстрел
                    if not count_reload:
                        PlayerBullet(player.rect.x + 15, player.rect.y + 15,
                                     *pg.mouse.get_pos())
                        count_reload = 25
                if keys[pg.K_ESCAPE]:  # переход в меню
                    mixer.music.pause()
                    main_menu(False)
                    control_list = open('control', encoding='UTF-8').read().strip().split()
                    keys_list = [letter2konst[control_list[i]] for i in range(4)]
                    click_btn = control_list[4]
                    mixer.music.unpause()

                player.move(keys, keys_list)

                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)

                updates(sc, player)
                player.main(sc)

                if enemies == player.get_kills():
                    if i == 3:  # если игрок прошёл 3 уровня(выиграл)
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

                if count_reload:
                    count_reload -= 1

            pg.display.update()
            clock.tick(FPS)


game()
