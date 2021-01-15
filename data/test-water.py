# F=−kx
# A = ma
# a=-k/m x-dv

import pygame
import random
import math as m
from pygame import *


class SurfaceWater:
    k = 0.025  # spring constant
    d = 0.025  # damping constant

    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.max_y = y
        self.velocity = 0

    def update(self):
        x = self.y_pos - self.max_y  # смещение пружины от начала
        a = -self.k * x  # ускорение

        self.y_pos += self.velocity
        self.velocity += a


class Water:
    def __init__(self, x_s, y_s, x_e, y_e, spring_segment):
        self.springs = []
        self.x_s = x_s
        self.y_s = y_s
        self.x_e = x_e
        self.y_e = y_e

        self.passes = 10
        self.spread = 0.05  # скорость распространения волн

        for i in range(abs(x_e - x_s) // spring_segment):
            self.springs.append(SurfaceWater(i * spring_segment + x_s, y_e))
        self.springs.append(SurfaceWater(x_e, y_e))

    def update(self):
        for i in self.springs:
            i.update()

        left_d = [0.0] * len(self.springs)
        right_d = [0.0] * len(self.springs)

        for i in range(self.passes):
            for num in range(len(self.springs) - 1):
                if num > 0:
                    left_d[num] = self.spread * (self.springs[i].y_pos - self.springs[num - 1].y_pos)
                    self.springs[num - 1].velocity += left_d[num]
                if num < len(self.springs) - 1:
                    right_d[num] = self.spread * (self.springs[i].y_pos - self.springs[num + 1].y_pos)
                    self.springs[num + 1].velocity += right_d[num]
            for num in range(len(self.springs) - 1):
                if i > 0:
                    self.springs[num - 1].y_pos += left_d[num]  # you were updating velocity here!
                if i < len(self.springs) - 1:
                    self.springs[num + 1].y_pos += right_d[num]

    def draw(self):
        for i in range(len(self.springs) - 1):
            pygame.draw.line(screen, (0, 0, 255), (self.springs[i].x_pos, self.springs[i].y_pos),
                             (self.springs[i + 1].x_pos, self.springs[i + 1].y_pos), 2)

    def force(self, place, speed):
        self.springs[place].velocity = speed


if __name__ == '__main__':
    pygame.init()
    size = w, h = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    k = 0.025  # adjust this value to your liking
    x = 250  # естественное положение верхней части пружины
    d = 0.025  # коэф увлажнения

    water = Water(0, 150, w, 150, 3)

    run = True
    while run:
        screen.fill((255, 255, 255))
        water.draw()
        water.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                water.force(50, 100)

        pygame.display.flip()

pygame.quit()