# F=−kx
# A = ma
# a=-k/m x-dv

import pygame
import random
import math as m
from pygame import *


class SurfaceWater:
    k = 0.04  # spring constant
    d = 0.08  # damping constant

    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.target_y = y
        self.velocity = 0


class Water:
    def __init__(self, x_s, y_s, x_e, y_e, spring_segment):
        self.springs = []
        self.x_s = x_s
        self.y_s = y_s
        self.x_e = x_e
        self.y_e = y_e

        for i in range(abs(x_e - x_s) // spring_segment):
            self.springs.append(SurfaceWater(i * spring_segment + x_s, y_e))
        self.springs.append(SurfaceWater(x_e, y_e))

    def update(self):
        left_d = []
        right_d = []

    def draw(self):
        for i in range(len(self.springs) - 1):
            pygame.draw.line(screen, (0, 0, 255), (self.springs[i].x_pos, self.springs[i].y_pos),
                             (self.springs[i + 1].x_pos, self.springs[i + 1].y_pos), 2)


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
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                pass

        pygame.display.flip()

pygame.quit()