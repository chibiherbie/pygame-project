import pygame


class Hero(pygame.sprite.Sprite):
    def __init__(self, os_name, pos_x, pos_y, wall, *group):
        super().__init__(*group)  # вызываем конструктор родительского класса Sprite

        self.image = pygame.image.load(os_name)
        self.image = pygame.transform.scale(self.image, (30, 50))  # размер ихображения

        self.rect = self.image.get_rect().move(pos_x,pos_y)

        self.wall = wall
        self.isGround = False
        self.speed = 6
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

        for i in self.wall:
            if pygame.sprite.collide_rect(self, i):
                if self.yvel > 0:
                    self.rect.bottom = i.rect.top
                    self.isGround = True
                    self.yvel = 0
                if self.yvel < 0:
                    self.rect.top = i.rect.bottom
                    self.yvel = 0

        print(self.yvel)

        if pygame.sprite.spritecollideany(self, self.wall):
            self.rect.x -= self.xvel

        if y:
            if self.isGround:
                self.yvel = -self.speed
                self.isGround = False

        # if not player.isGround:
        #     player.rect.y += player.speed
        #
        #     if pygame.sprite.spritecollideany(player, wall):
        #         player.rect.y -= player.speed
        #         player.speed = -5
        #         player.isGround = True
        #     else:
        #         player.speed += 0.2