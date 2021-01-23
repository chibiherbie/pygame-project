import pygame
import sys
from math import sqrt
from pygame.locals import *


r = [[0.0, 0.0], [0.0, -0.5], [0.0, -1.0], [0.0, -1.5], [0.0, -2.0]]
connect = [[0, 1], [1, 2], [2, 3], [3, 4]]


class Rope:
    def __init__(self):
        self.points = [i + i for i in r]  # делаем дубликаты координат для плавного перемещения
        self.orig_points = [i + i for i in r]

        self.sticks = []  # линии между точками

        self.scale = 50

        for stick in connect:
            self.sticks.append([stick[0], stick[1],
                                self.get_distance(self.points[stick[0]][:2], self.points[stick[1]][:2])])

        # размещаем на позицию
        point = self.points[0]
        point[0] = self.orig_points[0][0] + 300 / self.scale
        point[1] = self.orig_points[0][1] + 100 / self.scale
        point[2] = point[0]
        point[3] = point[1]

    # считаем расстояние между точками
    def get_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)  # находим гипотенузу

    def wind(self, speed):
        print(self.points[-1])
        self.points[-1][0] -= speed


    def upd_sticks(self):
        for stick in self.sticks:
            d = self.get_distance(self.points[stick[0]][:2], self.points[stick[1]][:2])
            mv_ratio = (stick[2] - d) / d / 2  # разница в дистанции

            # положение
            dx = self.points[stick[1]][0] - self.points[stick[0]][0]
            dy = self.points[stick[1]][1] - self.points[stick[0]][1]

            if stick[0] != 0:
                self.points[stick[0]][0] -= dx * mv_ratio * 0.85
                self.points[stick[0]][1] -= dy * mv_ratio * 0.85

            self.points[stick[1]][0] += dx * mv_ratio * 0.85
            self.points[stick[1]][1] += dy * mv_ratio * 0.85

    def update(self):
        for i, point in enumerate(self.points):
            if i != 0:
                d_x = point[0] - point[2]
                d_y = point[1] - point[3]
                point[2] = point[0]
                point[3] = point[1]
                point[0] += d_x
                point[1] += d_y
                point[1] += 0.05  # придаём массу, всгда тянем вниз

    def draw(self, screen, color):
        x_points = [i[0] * self.scale for i in self.points]
        y_points = [i[1] * self.scale for i in self.points]
        min_x, min_y = min(x_points), min(y_points)

        surf = pygame.Surface((300, 300))
        surf.fill((255, 0, 0, 0))

        # рисуем points
        render_points = [[i[0] * self.scale - int(min_x), i[1] * self.scale - int(min_y)] for i in self.points]
        for stick in self.sticks:
            pygame.draw.line(surf, color, render_points[stick[0]], render_points[stick[1]], 5)

        surf = pygame.transform.rotate(surf, 50)
        screen.blit(surf, (min_x, min_y))


pygame.init()
pygame.display.set_caption('ROPE')
screen = pygame.display.set_mode((500, 500), 0, 32)
mainClock = pygame.time.Clock()

rope = Rope()

while True:
    screen.fill((0, 0, 0))

    # process
    rope.update()
    rope.upd_sticks()

    rope.draw(screen, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_f:
                rope.wind(0.1)

    pygame.display.update()
    mainClock.tick(60)


class Ropess:
    def __init__(self, pos):
        self.points = [i + i for i in r]  # делаем дубликаты координат для плавного перемещения
        self.orig_points = [i + i for i in r]

        self.sticks = []  # линии между точками

        self.scale = 15

        # self.x_surf, self.y_surf = pos[0], pos[1]
        # self.w, self.h = self.x_surf + 100, self.x_surf + 100

        for stick in connect:
            self.sticks.append([stick[0], stick[1],
                                self.get_distance(self.points[stick[0]][:2], self.points[stick[1]][:2])])

        self.light = pygame.sprite.Group()
        self.img = LightRope(self.light, self.sticks[-1], 0)

        # размещаем на позицию
        point = self.points[0]
        point[0] = self.orig_points[0][0] + 50 / self.scale
        point[1] = self.orig_points[0][1] + 50 / self.scale
        point[2] = point[0]
        point[3] = point[1]

    # считаем расстояние между точками
    def get_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)  # находим гипотенузу

    def wind(self, speed):
        self.points[-1][0] -= speed

    def upd_sticks(self):
        for stick in self.sticks:
            d = self.get_distance(self.points[stick[0]][:2], self.points[stick[1]][:2])
            mv_ratio = (stick[2] - d) / d / 2  # разница в дистанции

            # положение
            dx = self.points[stick[1]][0] - self.points[stick[0]][0]
            dy = self.points[stick[1]][1] - self.points[stick[0]][1]

            if stick[0] != 0:
                self.points[stick[0]][0] -= dx * mv_ratio * 0.85
                self.points[stick[0]][1] -= dy * mv_ratio * 0.85

            self.points[stick[1]][0] += dx * mv_ratio * 0.85
            self.points[stick[1]][1] += dy * mv_ratio * 0.85

    def update(self):
        for i, point in enumerate(self.points):
            if i != 0:
                d_x = point[0] - point[2]
                d_y = point[1] - point[3]
                point[2] = point[0]
                point[3] = point[1]
                point[0] += d_x
                point[1] += d_y
                point[1] += 0.05  # придаём массу, всгда тянем вниз

    def draw(self, screen, color, dx, dy):
        x_points = [i[0] * self.scale for i in self.points]
        y_points = [i[1] * self.scale for i in self.points]
        min_x, min_y = min(x_points), min(y_points)

        surf = pygame.Surface((100, 100))
        surf.set_colorkey((0, 0, 0))

        # рисуем points
        render_points = [[i[0] * self.scale - int(min_x), i[1] * self.scale - int(min_y)] for i in self.points]
        for stick in self.sticks:
            pygame.draw.line(surf, color, render_points[stick[0]], render_points[stick[1]], 4)

        # self.light.update(render_points[self.sticks[-1][1]][0], render_points[self.sticks[-1][1]][1])
        # self.light.draw(surf)

        pygame.draw.circle(surf, (255, 0, 0), (0, 0), 30)
        pygame.draw.circle(surf, (255, 0, 0), (100, 100), 30)

        screen.blit(surf, (min_x, min_y))
