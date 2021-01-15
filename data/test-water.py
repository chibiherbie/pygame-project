# F=−kx
# A = ma
# a=-k/m x-dv

import pygame
from pygame import *


class Spring:
    k = 0.02  # коэф пружины
    d = 0.025  # коэф "влажности"

    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.max_y = y  # естественное положение верхней части пружины
        self.velocity = 0

    def update(self):
        x = self.y_pos - self.max_y  # смещение пружины от начала

        a = -self.k * x - self.d * self.velocity  # ускорение

        self.y_pos += self.velocity
        self.velocity += a


class Water:
    def __init__(self, x_s, y_s, x_e, y_e, spring_segment):
        self.springs = []
        self.x_s = x_s
        self.y_s = y_s
        self.x_e = x_e
        self.y_e = y_e

        self.passes = 20
        self.spread = 0.06  # скорость распространения волн

        for i in range(abs(x_e - x_s) // spring_segment):
            self.springs.append(Spring(i * spring_segment + x_s, y_e))
        self.springs.append(Spring(x_e, y_e))

    def update(self):
        for i in self.springs:
            i.update()

        left_d = [0.0] * len(self.springs)
        right_d = [0.0] * len(self.springs)

        for _ in range(self.passes):
            for num in range(len(self.springs) - 1):
                if num > 0:
                    left_d[num] = self.spread * (self.springs[num].y_pos - self.springs[num - 1].y_pos)
                    self.springs[num - 1].velocity += left_d[num]
                if num < len(self.springs) - 1:
                    right_d[num] = self.spread * (self.springs[num].y_pos - self.springs[num + 1].y_pos)
                    self.springs[num + 1].velocity += right_d[num]

            # обновляем скорость
            for num in range(len(self.springs) - 1):
                if num > 0:
                    self.springs[num - 1].y_pos += left_d[num]
                if num < len(self.springs) - 1:
                    self.springs[num + 1].y_pos += right_d[num]

    def draw(self):
        sur = pygame.Surface(size).convert_alpha()
        sur.fill((0, 255, 255))
        sur.set_alpha(50)
        for i in range(len(self.springs) - 1):
            pygame.draw.polygon(sur, (0, 0, 255), [(self.springs[i].x_pos, self.springs[i].y_pos),
                                                   (self.springs[i + 1].x_pos, self.springs[i + 1].y_pos),
                                                   (self.springs[i].x_pos, h)])
            pygame.draw.polygon(sur, (0, 0, 255), [(self.springs[i + 1].x_pos, self.springs[i + 1].y_pos),
                                                   (self.springs[i + 1].x_pos, h),
                                                   (self.springs[i].x_pos, h)])
        screen.blit(sur, (0, 0))

    def force(self, place, speed):
        self.springs[place].velocity = speed


if __name__ == '__main__':
    pygame.init()
    size = w, h = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    water = Water(0, 100, w, 300, 5)

    run = True
    while run:
        screen.fill((255, 255, 255))
        water.draw()
        water.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                water.force(30, 100)

        pygame.display.flip()

pygame.quit()