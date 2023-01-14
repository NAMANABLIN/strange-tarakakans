import pygame

from config import *

forward, back, left, right, shooting = open('control', encoding='UTF-8').read().strip().split()
control_list = [forward, back, left, right, shooting]
button_color = (28, 28, 28)


def menu(screen):
    pygame.display.set_caption('Тараканы!')
    pg.display.set_icon(logo)

    screen.blit(fon, (0, 0))
    pygame.display.flip()
    buttons_coord = [(W // 2 - 190 // 2, H - 100, 190, 50), (W // 2 - 190 // 2, H - 160, 190, 50),
                     (W // 2 - 190 // 2, H - 220, 190, 50), (W // 2 - 190 // 2, H - 280, 190, 50)]
    button(buttons_coord, screen)

    text = font.render("Продолжить", 1, font_color)
    screen.blit(text, (W // 2 - 190 // 2, H - 280, 180, 50))

    text = font.render("Новая игра", 1, font_color)
    screen.blit(text, (W // 2 - 190 // 2 + 17, H - 220, 180, 50))

    text = font.render("Настройки", 1, font_color)
    screen.blit(text, (W // 2 - 190 // 2 + 20, H - 160, 180, 50))

    text = font.render("Выйти", 1, font_color)
    screen.blit(text, (W // 2 - 190 // 2 + 45, buttons_coord[0][1]))

    pygame.display.flip()
    screen_value = 'menu'
    return buttons_coord, screen_value


def newgame():
    screen_value = 'newgame'
    return screen_value


def continuegame():
    screen_value = 'continue'
    return screen_value


def control():
    global control_list
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Управление')
    screen.blit(fon, (0, 0))
    screen.blit(font.render("Вперёд" + (18 - 6 - len(control_list[0])) * ' ' + control_list[0], 1, font_color),
                (W // 30 + 10, H - 400, 180, 50))
    screen.blit(font.render("Назад" + (19 - 5 - len(control_list[1])) * ' ' + control_list[1], 1, font_color),
                (W // 30 + 10, H - 365, 180, 50))
    screen.blit(font.render("Влево" + (19 - 5 - len(control_list[2])) * ' ' + control_list[2], 1, font_color),
                (W // 30 + 10, H - 335, 180, 50))
    screen.blit(font.render("Вправо" + (18 - 6 - len(control_list[3])) * ' ' + control_list[3], 1, font_color),
                (W // 30 + 10, H - 305, 180, 50))
    screen.blit(font.render("Стрельба" + (18 - 8 - len(control_list[4])) * ' ' + control_list[4], 1, font_color),
                (W // 30 + 10, H - 275, 180, 50))

    # Кнопки
    pygame.draw.rect(screen, button_color, (W // 2 - 95, H - 100, 190, 50), 0)
    text = font.render("Назад", 1, font_color)
    screen.blit(text, (W // 2 - 95 + 50, H - 100))

    pygame.draw.rect(screen, button_color, (W // 30, H - 220, 180, 50), 0)
    text = font.render("Сохранить", 1, font_color)
    screen.blit(text, (W // 30 + 15, H - 220, 180, 50))

    pygame.draw.rect(screen, button_color, (W // 30, H - 160, 180, 50), 0)
    text = font.render("Сброс", 1, font_color)
    screen.blit(text, (W // 30 + 50, H - 160, 180, 50))

    screen_value = 'control'
    return screen_value


def options(s, m, main_or_esc):
    screen = pygame.display.set_mode(size)
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('Настройки')
    screen_value = 'options'

    # Кнопки
    buttons_coord = [(W // 30, H - 250, 190, 50), (W // 30, H - 190, 190, 50), (W - 530, H - 250, 190, 50)]
    button(buttons_coord, screen)

    text = font.render("Звук", 1, font_color)
    screen.blit(text, (W // 30 + 60, H - 380, 180, 50))

    text = font.render("Музыка", 1, font_color)
    screen.blit(text, (W // 30 + 40, H - 320, 180, 50))

    text = font.render("Управление", 1, font_color)
    screen.blit(text, (W // 30 + 10, H - 250, 180, 50))

    text = font.render("Назад", 1, font_color)
    screen.blit(text, (W // 30 + 55, H - 190, 180, 50))

    text = font.render("Сохранить", 1, font_color)
    screen.blit(text, (W - 530 + 20, H - 250, 180, 50))

    # Слайдеры
    pygame.draw.line(screen, (52, 52, 52), (W - 550, H - 355), (W - 300, H - 355), width=5)
    pygame.draw.line(screen, (52, 52, 52), (W - 550, H - 295), (W - 300, H - 295), width=5)
    sound = pygame.draw.rect(screen, (45, 44, 41), (s, H - 370, 10, 30))
    music = pygame.draw.rect(screen, (45, 44, 41), (m, H - 310, 10, 30))

    sounds = [(sound.x, sound.y, 10, 30), (music.x, music.y, 10, 30)]
    volume = [round((s - 250) / 245, 2), round((m - 250) / 245, 2)]

    if not main_or_esc:
        pygame.draw.rect(screen, button_color, (W // 2 - 115, H - 100, 220, 50), 0)
        text = font.render("Выйти в меню", 1, font_color)
        screen.blit(text, (W // 2 - 110, H - 100))

    pygame.display.flip()

    return buttons_coord, screen_value, sounds, sound, music, volume


def button(buttons_coord, screen):  # отрисовка кнопок
    for x in buttons_coord:
        pygame.draw.rect(screen, button_color, x, 0)


def exit_game():
    screen = pygame.display.set_mode((800, 600))
    screen.blit(fon, (0, 0))
    text = font.render("Вы точно хотите выйти?", 1, font_color)
    screen.blit(text, (W - 570, H - 300))
    pygame.draw.rect(screen, (45, 44, 41), (W - 550, H - 240, 150, 50))
    pygame.draw.rect(screen, (45, 44, 41), (W - 380, H - 240, 150, 50))
    screen.blit(font.render("Да", 1, font_color), (W - 550 + 55, H - 240, 180, 50))
    screen.blit(font.render("Нет", 1, font_color), (W - 380 + 50, H - 240, 180, 50))
    screen_value = 'exit'
    return screen_value


def main_menu(main_or_esc=True):
    global forward, back, left, right, shooting, control_list
    key = ''  # индекс изменяемой кнопки управления в списке control_list
    pygame.init()
    screen = pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()
    s = int(open('sound').read().strip().split()[1])  # координата x прямоугольника sound
    m = int(open('sound').read().strip().split()[3])  # координата x прямоугольника music
    if main_or_esc:
        buttons, screen_value = menu(screen)
    else:
        buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                                screen_value = newgame()
                            elif buttons.index(i) == 3:  # continue
                                pass
                                # continuegame()
                if screen_value == 'options':
                    if sounds[0][0] <= x <= sounds[0][0] + sounds[0][2] and sounds[0][1] <= y <= sounds[0][1] + \
                            sounds[0][3]:  # sound
                        while pygame.mouse.get_pressed()[0]:
                            if W - 550 <= pygame.mouse.get_pos()[0]:
                                if pygame.mouse.get_pos()[0] <= W - 305:
                                    s = pygame.mouse.get_pos()[0]
                                else:
                                    s = W - 305
                            else:
                                s = W - 550
                            buttons, screen_value, sounds, sound, music, volume = options(s, m, main_or_esc)
                    if sounds[1][0] <= x <= sounds[1][0] + sounds[1][2] and sounds[1][1] <= y <= sounds[1][1] + \
                            sounds[1][3]:  # music
                        while pygame.mouse.get_pressed()[0]:
                            if W - 550 <= pygame.mouse.get_pos()[0]:
                                if pygame.mouse.get_pos()[0] <= W - 305:
                                    m = pygame.mouse.get_pos()[0]
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
                elif screen_value == 'exit':
                    if W - 550 <= x <= W - 400 and H - 240 <= y <= H - 190:
                        running = False
                    elif W - 380 <= x <= W - 230 and H - 240 <= y <= H - 190:
                        screen_value = 'menu'
                        main_menu()
            if event.type == pygame.KEYDOWN:
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
        pygame.display.flip()
    if main_or_esc:
        pygame.quit()
