import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, os_name, pos_x, pos_y, wall, *group):
        super().__init__(*group)  # вызываем конструктор родительского класса Sprite

        self.image = pygame.image.load(os_name)
        self.image = pygame.transform.scale(self.image, (35, 60))  # размер изображения

        self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.wall = wall
        self.isGround = False  # на змеле ли пресонаж?
        self.speed = 7  # сила прыжка
        self.gravity = 0.3

        self.xvel, self.yvel = 0, 0

    # передвижение персонажа
    def update(self, x, y):
        self.xvel = x

        if not self.isGround:
            self.yvel += self.gravity

        self.isGround = False

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        wall = pygame.sprite.spritecollide(self, self.wall, False)  # касаемся ли мы стен
        if wall:  #
            self.rect.x -= self.xvel

            for spr in pygame.sprite.spritecollide(self, self.wall, False):  # for spr in wall:
                if self.yvel > 0:
                    self.rect.bottom = spr.rect.top
                    self.isGround = True
                    self.yvel = 0

                if self.yvel < 0:  # если столкнулись с блоком сверху нас
                    self.rect.top = spr.rect.bottom
                    self.yvel = 0

        if y:  # прыжок
            if self.isGround:
                self.yvel = -self.speed
                self.isGround = False