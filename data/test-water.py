# F=−kx

import pygame, random
import math as m
from pygame import *

pygame.init()

WINDOW_SIZE = (854, 480)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


if __name__ == '__main__':
    pygame.init()
    size = w, h = 1000, 1000
    screen = pygame.display.set_mode(size)

    run = True
    while run:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                pass

        pygame.display.flip()

pygame.quit()