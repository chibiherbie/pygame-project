import pygame
from hero import Hero
from level import Level


FPS = 30

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('GAME')

    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)

    running = True

    time = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    level = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    hero = pygame.sprite.Group()
    Hero('data/image/hero/example.png', 100, 100, wall, all_sprites, hero)
    Level('data/maps/map1.txt', level, all_sprites, wall)

    # основной цикл
    while running:
        screen.fill(pygame.Color('white'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # перемещение персонажа
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                hero.update(0, 10)
            if key[pygame.K_UP]:
                hero.update(0, -10)
            if key[pygame.K_RIGHT]:
                hero.update(10, 0)
            if key[pygame.K_LEFT]:
                hero.update(-10, 0)

        all_sprites.draw(screen)  # рисуем всё
        hero.draw(screen)

        time.tick(FPS)

        pygame.display.flip()

    pygame.quit()