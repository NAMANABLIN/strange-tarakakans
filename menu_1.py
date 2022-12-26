import pygame

from config import *

size = width, height = 800, 600


def menu(screen):
    pygame.display.set_caption('menu')
    screen.fill((60, 113, 125))
    pygame.display.flip()
    buttons_coord = [(width // 2 - 190 // 2, height - 100, 190, 50), (width // 2 - 190 // 2, height - 160, 190, 50),
                     (width // 2 - 190 // 2, height - 220, 190, 50), (width // 2 - 190 // 2, height - 280, 190, 50)]
    button(buttons_coord, screen)

    text = font.render("Продолжить", 1, font_color)
    screen.blit(text, (width // 2 - 190 // 2, height - 280, 180, 50))

    text = font.render("Новая игра", 1, font_color)
    screen.blit(text, (width // 2 - 190 // 2 + 17, height - 220, 180, 50))

    text = font.render("Настройки", 1, font_color)
    screen.blit(text, (width // 2 - 190 // 2 + 20, height - 160, 180, 50))

    text = font.render("Выйти", 1, font_color)
    screen.blit(text, (width // 2 - 190 // 2 + 45, buttons_coord[0][1]))

    pygame.display.flip()
    screen_value = 'menu'
    return buttons_coord, screen_value


def newgame():
    screen = pygame.display.set_mode(size)
    screen_value = 'newgame'
    return screen_value


def continuegame():
    screen = pygame.display.set_mode(size)
    # screen_value = 'continue'


def control():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('control')
    screen.fill((60, 113, 125))
    screen.blit(font.render("Вперёд          W", 1, font_color), (width // 30 + 10, height - 550, 180, 50))
    screen.blit(font.render("Назад             S", 1, font_color), (width // 30 + 10, height - 515, 180, 50))
    screen.blit(font.render("Влево             A", 1, font_color), (width // 30 + 10, height - 485, 180, 50))
    screen.blit(font.render("Вправо           D", 1, font_color), (width // 30 + 10, height - 450, 180, 50))
    screen.blit(font.render("Стрельба        ЛКМ", 1, font_color), (width // 30 + 10, height - 415, 180, 50))
    buttons_coord = [(width // 2 - 190 // 2, height - 100, 190, 50)]
    pygame.draw.rect(screen, (50, 92, 102), buttons_coord[0], 0)
    text = font.render("Назад", 1, font_color)
    screen.blit(text, (width // 2 - 190 // 2 + 50, height - 100))
    screen_value = 'control'
    return buttons_coord, screen_value


def options():
    pygame.display.set_caption('options')
    screen = pygame.display.set_mode(size)
    screen.fill((60, 113, 125))
    screen_value = 'options'

    buttons_coord = [(width // 30, height - 480, 190, 50), (width // 30, height - 420, 190, 50),
                     (width // 30, height - 360, 190, 50), (width // 30, height - 300, 190, 50)]

    button(buttons_coord, screen)

    text = font.render("Звук", 1, font_color)
    screen.blit(text, (width // 30 + 60, height - 480, 180, 50))

    text = font.render("Музыка", 1, font_color)
    screen.blit(text, (width // 30 + 40, height - 420, 180, 50))

    text = font.render("Управление", 1, font_color)
    screen.blit(text, (width // 30 + 10, height - 360, 180, 50))

    text = font.render("Назад", 1, font_color)
    screen.blit(text, (width // 30 + 55, height - 300))

    pygame.draw.line(screen, (58, 65, 66), (width - 550, height - 455), (width - 300, height - 455), width=5)
    pygame.draw.line(screen, (58, 65, 66), (width - 550, height - 395), (width - 300, height - 395), width=5)

    sound = pygame.draw.rect(screen, (50, 92, 102), (width - 550, height - 470, 10, 30))
    music = pygame.draw.rect(screen, (50, 92, 102), (width - 550, height - 410, 10, 30))

    sounds = [(sound.x, sound.y, 10, 30), (music.x, music.y, 10, 30)]

    pygame.display.flip()

    return buttons_coord, screen_value, sounds, sound, music


def button(buttons_coord, screen):
    pygame.draw.rect(screen, (50, 92, 102), buttons_coord[0], 0)
    pygame.draw.rect(screen, (50, 92, 102), buttons_coord[1], 0)
    pygame.draw.rect(screen, (50, 92, 102), buttons_coord[2], 0)
    pygame.draw.rect(screen, (50, 92, 102), buttons_coord[3], 0)


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode(size)

    buttons, screen_value = menu(screen)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if screen_value == 'menu':
                    for i in buttons:
                        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                            if buttons.index(i) == 0:  # exit
                                running = False
                            elif buttons.index(i) == 1:  # options
                                buttons, screen_value, sounds, sound, music = options()
                                print(sounds)
                            elif buttons.index(i) == 2:  # new game
                                screen_value = newgame()
                            elif buttons.index(i) == 3:  # continue
                                pass
                                # continuegame()
                if screen_value == 'options':
                    if sounds[0][0] <= x <= sounds[0][0] + sounds[0][2] and sounds[0][1] <= y <= sounds[0][1] + \
                            sounds[0][3]:  # sound
                        if pygame.mouse.get_pressed()[0]:
                            pass
                    if sounds[1][0] <= x <= sounds[1][0] + sounds[1][2] and sounds[1][1] <= y <= sounds[1][1] + \
                            sounds[1][3]:  # music
                        if pygame.mouse.get_pressed()[0]:
                            pass
                    for i in buttons:
                        if i[0] <= x <= i[0] + i[2] and i[1] <= y <= i[1] + i[3]:
                            if buttons.index(i) == 3:  # back
                                buttons, screen_value = menu(screen)
                            elif buttons.index(i) == 2:  # control
                                buttons, screen_value = control()
                                break
                if screen_value == 'control':
                    if buttons[0][0] <= x <= buttons[0][0] + buttons[0][2] and buttons[0][1] <= y <= buttons[0][1] + \
                            buttons[0][3]:
                        buttons, screen_value, sounds, sound, music = options()
                if screen_value == 'newgame':
                    running = False
        pygame.display.flip()
        clock.tick(60)
