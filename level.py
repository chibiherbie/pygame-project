import pygame

tile_images = {
        'floor': pygame.image.load('data/image/graphics/example.jpg'),
        'empty': pygame.image.load('data/image/graphics/grass.png')
    }

tile_height = 50
tile_width = 50


class Level:
    def __init__(self, name_level, lvl, sprite, wall, back, layer_2, layer_1):
        self.lvl = lvl
        self.all_sprite = sprite
        self.wall = wall
        self.generate_level(self.load_level(name_level))

        # генирация планов (в будущем при загрузке будут исп карты)
        Background('data/image/graphics/back.png', back)
        Layer2('data/image/graphics/tree2.png', 0, layer_2)
        Layer2('data/image/graphics/tree2.png', 400, layer_2)
        Layer1('data/image/graphics/tree.png', layer_1)

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
                else:
                    pass


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


class Layer1(pygame.sprite.Sprite):
    def __init__(self, os_name, *group):
        super().__init__(*group)
        self.image = pygame.image.load(os_name).convert_alpha()
        # self.image = self.image.subsurface(pygame.Rect(0, 0, 500, 800))  # размер изображения
        self.rect = self.image.get_rect().move(100, 200)


class Layer2(pygame.sprite.Sprite):
    def __init__(self, os_name, pos, *group):
        super().__init__(*group)
        self.image = pygame.image.load(os_name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2,
                                                         self.image.get_height() // 2))
        self.rect = self.image.get_rect().move(pos, 400)