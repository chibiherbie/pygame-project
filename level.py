import pygame
import os
from objects import Lever, Door, Spikes, SavePoint, Water, Button
from random import choice, shuffle, randrange


tile_images = {
        'floor': pygame.image.load('data/image/graphics/platform-top.png'),
        'under': pygame.image.load('data/image/graphics/platform-bottom.png'),
        'left': pygame.image.load('data/image/graphics/platform-left.png'),
        'right': pygame.image.load('data/image/graphics/platform-right.png'),
    }

tile_height = 50
tile_width = 50


class Level:
    def __init__(self, folder, lvl, sprite, wall, back, layer_2, layer_1,
                 layer_front, lever, door, death, save_point, button, screen, leaves):
        self.lvl = lvl
        self.all_sprite = sprite
        self.wall = wall
        self.lever = lever
        self.button = button
        self.door = door
        self.death = death
        self.save_point = save_point
        self.screen = screen
        self.water_pos = {}

        self.water = []

        dir = 'data/levels/' + folder

        self.time_sound = 0  # таймер доп звуков
        self.sound_around = []  # доп звуки

        for sound in os.listdir(dir + '/sound_environment'):
            self.sound_around.append(pygame.mixer.Sound(dir + '/sound_environment/' + sound))
            self.sound_around[-1].set_volume(0.03)
            self.sound_around.append(pygame.mixer.Sound(dir + '/sound_environment/empty.mp3'))
        shuffle(self.sound_around)  # мешаем  звуки

        # загружаем спрайты в порядке иерархии по слоям (фон, 2 слой, 1 слой, плафтформа, передний план)
        Background('/'.join([dir, 'background.png']), back)
        self.layer_generation('/'.join([dir, 'layer_2.txt']), layer_2, sprite)
        self.layer_generation('/'.join([dir, 'layer_1.txt']), layer_1, sprite)
        self.generate_level(self.load_level('/'.join([dir, 'map.txt'])))
        self.layer_generation('/'.join([dir, 'layer_front.txt']), layer_front, sprite)

    def load_level(self, filename):
        filename = filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return level_map  # list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def update(self):
        self.time_sound += 1
        if self.time_sound == 1100:
            self.time_sound = 0
            choice(self.sound_around).play()

    def generate_level(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('under', x, y, self.wall, self.all_sprite)
                elif level[y][x] == '#':
                    Tile('floor', x, y, self.wall, self.all_sprite)
                elif level[y][x] == '-':
                    Tile('left', x, y, self.wall, self.all_sprite)
                elif level[y][x] == '+':
                    Tile('right', x, y, self.wall, self.all_sprite)
                elif level[y][x] == '/':
                    Lever(x, y, tile_width, tile_height, int(level[y][x + 1] + level[y][x + 2]),
                          self.lever, self.all_sprite)
                elif level[y][x] == '|':
                    Door(x, y - 1, tile_width, tile_height, int(level[y][x + 1] + level[y][x + 2]),
                         self.wall, self.door, self.all_sprite)
                elif level[y][x] == '"':
                    Spikes(x, y, tile_width, tile_height, self.death, self.all_sprite)
                elif level[y][x] == '!':
                    SavePoint(x, y, tile_width, tile_height, self.save_point, self.all_sprite)
                elif level[y][x] == '~':
                    if int(level[y][x + 1] + level[y][x + 2]) not in self.water_pos:
                        self.water_pos[int(level[y][x + 1] + level[y][x + 2])] = [x * tile_width,
                                                                                  y * tile_height]
                    else:
                        pos = self.water_pos[int(level[y][x + 1] + level[y][x + 2])]
                        self.water.append(Water(pos[0], pos[1], (x + 3) * tile_width,
                                                (y + 1) * tile_height, 4, self.all_sprite, 'water'))
                elif level[y][x] == '_':
                    if int(level[y][x + 1] + level[y][x + 2]) not in self.water_pos:
                        self.water_pos[int(level[y][x + 1] + level[y][x + 2])] = [x * tile_width,
                                                                                  y * tile_height]
                    else:

                        pos = self.water_pos[int(level[y][x + 1] + level[y][x + 2])]
                        self.water.append(Water(pos[0], pos[1], (x + 3) * tile_width,
                                                (y + 1) * tile_height, 4, self.all_sprite, 'swamp'))
                elif level[y][x] == '?':
                    Button(x, y - 1, tile_width, tile_height, int(level[y][x + 1] + level[y][x + 2]),
                          self.screen, self.button, self.all_sprite)

    def layer_generation(self, file, *layer):
        with open(file, mode='r', encoding='utf8') as f:
            data = f.readlines()

        for propertys in data:
            property = propertys.split()
            Layers('data/image/graphics/' + property[0], (int(property[1]), int(property[2])),
                   float(property[3]), layer)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = tile_images[tile_type].convert_alpha()

        self.image = pygame.transform.scale(self.image, (tile_width, tile_height))  # размер изображения

        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Background(pygame.sprite.Sprite):
    def __init__(self, os_name, *group):
        super().__init__(*group)
        self.image = pygame.image.load(os_name).convert_alpha()
        # self.image = self.image.subsurface(pygame.Rect(0, 0, 500, 800))  # размер изображения
        self.rect = self.image.get_rect().move(-150, 0)


class Layers(pygame.sprite.Sprite):
    def __init__(self, os_name, pos, scale, *group):
        super().__init__(*group)
        self.image = pygame.image.load(os_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() / scale),
                                                         int(self.image.get_height() / scale)))
        self.rect = self.image.get_rect().move(pos)


