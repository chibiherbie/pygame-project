import pygame

tile_images = {
        'wall': load_image('example.png')
    }


class Level(pygame.sprite.Sprite):
    def __init__(self, name_level):
        self.tile_width = 50
        self.tile_height = 50

        super().__init__(player_group, all_sprites)
        self.image = tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (50, 50))  # размер изображения

        self.rect = self.image.get_rect().move(self.tile_width * pos_x, self.tile_height * pos_y)
        
        a = self.generate_level(self.load_level(name_level))

    def load_level(self, filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    
    def generate_level(self):
        pass