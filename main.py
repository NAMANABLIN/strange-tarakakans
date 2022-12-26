from classes import *
from config import *
from random import randint
from menu_1 import main_menu

def generate_level(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return x, y


def load_level(filename):
    filename = os.path.join(filename)
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден.\n Возможно этого уровня нет в папке 'levels'")
        sys.exit()
    else:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


pg.init()
main_menu()

size = W, H = 800, 600
sc = pg.display.set_mode((800, 600))
pg.display.set_caption('Тараканы!')

clock = pg.time.Clock()
FPS = 60

speed = 15

enemies = []
for x in range(10):
    if randint(0,1):
        enemies.append(TarakanEnemy(randint(0, 350), randint(0, 250)))
    else:
        enemies.append(TarakanEnemy(randint(450, 800), randint(350, 600)))

player_bullets = []
camera = Camera(size)

level_x, level_y = generate_level(load_level('kek.txt'))
player = Player(400,300)
while True:
    sc.fill(MALAHIT)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    keys = pg.key.get_pressed()


    if keys[pg.K_LEFT] or keys[pg.K_a]:
        player.move('лево')
    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        player.move('право')
    if keys[pg.K_UP] or keys[pg.K_w]:
        player.move('вперёд')
    if keys[pg.K_DOWN] or keys[pg.K_s]:
        player.move('назад')

    bullets_group.update()
    enemys_group.update(player)
    tiles_group.draw(sc)
    wall_group.draw(sc)
    bullets_group.draw(sc)
    enemys_group.draw(sc)
    player_group.draw(sc)



    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    player.main(sc)

    lol = 10
    for x in range(player.hp):
        pg.draw.rect(sc, (255, 0, 0), (lol, 10, 30, 30))
        lol += 35

    pg.display.update()


    clock.tick(FPS)
