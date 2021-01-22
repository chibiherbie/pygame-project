import pygame
import sys
from math import sqrt
from pygame.locals import *


r = [[0.0, 0.0], [0.0, -1.0], [0.0, -2.0], [0.0, -3.0], [0.0, -5.0]]
conect = [[0, 1], [1, 2], [2, 3], [3, 4]]


class Rope:
    def __init__(self):
        self.points = [i + i for i in r]  # делаем дубликаты координат для плавного перемещения
        self.orig_points = [i + i for i in r]

        self.sticks = []  # линии между точками

        self.scale = 50

        for stick in conect:
            self.sticks.append([stick[0], stick[1],
                                self.get_distance(self.points[stick[0]][:2], self.points[stick[1]][:2])])

        # размещаем на позиции
        point = self.points[0]
        point[0] = self.orig_points[0][0] + 100 / self.scale
        point[1] = self.orig_points[0][1] + 100 / self.scale
        point[2] = point[0]
        point[3] = point[1]

    # считаем расстояние между точками
    def get_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)  # находим гипотенузу

    def add_stick(self, p):
        pass

    def update(self):
        pass

    def draw(self, screen, color):
        x_points = [i[0] * self.scale for i in self.points]
        y_points = [i[1] * self.scale for i in self.points]
        min_x, min_y = min(x_points), min(y_points)

        surf = pygame.Surface(screen.get_size())
        surf.set_colorkey((0, 0, 0))

        # render points
        render_points = [[i[0] * self.scale - int(min_x), i[1] * self.scale - int(min_y)] for i in self.points]
        for stick in self.sticks:
            pygame.draw.line(surf, (255, 255, 255), render_points[stick[0]], render_points[stick[1]], 5)

        screen.blit(surf, (100, 100))


pygame.init()
pygame.display.set_caption('ROPE')
screen = pygame.display.set_mode((500, 500), 0, 32)
mainClock = pygame.time.Clock()

rope = Rope()

while True:
    screen.fill((0, 0, 0))

    rope.draw(screen, (255, 255, 255))

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
