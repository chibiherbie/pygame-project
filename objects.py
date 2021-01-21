import pygame
import random


def upd_player_water(player, waters, all_sprites):
    # касание с водой
    for water in waters:
        if water.upd:
            if water.rect.x < player.rect.midbottom[0] < water.rect.x + water.w and \
                    water.rect.y < player.rect.midbottom[1] < water.rect.y + water.h + 2:
                water.force(abs(player.rect.midbottom[0] - water.rect.x) // water.spring_segment, player.yvel)
                if not player.isWater and water.type != 'swamp':
                    player.sound_water_drop.play()
                    create_particles(player.rect.midbottom, 'water', all_sprites)
                player.isWater = True

                if water.type == 'swamp':
                    if player.stop_death == 0:
                        water.sound_drop.play()
                    player.rect.y += 1.5
                    player.death_anim('swamp')
            else:
                if player.isWater and water.type != 'swamp':
                    player.sound_water_nodrop.play()
                    create_particles(player.rect.midbottom, 'water', all_sprites)
                player.isWater = False


def create_particles(position, type, all_sprites):
    particle_count = 20  # количество создаваемых частиц
    for _ in range(particle_count):
        ParticleWater(position, all_sprites, type)


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

        self.sound_lever = [pygame.mixer.Sound('data/sound/sound_lever_on.mp3'),
                            pygame.mixer.Sound('data/sound/sound_lever_off.mp3')]
        for i in self.sound_lever:
            i.set_volume(0.1)

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
            self.sound_lever[1].play()
        else:
            self.image = self.frames[0]
            self.close = True
            self.sound_lever[0].play()
        # if self.upd % 4 == 0:  # раз в 4 инетраций меняется кадр
        #     self.upd += 1
        #     self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        #     self.image = self.frames[self.cur_frame]
        #
        # self.upd += 1


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, num, *group):
        super().__init__(*group)
        self.image = pygame.image.load('data/image/graphics/door.png').convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * pos_x + tile_width // 2 - self.image.get_rect().w // 2,
                                               tile_height * pos_y)
        self.y = self.rect.y
        self.upd, self.count = 0, 0
        self.value = num

        self.stat = True

        self.sound_door = pygame.mixer.Sound('data/sound/sound_door.mp3')
        self.sound_door.set_volume(0.5)

    def update(self):
        if self.upd == 1:
            self.stat = False
            if self.count == 0:
                self.sound_door.play()
            self.rect.y += self.upd
            self.count += self.upd

            if self.count == self.rect.h:  # если достигнут предел, то останавливаем
                self.upd = 0
                self.sound_door.stop()
        elif self.upd == -1:
            if self.count == self.rect.h:
                self.sound_door.play()
            self.rect.y += self.upd
            self.count += self.upd
            if self.count == 0:
                self.upd = 0
                self.sound_door.stop()
                self.stat = True


class Spikes(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, *group):
        super().__init__(*group)

        self.image = pygame.image.load('data/image/graphics/spikes.png').convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * pos_x + tile_width // 2 - self.image.get_rect().w // 2,
                                               tile_height * pos_y)
        self.rect[1] += 10


class SavePoint(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, *group):
        super().__init__(*group)

        self.image = pygame.image.load('data/image/graphics/save_point.png').convert_alpha()
        self.rect = self.image.get_rect().move(tile_width * pos_x + tile_width // 2 - self.image.get_rect().w // 2,
                                               tile_height * pos_y)

        self.pos_player = [tile_width * pos_x + 100, tile_width * pos_x + 150, tile_height * pos_y - 10]
        self.active = False


