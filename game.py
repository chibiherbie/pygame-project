import pygame
import pygame_gui
from pygame.locals import *
from hero import Hero
from level import Level
from game_menu import GameMenu
from network import Network
import pickle


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
WIDTH, HEIGHT = 1000, 1000
RECT_HERO = (32, 58)


def main_loop(name_level):
    pygame.init()
    pygame.display.set_caption('GAME')

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF)
    # screen.set_alpha(None)

    running = True

    # внутриигровое меню
    show_manager = False
    game_menu = GameMenu(screen, size, FPS)

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

    with open('data/save/1_save.txt') as f:
        save_pos = f.read()

    player = n.getP()
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
                door, death, save_point)
    camera = Camera(player)

    # основной цикл
    while running:
        screen.fill(pygame.Color('white'))
        check = False

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
            if i.rect.x <= player.rect.x and not i.active:  # если пересекаем точку сохранения
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

        pl2 = n.send((p_x, p_y, check))
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

        camera.apply(background.sprites()[0], -3)

        # если спрайт не в зоне нашего зрения, он не рисуется
        for obj in all_sprites:
            if -obj.rect.width <= obj.rect.x <= WIDTH and -obj.rect.height <= obj.rect.y <= HEIGHT:
                draw_sprite.add(obj)

        # рисуем все объекты
        background.draw(screen)
        draw_sprite.draw(screen)
        hero.draw(screen)

        all_sprites.update()

        # очищаем спарйты
        draw_sprite.empty()

        if show_manager:
            game_menu.draw()  # рисуем внутриигровое меню

        time.tick(FPS)
        pygame.display.flip()
        # pygame.display.update(pygame.rect.Rect(0, 0, 100, 100))

    pygame.quit()


if __name__ == '__main__':
    # подключаемся к серверу
    n = Network('')

    while True:
        a = main_loop('1_level')
        if a != 'reset':
            break