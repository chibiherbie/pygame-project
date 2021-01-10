import pygame
import pygame_gui


class GameMenu:
    def __init__(self, screen, size, fps):
        self.screen = screen
        self.size = size
        self.fps = fps
        w, h = size

        self.settings_show = False

        self.manager = pygame_gui.UIManager(self.size)

        # меню
        self.text_menu = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3 - 75), (150, 50)),
            text='МЕНЮ',
            manager=self.manager,
        )
        self.resume = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3), (150, 50)),
            text='ПРОДОЛЖИТЬ',
            manager=self.manager,
        )
        self.settings = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3 + 50 // 2 * 2), (150, 50)),
            text='НАСТРОЙКИ',
            manager=self.manager,
        )
        self.exit_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3 + 50 // 2 * 4), (150, 50)),
            text='ВЫЙТИ В МЕНЮ',
            manager=self.manager,
        )
        self.exit_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3 + 50 // 2 * 6), (150, 50)),
            text='ВЫЙТИ ИЗ ИГРЫ',
            manager=self.manager,
        )

        # настройки
        self.settings_text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3 - 75), (150, 50)),
            text='НАСТРОЙКИ',
            manager=self.manager,
        )
        self.music = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3), (150, 50)),
            text='ЗВУК',
            manager=self.manager,
        )
        self.back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((w // 2 - 150 // 2, h // 3 + 50 // 2 * 2), (150, 50)),
            text='<- НАЗАД',
            manager=self.manager,
        )

    def update_manager(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.resume:
                    return 'res'
                elif event.ui_element == self.exit_game:
                    return 'exit'
                elif event.ui_element == self.settings:
                    self.settings_show = True
                elif event.ui_element == self.exit_menu:
                    return 'menu'
                elif event.ui_element == self.back:
                    self.settings_show = False
                elif event.ui_element == self.music:
                    print('МУЗЫКА')

        self.manager.process_events(event)

    def draw(self):
        # показываыем нужные кнопки
        if not self.settings_show:
            self.menu_visibility(True)
        else:
            self.menu_visibility(False)

        self.manager.update(time_delta=60)
        self.manager.draw_ui(self.screen)

    def menu_visibility(self, visibility):
        if visibility:
            self.text_menu.show()
            self.exit_menu.show()
            self.resume.show()
            self.settings.show()
            self.exit_game.show()
            self.music.hide()
            self.back.hide()
            self.settings_text.hide()
        else:
            self.text_menu.hide()
            self.exit_menu.hide()
            self.resume.hide()
            self.settings.hide()
            self.exit_game.hide()
            self.music.show()
            self.back.show()
            self.settings_text.show()


