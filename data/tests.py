import os
import random

import pygame

pygame.init()
fps = 50
gravity = 0.25

clock = pygame.time.Clock()
screen = pygame.display.set_mode((400, 300))


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


WIDTH = 400
HEIGHT = 300

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# для отслеживания улетевших частиц
# удобно использовать пересечение прямоугольников
screen_rect = (0, 0, WIDTH, HEIGHT)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [pygame.image.load("D:\Program Files (x86)\проект игра pygame\pygame-project\data\image\graphics\circle.png")]
    for scale in (10, 15):
        print(scale)
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))
    del fire[0]

    def __init__(self, pos, direction):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.x, self.y = random.choice(range(1, 5)), random.choice([-0.2, -0.1, 0])
        # и свои координаты
        self.rect.x, self.rect.y = pos
        self.posx = pos[0]
        self.direction = direction // abs(direction)

        # гравитация будет одинаковой
        self.gravity = gravity
        self.time = 0

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        # перемещаем частицу
        self.rect.x += self.x * self.direction
        self.rect.y += self.y
        if self.rect.x - self.posx < 20:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(0)
        self.time += 1
        # убиваем, если частица ушла за экран
        if self.time == 10:
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 50
    # возможные скорости
    numbers = 0
    for _ in range(particle_count):
        if numbers == 0:
            Particle(position, -5)
            numbers += 1
            continue
        numbers = 0 if numbers == 3 else numbers + 1


all_sprites = pygame.sprite.Group()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # создаем частицы по щелчку мыши
            create_particles(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
