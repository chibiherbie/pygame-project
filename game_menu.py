import pygame
import pygame_gui


class GameMenu:
    def __init__(self, screen, size, fps):
        self.screen = screen
        self.size = size
        self.fps = fps

        self.manager = pygame_gui.UIManager(self.size)
        self.resume = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text='RESUME',
            manager=self.manager,
        )


    def update_manager(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.resume:
                    print('RESUME')
                    return True
        self.manager.process_events(event)

    def draw(self):
        self.manager.update(time_delta=60)
        self.manager.draw_ui(self.screen)




