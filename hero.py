import pygame
import os
import random


class Hero(pygame.sprite.Sprite):
    def __init__(self, os_name, pos_x, pos_y, wall, *group):
        super().__init__(*group)  # вызываем конструктор родительского класса Sprite

        self.all_sprites = group[-1]

        # self.image = pygame.image.load(os_name)
        # self.image = pygame.transform.scale(self.image, (35, 60))  # размер изображения
        # self.rect = self.image.get_rect().move(pos_x, pos_y)

        self.wall = wall
        self.isGround = False  # на змеле ли пресонаж?
        self.speed = 7  # сила прыжка
        self.gravity = 0.3

        self.anim = AnimatedSprite(os_name, 3, 1, pos_x, pos_y)
        self.image = self.anim.image
        self.rect = self.anim.rect

        self.xvel, self.yvel = 0, 0

    # передвижение персонажа
    def move(self, x, y):
        self.image = self.anim.update((x, y))

        self.xvel = x

        if not self.isGround:
            self.yvel += self.gravity

        self.isGround = False

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        wall = pygame.sprite.spritecollide(self, self.wall, False)  # касаемся ли мы стен
        if wall:
            self.rect.x -= self.xvel

            for spr in pygame.sprite.spritecollide(self, self.wall, False):  # for spr in wall:
                if self.yvel > 0:
                    self.rect.bottom = spr.rect.top
                    self.isGround = True
                    self.yvel = 0

                if self.yvel < 0:  # если столкнулись с блоком сверху нас
                    self.rect.top = spr.rect.bottom
                    self.yvel = 0

        if self.isGround and self.xvel:
            self.create_particles((self.rect.x + self.rect.w // 2,
                                   self.rect.bottom - self.rect.h // 5), self.xvel)

        if y:  # прыжок
            if self.isGround:
                self.yvel = -self.speed
                self.isGround = False

    def create_particles(self, position, x):
        particle_count = 40  # количество создаваемых частиц
        for _ in range(particle_count):
            Particle(position, self.all_sprites, x)

    def check_objects(self, *group):
        for i in group:
            wall = pygame.sprite.spritecollide(self, i, False)  # касаемся ли мы объектов
            if wall:
                wall[0].animation()


class AnimatedSprite:
    def __init__(self, folder, columns, rows, x, y):
        self.frames = []
        self.anim = []

        # os.listdir(folder) - получаем название всех файлов в папке
        self.cut_sheet(folder, os.listdir(folder), columns, rows)

        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        self.upd = 0
        self.move = 0

    # режим заготовку на кадры
    def cut_sheet(self, folder, sheets, columns, rows):
        for count in range(len(sheets)):
            sheet = pygame.image.load(folder + '/' + sheets[count]).convert_alpha()  # загружаем файл

            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            self.frames = []
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    cut = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))  # размер изображения
                    self.frames.append(pygame.transform.scale(cut, (35, 60)))
            self.anim.append(self.frames)

    def update(self, action):
        # определяем направление
        move = action[0]
        if move != 0:
            move = -(move // abs(move))

        # прерываем прошлую анимацию, если началась новая
        if self.move != move:
            self.upd = 0
        self.move = move

        if self.upd == 0:
            self.upd += 1
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.anim[move][self.cur_frame]
            return self.image

        self.upd += 1

        if self.upd == 10:  # раз в 10 инетраций меняется кадр
            self.upd = 0

        return self.image


class Particle(pygame.sprite.Sprite):
    # генерируем частицы разного размера
    smoke = [pygame.image.load("data\image\graphics\circle.png")]
    for scale in (10, 12, 14):
        smoke.append(pygame.transform.scale(smoke[0], (scale, scale)))
    del smoke[0]  # удаляем изначально загруженое изображение

    def __init__(self, pos, all_sprites, direction):
        super().__init__(all_sprites)
        self.image = random.choice(self.smoke)
        self.image.set_alpha(10)  # устанавливаем прозрачность
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость
        self.x, self.y = random.choice(range(1, 5)), random.choice([-0.2, -0.1, 0])
        self.rect.x, self.rect.y = pos

        self.direction = -direction // abs(direction)  # направление частиц

        self.time = 0  # для подчёта итераций

    def update(self):
        # перемещаем частицу
        self.rect.x += self.x * self.direction
        self.rect.y += self.y

        self.time += 1

        if self.time == 10:  # удаляем частицу через 10 интераций
            self.kill()