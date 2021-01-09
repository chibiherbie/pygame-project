import pygame


def check_objects():
    pass


class Lever(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, *group):
        super().__init__(*group)

        self.frames = []

        self.cut_sheet('data/image/graphics/lever_anim.png', 5, 1)

        self.cur_frame = 0
        self.upd = 0

        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

        self.side_l = True
        self.value = 0  # индес рычага, для открытия определённой двери

    # режим заготовку на кадры
    def cut_sheet(self, sheet, columns, rows):
        sheet = pygame.image.load(sheet).convert_alpha()  # загружаем файл

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                cut = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))  # размер изображения
                self.frames.append(cut)

    def anim(self):
        pass