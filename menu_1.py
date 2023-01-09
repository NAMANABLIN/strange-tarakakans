import pygame

from config import *

forward = 'W'
back = 'S'
left = 'A'
right = 'D'
shooting = 'ЛКМ'

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


def control(forward, back, left, right, shooting):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('control')
    screen.fill((60, 113, 125))
    screen.blit(font.render("Вперёд" + (18 - 6 - len(forward)) * ' ' + forward, 1, font_color),
                (W // 30 + 10, H - 550, 180, 50))
    screen.blit(font.render("Назад" + (19 - 5 - len(back)) * ' ' + back, 1, font_color),
                (W // 30 + 10, H - 515, 180, 50))
    screen.blit(font.render("Влево" + (19 - 5 - len(left)) * ' ' + left, 1, font_color),
                (W // 30 + 10, H - 485, 180, 50))
    screen.blit(font.render("Вправо" + (18 - 6 - len(right)) * ' ' + right, 1, font_color),
                (W // 30 + 10, H - 450, 180, 50))
    screen.blit(font.render("Стрельба" + (18 - 8 - len(shooting)) * ' ' + shooting, 1, font_color),
                (W // 30 + 10, H - 415, 180, 50))
    buttons_coord = [(W // 2 - 190 // 2, H - 100, 190, 50)]
    pygame.draw.rect(screen, (50, 92, 102), buttons_coord[0], 0)
    text = font.render("Назад", 1, font_color)
    screen.blit(text, (W // 2 - 190 // 2 + 50, H - 100))
    screen_value = 'control'
    return buttons_coord, screen_value


def options(s, m):
    screen = pygame.display.set_mode(size)
    screen.fill((60, 113, 125))
    screen_value = 'options'

    buttons_coord = [(W // 30, H - 480, 190, 50), (W // 30, H - 420, 190, 50),
                     (W // 30, H - 360, 190, 50), (W // 30, H - 300, 190, 50)]

    button(buttons_coord, screen)

    text = font.render("Звук", 1, font_color)
    screen.blit(text, (W // 30 + 60, H - 480, 180, 50))

    text = font.render("Музыка", 1, font_color)
    screen.blit(text, (W // 30 + 40, H - 420, 180, 50))

    text = font.render("Управление", 1, font_color)
    screen.blit(text, (W // 30 + 10, H - 360, 180, 50))

    text = font.render("Назад", 1, font_color)
    screen.blit(text, (W // 30 + 55, H - 300))

    pygame.draw.line(screen, (58, 65, 66), (W - 550, H - 455), (W - 300, H - 455), width=5)
    pygame.draw.line(screen, (58, 65, 66), (W - 550, H - 395), (W - 300, H - 395), width=5)

    sound = pygame.draw.rect(screen, (50, 92, 102), (s, H - 470, 10, 30))
    music = pygame.draw.rect(screen, (50, 92, 102), (m, H - 410, 10, 30))

    sounds = [(sound.x, sound.y, 10, 30), (music.x, music.y, 10, 30)]

    pygame.display.flip()

    return buttons_coord, screen_value, sounds, sound, music


def button(buttons_coord, screen):
    for x in buttons_coord:
        pygame.draw.rect(screen, (50, 92, 102), x, 0)


def main_menu(main_or_esc=True):
    global forward, back, left, right, shooting
    key = ''  # !!!!!
    control_list = [forward, back, left, right, shooting]
    pygame.init()
    screen = pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()
    s = m = W - 550
    if main_or_esc:
        buttons, screen_value = menu(screen)
    else:
        buttons, screen_value, sounds, sound, music = options(s, m)
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
                                buttons, screen_value, sounds, sound, music = options(s, m)
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
                            buttons, screen_value, sounds, sound, music = options(s, m)
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
                            buttons, screen_value, sounds, sound, music = options(s, m)
                    for i in buttons:
                        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                            if buttons.index(i) == 3:  # back
                                if main_or_esc:
                                    buttons, screen_value = menu(screen)
                                else:
                                    running = False
                            elif buttons.index(i) == 2:  # control
                                buttons, screen_value = control(forward, back, left, right, shooting)
                                break

                elif screen_value == 'control':
                    if buttons[0][0] <= x <= buttons[0][0] + buttons[0][2] and buttons[0][1] <= y <= buttons[0][1] + \
                            buttons[0][3]:
                        buttons, screen_value, sounds, sound, music = options(s, m)
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
                        forward, back, left, right, shooting = control_list
                        control(forward, back, left, right, shooting)
                        control_list = [forward, back, left, right, shooting]
                elif screen_value == 'newgame':
                    return
            if event.type == pygame.KEYDOWN:
                if event.key in range(97, 122):
                    if screen_value == 'control':
                        if chr(event.key).upper() in control_list and '' not in control_list:
                            key = control_list.index(chr(event.key).upper())
                            control_list[control_list.index(chr(event.key).upper())] = ''
                            forward, back, left, right, shooting = control_list
                            control(forward, back, left, right, shooting)
                        elif chr(event.key).upper() not in control_list and key != '':
                            control_list[key] = chr(event.key).upper()
                            forward, back, left, right, shooting = control_list
                            control(forward, back, left, right, shooting)
                            key = ''
                        control_list = [forward, back, left, right, shooting]
        clock.tick(60)
        pygame.display.flip()
    if main_or_esc:
        pygame.quit()
