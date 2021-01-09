import pygame
import os
from objects import Lever


tile_images = {
        'floor': pygame.image.load('data/image/graphics/example.jpg'),
        'empty': pygame.image.load('data/image/graphics/grass.png'),
    }

tile_height = 50
tile_width = 50


class Level:
    def __init__(self, folder, lvl, sprite, wall, back, layer_2, layer_1, layer_front):
        self.lvl = lvl
        self.all_sprite = sprite
        self.wall = wall

        dir = 'data/levels/' + folder

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

    def generate_level(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y, self.lvl, self.all_sprite)
                elif level[y][x] == '#':
                    Tile('floor', x, y, self.wall, self.all_sprite)
                elif level[y][x] == '/':
                    Tile('floor', x, y, self.wall, self.all_sprite)
                    Lever(x, y - 1, tile_width, tile_height, self.all_sprite)

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
        self.image = tile_images[tile_type]

        self.image = pygame.transform.scale(self.image, (50, 50))  # размер изображения

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
