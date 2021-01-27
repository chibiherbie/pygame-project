import sys
import pygame
from game import WIDTH, HEIGHT, start_game, FPS, Transition
from level import Level, Wind, LeavesMain
from hero import Hero, AnimatedSprite
from random import randrange
from pygame.locals import *
from network import Network
import os


def draw_text(text, font, color, surface, x, y, w=0):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if w:
        w = textrect.w // 2
    textrect.topleft = (x - w, y)
    surface.blit(textobj, textrect)


game_ready = False
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Ангкар')
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

font = pygame.font.SysFont(None, 20)
sound_click = pygame.mixer.Sound('data/sound/sound_click_btn.mp3')
sound_click.set_volume(0.1)


# background
def generation():
    global lvl, wind, player, player2

    player = Hero('data/image/hero1', 600, 385)
    player.add_group(wall, death, hero, all_sprites)

    player2 = Hero('data/image/hero2', 650, 385)
    player2.add_group(wall, death, hero, all_sprites)

    lvl = Level('menu', level, all_sprites, wall, background, layer_2, layer_1, layer_front, lever,
                door, death, save_point, button, screen, leaves)

    for i in lvl.water:
        screen.blit(i.draw(), (i.rect[0], i.rect[1]))

    wind = Wind('data/levels/' + '1_level' + '/sound_environment')


def back_upd(scr):

    background.draw(scr)
    all_sprites.draw(scr)

    p_x, p_y = 0, 0
    player.move(p_x, p_y)
    player2.move(p_x, p_y)

    # UPD rope with button and draw
    for i in button:
        i.rope.wind(-wind.speed_x / randrange(50, 55))  # i.rope.wind(-wind.speed_x / randrange(7, 10))
        i.upd_rope()

    hero.draw(scr)
    all_sprites.update()

    # UPDATE LEAVES #
    if len(leaves) < 40:
        for i in range(40 - len(leaves)):
            LeavesMain(screen, leaves)
    wind.update()
    leaves.update(wind)
    leaves.draw(scr)


def main_menu():
    global game_ready
    generation()

    game_ready = False
    while True:
        back(screen, (250, 250, 250, 0))

        font4 = pygame.font.Font(None, 70)
        font = pygame.font.Font(None, 25)

        draw_text('Ангкар', font4, (0, 0, 0), screen, 160, 200)
        draw_text('Начать новую игру', font, (0, 0, 0), screen, 162, 280)
        draw_text('Настройки', font, (0, 0, 0), screen, 200, 480)
        draw_text('Продолжить', font, (0, 0, 0), screen, 130, 380)
        draw_text('Найти лобби', font, (0, 0, 0), screen, 250, 380)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(120, 300, 250, 50)
        button_2 = pygame.Rect(120, 500, 250, 50)
        button_3 = pygame.Rect(120, 400, 125, 50)
        button_4 = pygame.Rect(250, 400, 120, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                sound_click.play()
                lobby()
        if button_2.collidepoint((mx, my)):
            if click:
                sound_click.play()
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                sound_click.play()
                saved_games()
        if button_4.collidepoint((mx, my)):
            if click:
                sound_click.play()
                lobby_enter()

        pygame.draw.rect(screen, (120, 120, 120), button_1)
        pygame.draw.rect(screen, (120, 120, 120), button_2)
        pygame.draw.rect(screen, (120, 120, 120), button_3)
        pygame.draw.rect(screen, (120, 120, 120), button_4)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                pass
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # fps_text = pygame.font.Font(None, 40).render(str(int(mainClock.get_fps())), True, (100, 255, 100))
        # screen.blit(fps_text, (0, 0))
        mainClock.tick(FPS)
        if transition.type:
            transition.update()
            if transition.time_count == -transition.max_time:
                transition.type = ''
                transition.start()

        if game_ready:
            break

        pygame.display.flip()


def options():
    font4 = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 40)

    running = True
    while running:
        back(screen, (200, 200, 200, 100))
        draw_text('Общая громкость', font, (0, 0, 0), screen, 20, 100)
        draw_text('Громкость музыки', font, (0, 0, 0), screen, 20, 140)
        draw_text('Настройки', font4, (0, 0, 0), screen, 200, 20)
        button_10 = pygame.Rect(250, 800, 120, 50)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(FPS)


