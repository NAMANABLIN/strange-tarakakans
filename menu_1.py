import pygame

from config import *

forward, back, left, right, shooting = 'W', 'S', 'A', 'D', 'ЛКМ'
control_list = [forward, back, left, right, shooting]


def menu(screen):
    pygame.display.set_caption('Тараканы!')
    pg.display.set_icon(logo)

    screen.fill((60, 113, 125))
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
    screen.fill((60, 113, 125))
    screen.blit(font.render("Вперёд" + (18 - 6 - len(control_list[0])) * ' ' + control_list[0], 1, font_color),
                (W // 30 + 10, H - 550, 180, 50))
    screen.blit(font.render("Назад" + (19 - 5 - len(control_list[1])) * ' ' + control_list[1], 1, font_color),
                (W // 30 + 10, H - 515, 180, 50))
    screen.blit(font.render("Влево" + (19 - 5 - len(control_list[2])) * ' ' + control_list[2], 1, font_color),
                (W // 30 + 10, H - 485, 180, 50))
    screen.blit(font.render("Вправо" + (18 - 6 - len(control_list[3])) * ' ' + control_list[3], 1, font_color),
                (W // 30 + 10, H - 450, 180, 50))
    screen.blit(font.render("Стрельба" + (18 - 8 - len(control_list[4])) * ' ' + control_list[4], 1, font_color),
                (W // 30 + 10, H - 415, 180, 50))

    # Кнопки
    pygame.draw.rect(screen, (50, 92, 102), (W // 2 - 95, H - 100, 190, 50), 0)
    text = font.render("Назад", 1, font_color)
    screen.blit(text, (W // 2 - 95 + 50, H - 100))

    pygame.draw.rect(screen, (50, 92, 102), (W // 30, H - 360, 180, 50), 0)
    text = font.render("Сохранить", 1, font_color)
    screen.blit(text, (W // 30 + 15, H - 360, 180, 50))

    pygame.draw.rect(screen, (50, 92, 102), (W // 30, H - 300, 180, 50), 0)
    text = font.render("Сброс", 1, font_color)
    screen.blit(text, (W // 30 + 50, H - 300, 180, 50))

    screen_value = 'control'
    return screen_value


def options(s, m):
    screen = pygame.display.set_mode(size)
    screen.fill((60, 113, 125))
    pygame.display.set_caption('Настройки')
    screen_value = 'options'

    # Кнопки
    buttons_coord = [(W // 30, H - 480, 190, 50), (W // 30, H - 420, 190, 50),
                     (W // 30, H - 360, 190, 50), (W // 30, H - 300, 190, 50), (W - 530, H - 360, 190, 50)]
    button(buttons_coord, screen)

    text = font.render("Звук", 1, font_color)
    screen.blit(text, (W // 30 + 60, H - 480, 180, 50))

    text = font.render("Музыка", 1, font_color)
    screen.blit(text, (W // 30 + 40, H - 420, 180, 50))

    text = font.render("Управление", 1, font_color)
    screen.blit(text, (W // 30 + 10, H - 360, 180, 50))

    text = font.render("Назад", 1, font_color)
    screen.blit(text, (W // 30 + 55, H - 300, 180, 50))

    text = font.render("Сохранить", 1, font_color)
    screen.blit(text, (W - 530 + 20, H - 360, 180, 50))

    # Слайдеры
    pygame.draw.line(screen, (58, 65, 66), (W - 550, H - 455), (W - 300, H - 455), width=5)
    pygame.draw.line(screen, (58, 65, 66), (W - 550, H - 395), (W - 300, H - 395), width=5)
    sound = pygame.draw.rect(screen, (50, 92, 102), (s, H - 470, 10, 30))
    music = pygame.draw.rect(screen, (50, 92, 102), (m, H - 410, 10, 30))

    sounds = [(sound.x, sound.y, 10, 30), (music.x, music.y, 10, 30)]
    volume = [round((s - 250) / 245, 2), round((m - 250) / 245, 2)]

    pygame.display.flip()

    return buttons_coord, screen_value, sounds, sound, music, volume


def button(buttons_coord, screen):  # отрисовка кнопок
    for x in buttons_coord:
        pygame.draw.rect(screen, (50, 92, 102), x, 0)


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
        buttons, screen_value, sounds, sound, music, volume = options(s, m)
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
                                running = False
                            elif buttons.index(i) == 1:  # options
                                s = int(open('sound').read().strip().split()[1])
                                m = int(open('sound').read().strip().split()[3])
                                buttons, screen_value, sounds, sound, music, volume = options(s, m)
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
                            buttons, screen_value, sounds, sound, music, volume = options(s, m)
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
                            buttons, screen_value, sounds, sound, music, volume = options(s, m)
                    for i in buttons:
                        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                            if buttons.index(i) == 3:  # back
                                if main_or_esc:
                                    buttons, screen_value = menu(screen)
                                else:
                                    running = False
                            elif buttons.index(i) == 2:  # control
                                screen_value = control()
                                break
                            elif buttons.index(i) == 4:  # save
                                open('sound', 'w').write(
                                    str(volume[0]) + ' ' + str(s) + '\n' + str(volume[1]) + ' ' + str(m))
                elif screen_value == 'control':
                    if W // 2 - 95 <= x <= W // 2 - 95 + 190 and H - 100 <= y <= H - 100 + 50:  # back
                        control_list = [forward, back, left, right, shooting]
                        s = int(open('sound').read().strip().split()[1])
                        m = int(open('sound').read().strip().split()[3])
                        buttons, screen_value, sounds, sound, music, volume = options(s, m)
                    else:
                        if key == '' and W // 30 <= x <= W // 30 + 180 and H - 360 <= y <= H - 310:  # save
                            open('control', 'w', encoding='UTF-8').write('\n'.join(control_list))
                            forward, back, left, right, shooting = control_list
                        elif key == '' and W // 30 <= x <= W // 30 + 180 and H - 300 <= y <= H - 250:  # reset
                            forward, back, left, right, shooting = 'W', 'S', 'A', 'D', 'ЛКМ'
                            control_list = [forward, back, left, right, shooting]
                            open('control', 'w', encoding='UTF-8').write('\n'.join(control_list))
                            control()
                        else:
                            if event.button == 1 and 'ЛКМ' in control_list and key == '':
                                key = control_list.index('ЛКМ')
                                control_list[control_list.index('ЛКМ')] = ''
                            elif event.button == 3 and 'ПКМ' in control_list and key == '':
                                key = control_list.index('ПКМ')
                                control_list[control_list.index('ПКМ')] = ''
                            elif event.button == 1 and key != '' and 'ЛКМ' not in control_list:
                                control_list[key] = 'ЛКМ'
                                key = ''
                            elif event.button == 3 and key != '' and 'ПКМ' not in control_list:
                                control_list[key] = 'ПКМ'
                                key = ''
                            control()
                elif screen_value == 'newgame':
                    return
            if event.type == pygame.KEYDOWN:
                if event.key in range(97, 122):
                    if screen_value == 'control':
                        if chr(event.key).upper() in control_list and '' not in control_list:
                            key = control_list.index(chr(event.key).upper())
                            control_list[control_list.index(chr(event.key).upper())] = ''
                            control()
                        elif chr(event.key).upper() not in control_list and key != '':
                            control_list[key] = chr(event.key).upper()
                            control()
                            key = ''
        clock.tick(60)
        pygame.display.flip()
    if main_or_esc:
        pygame.quit()
