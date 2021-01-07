import pygame
from hero import Hero
from level import Level


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = player.rect.x
        self.dy = player.rect.y

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj, layer):
        # рисуем в зависимоти от плана
        if layer == 0:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        elif layer == -2:
            obj.rect.x += self.dx * 0.6
            # obj.rect.y += self.dy * 0.6
        elif layer == -1:
            obj.rect.x += self.dx * 0.8
            obj.rect.y += self.dy * 0.001
        else:
            obj.rect.x += self.dx * 0.4
            obj.rect.y += self.dy * 0.4

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2) // 40
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2) // 40


FPS = 60

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('GAME')

    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)

    running = True

    # перемещение
    p_x = 0
    p_y = 0

    time = pygame.time.Clock()

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    level = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    hero = pygame.sprite.Group()
    background = pygame.sprite.Group()
    layer_2 = pygame.sprite.Group()
    layer_1 = pygame.sprite.Group()

    player = Hero('data/image/hero', 100, 400, wall, all_sprites, hero)
    Level('data/maps/map1.txt', level, all_sprites, wall, background, layer_2, layer_1)
    camera = Camera()

    # основной цикл
    while running:
        screen.fill(pygame.Color('white'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # перемещение персонажа
        key = pygame.key.get_pressed()
        # if key[pygame.K_DOWN]:
        #     hero.update(0, 1)
        if key[pygame.K_UP]:
            p_y = 1
        if key[pygame.K_RIGHT]:
            p_x = 5
        if key[pygame.K_LEFT]:
            p_x = -5

        player.move(p_x, p_y)
        p_x, p_y = 0, 0

        # двигаем объекты за персонажем
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite, 0)

        for sprite in layer_2:
            camera.apply(sprite, -2)

        for sprite in layer_1:
            camera.apply(sprite, -1)

        camera.apply(background.sprites()[0], -3)

        background.draw(screen)
        layer_2.draw(screen)
        layer_1.draw(screen)
        all_sprites.draw(screen)  # рисуем всё

        hero.draw(screen)

        time.tick(FPS)
        pygame.display.flip()
        # pygame.display.update(pygame.rect.Rect(0, 0, 100, 100))

    pygame.quit()