class Wind:
    def __init__(self, dir):
        self.speed_x = -1
        self.speed_y = 1
        self.power = 0
        self.transition_x = 0
        self.transition_y = 0

        self.time = 0

        self.sound = []
        for sound in os.listdir(dir):
            if 'windy' in sound:
                self.sound.append(pygame.mixer.Sound(dir + '/' + sound))
                self.sound[-1].set_volume(0.07)

    def get_speedx(self):
        return self.speed_x

    def update(self):
        self.time += 1

        if self.time == 1000:
            if self.power == 0:
                self.power = choice([0, 1, 0, 2, 0, 1, 0])  # 0, 1, 0, 2, 0, 1, 0
            else:
                self.power = 0
            self.time = 0
            # print('POWER:', self.power, self.speed_x)

        if self.power != 0 and self.time == 0:
            self.transition_x = -randrange(3, 6) * self.power
            self.t = 1
            self.sound[randrange(0, len(self.sound))].play()

        elif self.power == 0 and self.time == 0 and self.speed_x < -1:
            self.transition_x = self.speed_x + 1
            self.t = -1

        if self.transition_x < 0:
            self.speed_x += -0.05 * self.t
            self.transition_x += 0.05


class LeavesMain(pygame.sprite.Sprite):
    def __init__(self, screen, *group):
        super().__init__(*group)

        dir = 'data/image/graphics/'
        name = ['leaves_1.png', 'leaves_2.png', 'leaves_3.png', 'leaves_4.png']

        self.screen = screen

        self.image = pygame.image.load(dir + choice(name)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(randrange(0, screen.get_size()[0] + 500), randrange(-100, 0))
        if self.rect.x > screen.get_size()[0]:
            self.rect = self.rect.move(0, randrange(0, screen.get_size()[1] - screen.get_size()[1] // 4))
        self.image = pygame.transform.rotate(self.image, randrange(1, 100))

        self.rectx = self.rect.x
        self.recty = self.rect.y

        self.x = -randrange(1, 3)
        self.y = 0
        self.m = 1
        self.l = True

    def update(self, wind):
        self.rect.y += wind.speed_y - self.x
        self.rect.x += wind.speed_x + self.x

        if wind.time % 100 == 0:
            self.x = -randrange(1, 3)

        # ------------------------------ПЛАВНОЕ ДВИЖЕНИЕ ЛИСТВЫ --------------------------------
        # self.rectx += wind.speed_x + self.x
        # self.recty += wind.speed_y - self.y
        #
        # if wind.power == 0 and wind.time > 150:
        #     t = choice([0.03, 0.08, 0.05])
        #     if self.l:
        #         self.x += t
        #         self.m -= t
        #     elif not self.l:
        #         self.x -= t
        #         self.m += t
        #
        #     if self.m > 1:
        #         self.y += 0.05
        #     elif -1 < self.m < 1:
        #         if self.y > 0:
        #             self.y -= 0.07
        #     elif self.m < -1:
        #         self.y += 0.05
        #     if self.y < 0:
        #         self.y = 0
        # else:
        #     if self.x > 0:
        #         self.x = -randrange(1, 3)
        #
        # if self.m > 1.5 or self.m < -1.5:
        #     self.l = not self.l
        #
        # self.rect.y = self.recty  # wind.speed_y - self.y
        # self.rect.x = int(self.rectx)  # wind.speed_x + self.x
        # --------------------------------------------------------------------------------

        if not (-self.rect.width - 500 <= self.rect.x <= self.screen.get_size()[0] + 500 and
            -self.rect.height - 100 <= self.rect.y <= self.screen.get_size()[1] + 100):
            self.kill()