def lobby_enter():
    font4 = pygame.font.Font(None, 70)
    window = pygame.Rect(WIDTH // 2 - 300 // 2, HEIGHT // 2 - 100 // 2, 300, 100)
    code = 'c o d e'
    color_rect = [230, 230, 230]

    running = True
    while running:
        back(screen, (200, 200, 200, 100))

        draw_text('Введите код команты', font4, (0, 0, 0), screen, WIDTH // 2, 40, 1)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_RETURN:
                    net = Network(''.join(code.lower().split()))
                    if net.isConnect:
                        sound_click.play()
                        lobby(net)
                        return
                    else:
                        color_rect = [230, 100, 100]
                elif event.key == K_BACKSPACE:
                    code = code[:-2]
                elif len(code) < 7:
                    code += event.unicode + ' '
                    if len(code) == 8:
                        code = code[:-1]

        pygame.draw.rect(screen, color_rect, window)
        draw_text(code, font4, (0, 0, 0), screen, window.centerx, window.y + window.h // 3, 1)

        if color_rect[1] != 230:
            color_rect[1] += 1
            color_rect[2] += 1

        pygame.display.update()
        mainClock.tick(FPS)


def lobby(net=None, save=None):
    global game_ready

    start_t = False

    font4 = pygame.font.Font(None, 70)
    window1 = pygame.Rect(WIDTH * 10 // 100, HEIGHT * 20 // 100, 200, 300)
    window2 = pygame.Rect(WIDTH - 200 - WIDTH * 10 // 100,  HEIGHT * 20 // 100, 200, 300)
    window_code = pygame.Rect(WIDTH // 2 - 100, window1.y + window1.h // 2 - 25, 200, 50)

    button_start = pygame.Rect(WIDTH // 2 - 200, HEIGHT - HEIGHT * 20 // 100, 400, 100)
    start = False
    bnt_start = False

    isPlayer2 = True
    coor = 0
    if not net:
        net = Network('')
        bnt_start = True
        isPlayer2 = False
        if not save:
            with open('data/save/' + str(len(os.listdir('data/save')) + 1) + '_save_1.txt', mode='w') as f:
                f.write('650, 700, 440')
            save = os.listdir('data/save')[-1]
            coor = '650, 700, 440'

    if save and not coor:
        with open('data/save/' + save, mode='r') as f:
            coor = f.read()
    print(coor, save)

    code = net.open
    code = ' '.join(list(code))

    pl1 = AnimatedSprite('data/image/hero1', 3, 1, 0, 0, (75, 110))
    pl2 = AnimatedSprite('data/image/hero2', 3, 1, 0, 0, (75, 110))

    running = True
    while running:
        back(screen, (200, 200, 200, 100))

        # обнуляем данные
        count_lobby = 1
        mx, my = pygame.mouse.get_pos()
        click = False
        status_2 = (255, 150, 154)

        for event in pygame.event.get():
            if event.type == QUIT:
                a = net.send((start, 0, 0))
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    a = net.send((start, 0, 0))
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # title
        draw_text('ЛОББИ', font4, (0, 0, 0), screen, WIDTH // 2, 40, 1)

        # network
        a = net.send((start, 1, (save, coor)))
        if start or a[0]:
            start_t = True
        if a[1]:
            count_lobby = 2
            status_2 = (143, 200, 154)
        if not save:
            print(a[2][0], a[2][1])
            with open('data/save/' + a[2][0], mode='w') as f:
                f.write(a[2][1])
            save = a[2][0]
            coor = a[2][1]

        # рисуем ячейки для игроков
        pygame.draw.rect(screen, (240, 240, 240), window1)
        pygame.draw.rect(screen, (0, 0, 0), window1, 5)
        pygame.draw.rect(screen, (240, 240, 240), window2)
        pygame.draw.rect(screen, (0, 0, 0), window2, 5)
        draw_text('в сети', font4, (143, 200, 154), screen,
                  window1.centerx, window1.y + window1.h - window1.h / 5, 1)
        draw_text('в сети', font4, status_2, screen,
                  window2.centerx, window2.y + window2.h - window2.h / 5, 1)

        # рисуем код
        pygame.draw.rect(screen, (240, 240, 240), window_code)
        pygame.draw.rect(screen, (143, 200, 154), window_code, 2)
        draw_text(code, font4, (143, 200, 154), screen,
                  window_code.centerx, window_code.y, 1)

        # рисуем игроков
        pl1.update((0, 0))
        pl2.update((0, 0))
        screen.blit(pl1.image, (window1.x + window1.w // 2 - pl1.rect.w,
                                window1.y + window1.h // 2 - pl1.rect.h))
        screen.blit(pl2.image, (window2.x + window2.w // 2 - pl2.rect.w,
                                window2.y + window2.h // 2 - pl2.rect.h))

        # кнпока старта
        if bnt_start:
            pygame.draw.rect(screen, (240, 240, 240,), button_start)
            draw_text('НАЧАТЬ ИГРУ', font4, (0, 0, 0), screen,
                      button_start.centerx, button_start.y + 27, 1)

        if button_start.collidepoint((mx, my)) and bnt_start:
            if click and count_lobby == 2:
                sound_click.play()
                start = True

        # анимация перехода в игру
        if start_t:
            transition.update()
            pygame.mixer.music.fadeout(2000)
            if transition.time_count == 0:
                game_ready = True
                start_game(net, save)
                return
        if count_lobby == 1 and isPlayer2:
            print('ВЫХОД')
            return

        pygame.display.update()
        mainClock.tick(FPS)


def saved_games():
    font4 = pygame.font.Font(None, 70)

    save_scr = []
    for i in range(2, 7):
        save_scr.append(pygame.Rect(WIDTH // 2 - 100, HEIGHT * (i * 10) // 100 + 50, 200, 50))

    file = os.listdir('data/save')

    running = True
    while running:
        back(screen, (200, 200, 200, 100))
        draw_text('Сохранённые игры', font4, (0, 0, 0), screen, WIDTH // 2, HEIGHT * 10 // 100, 1)
        mx, my = pygame.mouse.get_pos()

        # рисуем сохранения
        for btn in save_scr:
            pygame.draw.rect(screen, (255, 255, 255), btn)
        for i in range(len(file)):
            draw_text('save ' + str(i + 1), font4, (0, 0, 0), screen,
                      save_scr[i].centerx, save_scr[i].y + 0, 1)

        # проверяем на клик
        for btn in save_scr:
            if btn.collidepoint((mx, my)):
                if click:
                    sound_click.play()
                    lobby(save=file[save_scr.index(btn)])
                    return

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(FPS)


def back(screen, color):
    back_upd(screen)

    # затемняем картинку
    f = pygame.Surface(screen.get_size()).convert_alpha()
    pygame.draw.rect(f, color, (0, 0, WIDTH, HEIGHT))
    screen.blit(f, (0, 0))


def start_screen():
    upd = 254
    side = 1
    img_s = pygame.image.load('data/levels/menu/start_image.png')
    img_s = pygame.transform.scale(img_s, (WIDTH, HEIGHT))
    while True:
        screen.blit(img_s, (0, 0))
        if upd >= 255:
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        f = pygame.Surface(screen.get_size()).convert_alpha()

        # затемняем картинку
        pygame.draw.rect(f, (0, 0, 0, upd), (0, 0, WIDTH, HEIGHT))
        screen.blit(f, (0, 0))

        if upd == 0:
            side = -1
        if upd < 150:
            speed = 1
        elif upd < 20:
            speed = 0.2
        else:
            speed = 2

        upd -= speed * side

        pygame.display.flip()
        mainClock.tick(FPS)


if __name__ == '__main__':
    # start_screen()
    while True:
        # музыка
        pygame.mixer.music.load('data/music/3.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        # обнуляем группы
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

        transition = Transition(screen)

        main_menu()