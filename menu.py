import sys
import pygame
from game import WIDTH, HEIGHT, start_game
from pygame.locals import *


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Ангкар')
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

font = pygame.font.SysFont(None, 20)

click = False


def main_menu():
    while True:
        font4 = pygame.font.Font(None, 70)
        screen.fill((250, 250, 250))
        font = pygame.font.Font(None, 25)
        draw_text('Ангкар', font4, (0, 0, 0), screen, 160, 200)
        draw_text('Начать игру', font, (0, 0, 0), screen, 200, 280)
        draw_text('Настройки', font, (0, 0, 0), screen, 200, 480)
        draw_text('Продолжить', font, (0, 0, 0), screen, 130, 380)
        draw_text('Найти лобби', font, (0, 0, 0), screen, 250, 380)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(120, 300, 250, 50)
        button_2 = pygame.Rect(120, 500, 250, 50)
        button_3 = pygame.Rect(120, 400, 125, 50)
        button_4 = pygame.Rect(250, 400, 120, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                start_game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                saved_games()
        if button_4.collidepoint((mx, my)):
            if click:
                lobby()
        pygame.draw.rect(screen, (120, 120, 120), button_1)
        pygame.draw.rect(screen, (120, 120, 120), button_2)
        pygame.draw.rect(screen, (120, 120, 120), button_3)
        pygame.draw.rect(screen, (120, 120, 120), button_4)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                pass
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def options():
    font4 = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 40)
    running = True
    while running:
        screen.fill((200, 200, 200))
        draw_text('Общая громкость', font, (0, 0, 0), screen, 20, 100)
        draw_text('Громкость музыки', font, (0, 0, 0), screen, 20, 140)
        draw_text('Настройки', font4, (0, 0, 0), screen, 200, 20)
        button_10 = pygame.Rect(250, 800, 120, 50)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def lobby():
    font4 = pygame.font.Font(None, 70)
    running = True
    while running:
        screen.fill((200, 200, 200))
        draw_text('Лобби', font4, (0, 0, 0), screen, 180, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def saved_games():
    font4 = pygame.font.Font(None, 70)
    running = True
    while running:
        screen.fill((200, 200, 200))
        draw_text('Сохранённые игры', font4, (0, 0, 0), screen, 180, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


if __name__ == '__main__':
    main_menu()