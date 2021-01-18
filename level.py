import pygame
import os
from objects import Lever, Door, Spikes, SavePoint
from random import choice, shuffle


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
                 layer_front, lever, door, death, save_point):
        self.lvl = lvl
        self.all_sprite = sprite
        self.wall = wall
        self.lever = lever
        self.door = door
        self.death = death
        self.save_point = save_point
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
                elif level[y][x] == '_':
                    if int(level[y][x + 1] + level[y][x + 2]) not in self.water_pos:
                        self.water_pos[int(level[y][x + 1] + level[y][x + 2])] = [x * tile_width,
                                                                                  y * tile_height]
                    else:
                        pos = [0, 100]
                        self.water.append(Water(pos[0], pos[1], 500, 500, 5))

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


class Spring:
    k = 0.02  # коэф пружины
    d = 0.025  # коэф "влажности"

    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.max_y = y  # естественное положение верхней части пружины
        self.velocity = 0

    def update(self):
        x = self.y_pos - self.max_y  # смещение пружины от начала

        a = -self.k * x - self.d * self.velocity  # ускорение

        self.y_pos += self.velocity
        self.velocity += a


class Water:
    def __init__(self, x_s, y_s, x_e, y_e, spring_segment):
        self.springs = []
        self.x_s = x_s
        self.y_s = y_s
        self.x_e = x_e
        self.y_e = y_e
        self.spring_segment = spring_segment

        self.rect = pygame.Rect(self.x_s, self.y_s, self.x_e, self.y_e)

        print(x_s, y_s, x_e, y_e)
        print('SURFACE:', (self.x_e - self.x_s, self.y_e - self.y_s))
        print(self.rect)

        self.passes = 20
        self.spread = 0.06  # скорость распространения волн

        self.upd_camera()

    def update(self):
        for i in self.springs:
            i.update()
        left_d = [0.0] * len(self.springs)
        right_d = [0.0] * len(self.springs)

        for _ in range(self.passes):
            for num in range(len(self.springs) - 1):
                if num > 0:
                    left_d[num] = self.spread * (self.springs[num].y_pos - self.springs[num - 1].y_pos)
                    self.springs[num - 1].velocity += left_d[num]
                if num < len(self.springs) - 1:
                    right_d[num] = self.spread * (self.springs[num].y_pos - self.springs[num + 1].y_pos)
                    self.springs[num + 1].velocity += right_d[num]

            # обновляем скорость
            for num in range(len(self.springs) - 1):
                if num > 0:
                    self.springs[num - 1].y_pos += left_d[num]
                if num < len(self.springs) - 1:
                    self.springs[num + 1].y_pos += right_d[num]

    def draw(self):
        sur = pygame.Surface((self.x_e - self.x_s, self.y_e - self.y_s)).convert_alpha()  # self.x_e - self.x_s, self.y_e - self.y_s
        sur.fill((255, 255, 255))
        sur.set_alpha(100)
        for i in range(len(self.springs) - 1):
            pygame.draw.polygon(sur, (0, 255, 0), [(self.springs[i].x_pos, self.springs[i].y_pos),
                                                   (self.springs[i + 1].x_pos, self.springs[i + 1].y_pos),
                                                   (self.springs[i].x_pos, self.y_e)])
            pygame.draw.polygon(sur, (0, 255, 0), [(self.springs[i + 1].x_pos, self.springs[i + 1].y_pos),
                                                   (self.springs[i + 1].x_pos, self.y_e),
                                                   (self.springs[i].x_pos, self.y_e)])
        return sur

    def upd_camera(self):
        for i in range(abs(self.rect[2] - self.rect[0]) // self.spring_segment):
            self.springs.append(Spring(i * self.spring_segment + self.rect[0], self.rect[1]))
        self.springs.append(Spring(self.rect[2], self.rect[3]))

    def force(self, place, speed):
        self.springs[place].velocity = speed