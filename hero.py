import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self,os_name, *group):
        super().__init__(*group)  # вызываем конструктор родительского класса Sprite

        self.image = pygame.image.load(os_name)
        self.image = pygame.transform.scale(self.image, (100, 100))  # размер ихображения

        self.rect = self.image.get_rect()

        self.x, self.y = 0, 0

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
