import pygame

tile_images = {
        'floor': pygame.image.load('data/image/graphics/example.jpg'),
        'empty': pygame.image.load('data/image/graphics/grass.png')
    }

tile_height = 50
tile_width = 50


class Level:
    def __init__(self, name_level, lvl, sprite):
        self.lvl = lvl
        self.all_sprite = sprite
        self.generate_level(self.load_level(name_level))

    def load_level(self, filename):
        filename = filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    
    def generate_level(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y, self.lvl, self.all_sprite)
                elif level[y][x] == '#':
                    Tile('floor', x, y, self.lvl, self.all_sprite)
                else:
                    pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tiles_group, all_sprites):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]

        self.image = pygame.transform.scale(self.image, (50, 50))  # размер изображения

        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
