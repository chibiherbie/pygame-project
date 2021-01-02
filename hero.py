import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, os_name, pos_x, pos_y, wall, *group):
        super().__init__(*group)  # вызываем конструктор родительского класса Sprite

        self.image = pygame.image.load(os_name)
        self.image = pygame.transform.scale(self.image, (30, 50))  # размер ихображения

        self.rect = self.image.get_rect().move(pos_x,pos_y)

        self.x, self.y = 0, 0

        self.wall = wall
        self.isGround = True
        self.speed = -5

    def update(self, x, y):
        self.rect.x += x

        if pygame.sprite.spritecollideany(self, self.wall):
            self.isGround = True
            self.rect.x -= x

        if y:
            self.isGround = False