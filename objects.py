import pygame


class Lever(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, num, *group):
        super().__init__(*group)

        self.frames = []

        self.cut_sheet('data/image/graphics/lever_anim.png', 5, 1)

        self.cur_frame = 0
        self.upd = 0

        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

        self.close = True
        self.value = num  # индес рычага, для открытия определённой двери

    # режим заготовку на кадры
    def cut_sheet(self, sheet, columns, rows):
        sheet = pygame.image.load(sheet).convert_alpha()  # загружаем файл

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                cut = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))  # размер изображения
                self.frames.append(cut)

    def animation(self):
        if self.close:
            self.image = self.frames[-1]
            self.close = False
        else:
            self.image = self.frames[0]
            self.close = True
        # if self.upd % 4 == 0:  # раз в 4 инетраций меняется кадр
        #     self.upd += 1
        #     self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        #     self.image = self.frames[self.cur_frame]
        #
        # self.upd += 1


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, num, *group):
        super().__init__(*group)

        self.frames = []

        self.image = pygame.image.load('data/image/graphics/door2.png')
        self.rect = self.image.get_rect().move(tile_width * pos_x + tile_width // 2 - self.image.get_rect().w // 2,
                                               tile_height * pos_y)
        self.y = self.rect.y
        self.upd = 0
        self.speed = 1
        self.value = num
        print(self.y, self.y - self.rect.h)

    def update(self):
        if self.upd == 1:
            self.rect.y += self.upd
            if self.rect.y == self.y:
                self.upd = 0
        elif self.upd == -1:
            self.rect.y += self.upd
            if self.rect.y == self.y - self.rect.h:
                self.upd = 0
