import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, os_name, pos_x, pos_y, *group):
        super().__init__(*group)  # вызываем конструктор родительского класса Sprite

        self.image = pygame.image.load(os_name)
        self.image = pygame.transform.scale(self.image, (100, 100))  # размер ихображения

        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

        self.x, self.y = 0, 0

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
