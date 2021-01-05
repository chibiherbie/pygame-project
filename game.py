import pygame
from hero import Hero
from level import Level


FPS = 60

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('GAME')

    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)

    running = True

    # перемещение
    x = 0
    y = 0

    time = pygame.time.Clock()

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    level = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    hero = pygame.sprite.Group()

    player = Hero('data/image/hero/example.png', 100, 400, wall, all_sprites, hero)
    Level('data/maps/map1.txt', level, all_sprites, wall)

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
            y = 1
        if key[pygame.K_RIGHT]:
            x = 5
        if key[pygame.K_LEFT]:
            x = -5

        hero.update(x, y)
        x, y = 0, 0

        all_sprites.draw(screen)  # рисуем всё
        hero.draw(screen)

        time.tick(FPS)

        pygame.display.flip()

    pygame.quit()