class Spring:
    k = 0.02  # коэф пружины
    d = 0.025  # коэф "влажности"

    def __init__(self, x, y, type):
        if type == 'swamp':
            self.d = 0.03  # коэф "влажности"
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
    def __init__(self, x_s, y_s, x_e, y_e, spring_segment, all_sprite, type):
        self.springs = []
        self.x_s = x_s
        self.y_s = y_s
        self.x_e = x_e
        self.y_e = y_e
        self.spring_segment = spring_segment
        self.upd = False
        self.type = type

        if type == 'water':
            self.color = pygame.Color(0, 0, 255)
            self.passes = 20
            self.spread = 0.06  # скорость распространения волн
            self.alpha = 100
        else:
            self.color = pygame.Color(79,131,57)
            self.spread = 0.09
            self.passes = 10
            self.sound_drop = pygame.mixer.Sound('data/sound/sound_swamp_drop.mp3')
            self.sound_drop.set_volume(0.1)
            self.alpha = 175

        self.all_sprites = all_sprite

        self.w, self.h = self.x_e - self.x_s, self.y_e - self.y_s

        self.rect = pygame.Rect(self.x_s, self.y_s, self.x_e, self.y_e)

        # print(x_s, y_s, x_e, y_e)
        # print('SURFACE:', (self.x_e - self.x_s, self.y_e - self.y_s))
        # print(self.rect)

        # self.passes = 20
        # self.spread = 0.06  # скорость распространения волн

        # даём позицию нашим пружинам
        for i in range(abs(self.rect[2] - self.rect[0]) // self.spring_segment):
            self.springs.append(Spring(i * self.spring_segment, 20, type))
        self.springs.append(Spring(self.x_e - self.x_s, 20, type))

    def update(self):
        for i in self.springs:
            i.update()
        left_d = [0.0] * len(self.springs)
        right_d = [0.0] * len(self.springs)
        if self.upd:
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
        sur = pygame.Surface((self.x_e - self.x_s, self.y_e - self.y_s)).convert_alpha()  # self.x_e - self.x_s, self.y_e - self.y_s
        sur.fill((0, 0, 0, 0))
        sur.set_alpha(self.alpha)
        for i in range(len(self.springs) - 1):
            pygame.draw.polygon(sur, self.color, [(self.springs[i].x_pos, self.springs[i].y_pos),
                                                   (self.springs[i + 1].x_pos, self.springs[i + 1].y_pos),
                                                   (self.springs[i].x_pos, self.y_e)])
            pygame.draw.polygon(sur, self.color, [(self.springs[i + 1].x_pos, self.springs[i + 1].y_pos),
                                                   (self.springs[i + 1].x_pos, self.y_e),
                                                   (self.springs[i].x_pos, self.y_e)])
        return sur

    def force(self, place, speed):
        self.springs[place].velocity = speed

    def upd_camera(self, dx, dy, w, h, screen):
        self.rect[0] += dx
        self.rect[1] += dy
        # не рисуется за границами экрана
        if -self.w <= self.rect.x <= w and -self.h <= self.rect.y <= h:
            screen.blit(self.draw(), (self.rect[0], self.rect[1]))
            self.upd = True
        else:
            self.upd = False
        self.update()


class ParticleWater(pygame.sprite.Sprite):
    # генерируем частицы разного размера
    water = [pygame.image.load("data\image\graphics\circle_water.png")]
    for scale in (10, 12, 14):
        water.append(pygame.transform.scale(water[0], (scale, scale)))
    del water[0]  # удаляем изначально загруженое изображение

    def __init__(self, pos, all_sprites, type):
        super().__init__(all_sprites)
        if type == 'water':
            self.image = random.choice(self.water).convert_alpha()
        else:
            pass
        self.rect = self.image.get_rect()
        self.image.set_alpha(50)

        # у каждой частицы своя скорость - это вектор
        self.velocity = [random.choice(range(-5, 6)), random.choice(range(-5, 6))]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = 0.4
        self.time = 0

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        self.time += 1

        if self.time == 15:  # удаляем частицу через 10 интераций
            self.kill()


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_width, tile_height, num, screen, *group):
        super().__init__(*group)

        self.frames = []

        self.cut_sheet('data/image/graphics/button.png', 1, 1)

        self.cur_frame = 0
        self.upd = 0
        self.screen = screen

        self.image = self.frames[self.cur_frame]
        self.rect.w += 50
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

        self.close = True
        self.value = num  # индес рычага, для открытия определённой двери

        self.sound_lever = [pygame.mixer.Sound('data/sound/sound_lever_on.mp3'),
                            pygame.mixer.Sound('data/sound/sound_lever_off.mp3')]
        for i in self.sound_lever:
            i.set_volume(0.1)

    # режим заготовку на кадры
    def cut_sheet(self, sheet, columns, rows):
        sheet = pygame.image.load(sheet).convert_alpha()  # загружаем файл

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                cut = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))  # размер изображения
                cut = pygame.transform.scale(cut, (100, 100))
                self.frames.append(cut)

    def update(self):
        if not self.close:
            s = pygame.Surface(self.screen.get_size()).convert_alpha()
            s.fill((0, 0, 0, 0))
            s.set_alpha(255)
            
            # рисуем свет от лампы
            pygame.draw.circle(s, pygame.Color(255, 207, 72, 50), (self.rect.x + 70, self.rect.y + 65), 60)
            pygame.draw.circle(s, pygame.Color(255, 180, 72, 80),
                               (self.rect.x + 70, self.rect.y + 65), random.randrange(29, 31))
            pygame.draw.circle(s, pygame.Color(255, 130, 72, 80),
                               (self.rect.x + 70, self.rect.y + 65), random.randrange(17, 19))

            self.screen.blit(s, (0, 0))
        self.close = True


