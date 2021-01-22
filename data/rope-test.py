import pygame
import sys
from pygame.locals import *


r = [[0.0, 0.0], [0.0, -1.0], [0.0, -2.0], [0.0, -3.0], [0.0, -5.0]]
c = [[0, 1], [1, 2], [2, 3], [3, 4]]


class Rope:
    def __init__(self):
        self.points = [i + i for i in r]  # dupe position for last position
        self.orig_points = [i + i for i in r]
        self.sticks = []
        self.scale = 50
        for stick in c:
            self.add_stick(stick)
        # self.grounded = 0

    def add_stick(self, p):
        pass

    def update(self):
        pass


pygame.init()
pygame.display.set_caption('cloth?')
screen = pygame.display.set_mode((500, 500), 0, 32)
mainClock = pygame.time.Clock()

my_cloth = Rope()

while True:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    mainClock.tick(60)
