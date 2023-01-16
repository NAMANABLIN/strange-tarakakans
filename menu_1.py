from config import pg, logo, fon, \
    font, font_color, button_color, SIZE, W, H

forward, back, left, right, shooting = open('control', encoding='UTF-8').read().strip().split()
control_list = [forward, back, left, right, shooting]


def menu(screen):
    pg.display.set_caption('Тараканы!')
    pg.display.set_icon(logo)
    screen.blit(fon, (0, 0))
    pg.display.flip()

    buttons_coord = [(W // 2 - 190 // 2, H - 100, 190, 50), (W // 2 - 190 // 2, H - 160, 190, 50),
                     (W // 2 - 190 // 2, H - 220, 190, 50)]
    txt_coord = [(W // 2 - 190 // 2 + 45, H - 100, 190, 50), (W // 2 - 190 // 2 + 20, H - 160, 180, 50),
                 (W // 2 - 190 // 2 + 50, H - 220, 180, 50)]
    txts = ["Выйти", "Настройки", "Играть"]

    button(buttons_coord, txt_coord, txts, screen)

    pg.display.flip()
    screen_value = 'menu'
    return buttons_coord, screen_value


def new_game():
    screen_value = 'newgame'
    return screen_value


def control():
    global control_list
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption('Управление')
    screen.blit(fon, (0, 0))

    txt_coord = [(W // 30 + 10, H - 400, 180, 50), (W // 30 + 10, H - 365, 180, 50),
                 (W // 30 + 10, H - 335, 180, 50), (W // 30 + 10, H - 305, 180, 50),
                 (W // 30 + 10, H - 275, 180, 50)]
    txts = ["Вперёд", "Назад", "Влево", "Вправо", "Стрельба"]
    lol = [12, 14, 14, 12, 10]
    for i in range(5):
        screen.blit(font.render(txts[i] + (lol[i] - len(control_list[i])) * ' ' + control_list[i],
                                1, font_color), txt_coord[i])

    buttons_coord = [(W // 2 - 95, H - 100, 190, 50), (W // 30, H - 220, 180, 50),
                     (W // 30, H - 160, 180, 50)]
    txt_coord = [(W // 2 - 95 + 50, H - 100), (W // 30 + 15, H - 220, 180, 50),
                 (W // 30 + 50, H - 160, 180, 50)]
    txts = ["Назад", "Сохранить", "Сброс"]

    button(buttons_coord, txt_coord, txts, screen)

    screen_value = 'control'
    return screen_value


def options(s, m, main_or_esc):
    screen = pg.display.set_mode(SIZE)
    screen.blit(fon, (0, 0))
    pg.display.set_caption('Настройки')
    screen_value = 'options'

    # Кнопки
    buttons_coord = [(W // 30, H - 250, 190, 50), (W // 30, H - 190, 190, 50),
                     (W - 530, H - 250, 190, 50)]
    txt_coord = [(W // 30 + 10, H - 250, 180, 50), (W // 30 + 55, H - 190, 180, 50),
                 (W - 530 + 20, H - 250, 180, 50)]
    txts = ["Управление", "Назад", "Сохранить"]

    button(buttons_coord, txt_coord, txts, screen)

    txt_coord = [(W // 30 + 60, H - 380, 180, 50), (W // 30 + 40, H - 320, 180, 50)]
    txts = ["Звук", "Музыка"]
    for i in range(2):
        text = font.render(txts[i], 1, font_color)
        screen.blit(text, txt_coord[i])

    # Слайдеры
    pg.draw.line(screen, (52, 52, 52), (W - 550, H - 355), (W - 300, H - 355), width=5)
    pg.draw.line(screen, (52, 52, 52), (W - 550, H - 295), (W - 300, H - 295), width=5)
    sound = pg.draw.rect(screen, (45, 44, 41), (s, H - 370, 10, 30))
    music = pg.draw.rect(screen, (45, 44, 41), (m, H - 310, 10, 30))

    sounds = [(sound.x, sound.y, 10, 30), (music.x, music.y, 10, 30)]
    volume = [round((s - 250) / 245, 2), round((m - 250) / 245, 2)]

    if not main_or_esc:
        button([(W // 2 - 115, H - 100, 220, 50)],
               [(W // 2 - 110, H - 100)], ["Выйти в меню"], screen)

    pg.display.flip()

    return buttons_coord, screen_value, sounds, sound, music, volume


def button(buttons_coord, txt_coord, txts, screen):  # отрисовка кнопок
    for i in range(len(buttons_coord)):
        pg.draw.rect(screen, button_color, buttons_coord[i], 0)
        text = font.render(txts[i], 1, font_color)
        screen.blit(text, txt_coord[i])


def exit_game():
    screen = pg.display.set_mode((800, 600))
    screen.blit(fon, (0, 0))
    text = font.render("Вы точно хотите выйти?", 1, font_color)
    screen.blit(text, (W - 570, H - 300))
    pg.draw.rect(screen, (45, 44, 41), (W - 550, H - 240, 150, 50))
    pg.draw.rect(screen, (45, 44, 41), (W - 380, H - 240, 150, 50))
    screen.blit(font.render("Да", 1, font_color), (W - 550 + 55, H - 240, 180, 50))
    screen.blit(font.render("Нет", 1, font_color), (W - 380 + 50, H - 240, 180, 50))
    screen_value = 'exit'
    return screen_value


def main_menu(main_or_esc=True):
    global forward, back, left, right, shooting, control_list
    key = ''  # индекс изменяемой кнопки управления в списке control_list
    pg.init()
    screen = pg.display.set_mode(SIZE)

    running = True
    clock = pg.time.Clock()
    s = int(open('sound').read().strip().split()[1])  # координата x прямоугольника sound
    m = int(open('sound').read().strip().split()[3])  # координата x прямоугольника music
    if main_or_esc:
        buttons, screen_value = menu(screen)
    else:
        buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if screen_value == 'menu':
                    for i in buttons:
                        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                            if buttons.index(i) == 0:  # exit
                                screen_value = exit_game()
                            elif buttons.index(i) == 1:  # options
                                s = int(open('sound').read().strip().split()[1])
                                m = int(open('sound').read().strip().split()[3])
                                buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
                            elif buttons.index(i) == 2:  # new game
                                screen_value = new_game()

                if screen_value == 'options':
                    if sounds[0][0] <= x <= sounds[0][0] + sounds[0][2] and sounds[0][1] <= y <= sounds[0][1] + \
                            sounds[0][3]:  # sound
                        while pg.mouse.get_pressed()[0]:
                            if W - 550 <= pg.mouse.get_pos()[0]:
                                if pg.mouse.get_pos()[0] <= W - 305:
                                    s = pg.mouse.get_pos()[0]
                                else:
                                    s = W - 305
                            else:
                                s = W - 550
                            buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
                    if sounds[1][0] <= x <= sounds[1][0] + sounds[1][2] and sounds[1][1] <= y <= sounds[1][1] + \
                            sounds[1][3]:  # music
                        while pg.mouse.get_pressed()[0]:
                            if W - 550 <= pg.mouse.get_pos()[0]:
                                if pg.mouse.get_pos()[0] <= W - 305:
                                    m = pg.mouse.get_pos()[0]
                                else:
                                    m = W - 305
                            else:
                                m = W - 550
                            buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
                    for i in buttons:
                        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                            if buttons.index(i) == 1:  # back
                                if main_or_esc:
                                    buttons, screen_value = menu(screen)
                                else:
                                    running = False
                            elif buttons.index(i) == 0:  # control
                                screen_value = control()
                                print(1)
                                break
                            elif buttons.index(i) == 2:  # save
                                open('sound', 'w').write(
                                    str(volume[0]) + ' ' + str(s) + '\n' + str(volume[1]) + ' ' + str(m))
                    if W // 2 - 115 <= x <= W // 2 + 105 and H - 100 <= y <= H - 50:
                        main_menu()
                        running = False

                elif screen_value == 'control':
                    if W // 2 - 95 <= x <= W // 2 - 95 + 190 and H - 100 <= y <= H - 100 + 50:  # back
                        control_list = [forward, back, left, right, shooting]
                        s = int(open('sound').read().strip().split()[1])
                        m = int(open('sound').read().strip().split()[3])
                        buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
                    else:
                        if key == '' and W // 30 <= x <= W // 30 + 180 and H - 220 <= y <= H - 170:  # save
                            open('control', 'w', encoding='UTF-8').write('\n'.join(control_list))
                            forward, back, left, right, shooting = control_list
                        elif key == '' and W // 30 <= x <= W // 30 + 180 and H - 160 <= y <= H - 110:  # reset
                            forward, back, left, right, shooting = 'W', 'S', 'A', 'D', 'ЛКМ'
                            control_list = [forward, back, left, right, shooting]
                            open('control', 'w', encoding='UTF-8').write('\n'.join(control_list))
                            control()
                        else:
                            if event.button == 1 and 'ЛКМ' in control_list and key == '':
                                key = 4
                                control_list[4] = ''
                            elif event.button == 3 and 'ПКМ' in control_list and key == '':
                                key = 4
                                control_list[4] = ''
                            elif event.button == 1 and key == 4 and 'ЛКМ' not in control_list:
                                control_list[key] = 'ЛКМ'
                                key = ''
                            elif event.button == 3 and key == 4 and 'ПКМ' not in control_list:
                                control_list[key] = 'ПКМ'
                                key = ''
                            control()

                elif screen_value == 'newgame':
                    return

                elif screen_value == 'continue':
                    return

                elif screen_value == 'exit':
                    if W - 550 <= x <= W - 400 and H - 240 <= y <= H - 190:
                        exit()
                    elif W - 380 <= x <= W - 230 and H - 240 <= y <= H - 190:
                        screen_value = 'menu'
                        main_menu()

            if event.type == pg.KEYDOWN:
                if event.key in range(97, 123):
                    if screen_value == 'control':
                        if chr(event.key).upper() in control_list and '' not in control_list:
                            key = control_list.index(chr(event.key).upper())
                            control_list[control_list.index(chr(event.key).upper())] = ''
                            control()
                        elif chr(event.key).upper() not in control_list and key != '' and key != 4:
                            control_list[key] = chr(event.key).upper()
                            control()
                            key = ''
        clock.tick(60)
        pg.display.flip()
    if main_or_esc:
        pg.quit()
