import pygame
import pygame_gui
from pygame.locals import *
from hero import Hero
from level import Level, LeavesMain, Wind
from game_menu import GameMenu
from network import Network
from objects import upd_player_water
from random import randrange


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, player):
        self.player = player

        self.dx = player.rect.x
        self.dy = player.rect.y

        self.parx = player.rect.x
        self.pary = player.rect.y

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, layer):
        # рисуем в зависимоти от плана
        if layer == 0:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        elif layer == -2:
            obj.rect.x += self.dx * 0.2
            # obj.rect.y += self.dy * 0.2
        elif layer == -1:
            obj.rect.x += self.parallax_x(60)
        elif layer == 1:
            obj.rect.x += self.parallax_x(40)
        else:
            obj.rect.x += self.dx * 0.4
            obj.rect.y += self.dy * 0.4

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2) // 40
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2) // 40

    def parallax_x(self, num):
        return -(self.player.rect.x + self.player.rect.w // 2 - WIDTH // 2) // num

    def parallax_y(self, num):
        return -(self.player.rect.y + self.player.rect.h // 2 - HEIGHT // 2) // num


class Transition:
    def __init__(self, screen):
        self.time_count = 0
        self.max_time = 60
        self.type = 'start and go!!!'
        self.screen = screen

    def start(self):
        self.time_count = 60
        self.max_time = self.time_count
        self.frame = self.screen

    def update(self):
        mask = pygame.Surface(SIZE)
        pygame.draw.circle(mask, (255, 255, 255), (WIDTH // 2, HEIGHT // 2), (self.time_count / self.max_time) ** 4 * WIDTH)
        mask.set_colorkey((255, 255, 255))
        self.screen.blit(mask, (0, 0))

        if 't' in self.type:
            self.type = self.type[:-1]
            return
        self.time_count -= 1


def player_with_obj(action, type, value, door):
    if type == 'door':  # исп объект дверь
        for i in door.sprites():
            if i.value == value:  # ищем дверь приявзаную к нажатому рычагу
                # взаимодействуем с дверью
                if not action:
                    i.upd = 1
                else:
                    i.upd = -1


def load_save_point(player, player2, pos_new):
    pass


FPS = 60
SIZE = WIDTH, HEIGHT = 1000, 700
RECT_HERO = (32, 58)
NETWORK = None


def main_loop(name_level):
    pygame.display.set_caption('GAME')

    screen = pygame.display.set_mode(SIZE, HWSURFACE | DOUBLEBUF)
    # screen.set_alpha(None)

    running = True

    # внутриигровое меню
    show_manager = False
    game_menu = GameMenu(screen, SIZE, FPS)

    # перемещение
    p_x = 0
    p_y = 0

    time = pygame.time.Clock()

    # группы спрайтов
    draw_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    level = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    death = pygame.sprite.Group()
    hero = pygame.sprite.Group()
    background = pygame.sprite.Group()
    layer_2 = pygame.sprite.Group()
    layer_1 = pygame.sprite.Group()
    layer_front = pygame.sprite.Group()
    lever = pygame.sprite.Group()
    door = pygame.sprite.Group()
    save_point = pygame.sprite.Group()
    button = pygame.sprite.Group()
    leaves = pygame.sprite.Group()

    with open('data/save/1_save.txt') as f:
        save_pos = f.read()

    player = NETWORK.getP()
    player.add_group(wall, death, hero, all_sprites)

    pos_new = save_pos.split(',')

    if player.os_name == 'data/image/hero1':
        player2 = Hero('data/image/hero2', int(pos_new[1]), int(pos_new[2]))
        player.rect = player.rect.move(int(pos_new[0]), int(pos_new[2]))
    else:
        player2 = Hero('data/image/hero1', int(pos_new[0]), int(pos_new[2]))
        player.rect = player.rect.move(int(pos_new[1]), int(pos_new[2]))
    player2.add_group(wall, death, hero, all_sprites)

    # вместо пути, после запуска игры, будет передеваться индекс уровня или его название
    lvl = Level(name_level, level, all_sprites, wall, background, layer_2, layer_1, layer_front, lever,
                door, death, save_point, button, screen, leaves)

    # размещаем воду
    for i in lvl.water:
        screen.blit(i.draw(), (i.rect[0], i.rect[1]))

    camera = Camera(player)

    # переход при смерти. в будущем для перемещения в новое место
    transition = Transition(screen)

    # ветер
    wind = Wind('data/levels/' + name_level + '/sound_environment')

    # основной цикл
    while running:
        screen.fill(pygame.Color('white'))
        check = False

        lvl.update()

        with open('data/save/1_save.txt', mode='w') as f:
            f.write(save_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # запускаем внутриигровое меню
                    show_manager = not show_manager
                    game_menu.settings_show = False
                if event.key == pygame.K_f:
                    check = player.check_objects(lever)   # проверка на пересечение с объектами, в случаи успеха отклик
                    if check:
                        player_with_obj(check[0], check[1], check[2], door)
            if show_manager:
                answer = game_menu.update_manager(event)
                # если были нажаты кнопки
                if answer == 'res':
                    show_manager = False
                elif answer == 'exit':
                    running = False
                elif answer == 'menu':
                    print('ВЫХОД В МЕНЮ')

        for i in save_point.sprites():
            if (i.rect.x <= player.rect.x or i.rect.x <= player2.rect.x) and not i.active:  # если пересекаем точку сохранения
                i.active = True
                # записываем координаты точек для персонажей в файл
                save_pos = f'{i.pos_player[0]}, {i.pos_player[1]}, {i.pos_player[2]}'

        if player.death_colide or player2.death_colide:
            player.death_colide, player2.death_colide = False, False
            # load_save_point(player, player2, save_pos)
            return 'reset'

        # перемещение персонажа
        key = pygame.key.get_pressed()
        # if key[pygame.K_DOWN]:
        #     hero.update(0, 1)
        if key[pygame.K_UP]:
            p_y = 1
        if key[pygame.K_RIGHT]:
            p_x = 5
        if key[pygame.K_LEFT]:
            p_x = -5
        if key[pygame.K_UP]:
            p_y = 1

        # если включено внетриигровое меню, то двигать персонажем нельзя, но всё окружение работает
        if show_manager:
            p_x, p_y = 0, 0

        if check:
            check = True

        pl2 = NETWORK.send((p_x, p_y, check))
        if pl2[0] == 'stop':
            running = False
        player2.move(int(pl2[0]), int(pl2[1]))
        if pl2[2]:
            check = player2.check_objects(lever)  # проверка на пересечение с объектами, в случаи успеха отклик
            if check:
                player_with_obj(check[0], check[1], check[2], door)

        # двигаем игрока
        player.move(p_x, p_y)
        p_x, p_y = 0, 0

        # двигаем объекты за персонажем
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite, 0)

        for sprite in layer_2:
            camera.apply(sprite, -2)

        for sprite in layer_1:
            camera.apply(sprite, -1)

        for sprite in layer_front:
            camera.apply(sprite, 1)

        for back in background:
            back.rect.x += camera.dx

        # если спрайт не в зоне нашего зрения, он не рисуется
        for obj in all_sprites:
            if -obj.rect.width <= obj.rect.x <= WIDTH and -obj.rect.height <= obj.rect.y <= HEIGHT:
                draw_sprite.add(obj)

        # # рисуем все объекты
        # for back in background:
        #     if -back.rect.width <= back.rect.x <= WIDTH and -back.rect.height <= back.rect.y <= HEIGHT:
        #         background[0].draw()

        background.draw(screen)
        draw_sprite.draw(screen)
        hero.draw(screen)

        all_sprites.update()

        # очищаем спарйты
        draw_sprite.empty()

        # UPDATE LEAVES #
        for i in leaves:
            camera.apply(i, 0)

        if len(leaves) < 40:
            for i in range(40 - len(leaves)):
                a = LeavesMain(screen, leaves)
                camera.apply(a, 0)

        wind.update()
        leaves.update(wind)
        leaves.draw(screen)

        # UPDATE WATER #
        for i in lvl.water:
            i.upd_camera(camera.dx, camera.dy, WIDTH, HEIGHT, screen)

        upd_player_water(player, lvl.water, all_sprites)
        upd_player_water(player2, lvl.water, all_sprites)
        ######

        # UPD rope with button
        for i in button:
            i.rope.wind(-wind.speed_x / randrange(50, 55))  # i.rope.wind(-wind.speed_x / randrange(7, 10))

        # стоим ли мы на объекте кнопка
        if not player2.btn:
            player.player_stay_button(button, door)
        if not player.btn:
            player2.player_stay_button(button, door)

        if show_manager:
            game_menu.draw()  # рисуем внутриигровое меню

        if transition.type:
            transition.update()
            if transition.time_count == -transition.max_time:
                transition.type = ''
                transition.start()

        if player.stop_death >= 30 or player2.stop_death >= 30:
            transition.update()
            if transition.time_count == 0:
                player.death_colide = True

        # выводим фпс
        fps_text = pygame.font.Font(None, 40).render(str(int(time.get_fps())), True, (100, 255, 100))
        screen.blit(fps_text, (0, 0))

        time.tick(FPS)
        # pygame.display.flip()
        pygame.display.update()

    pygame.quit()


def start_game():
    global NETWORK
    # инициализируем
    pygame.init()

    # подключаемся к серверу
    NETWORK = Network('')

    pygame.mixer.music.load('data/music/1.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    while True:
        a = main_loop('1_level')
        if a != 'reset':
            break


if __name__ == '__main__':
    start_game()