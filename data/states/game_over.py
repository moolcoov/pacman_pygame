import pygame

from data import constants as const
from data import tools


class GameOverState(tools.State):
    def __init__(self, start_time, props):
        super().__init__()
        self.props = props
        self.start_time = start_time
        self.sprites = pygame.sprite.AbstractGroup()
        self.startup()

    def startup(self):
        pygame.mouse.set_visible(True)
        self.setup_title()
        self.setup_buttons()

    def setup_title(self):
        self.title = pygame.sprite.Sprite()
        self.title.image = tools.load_image("go_title.png")
        self.title.rect = (((const.SCREEN_SIZE[0] // 2) - self.title.image.get_size()[0] // 2, 184),
                           self.title.image.get_size())
        self.title.add(self.sprites)

    def setup_buttons(self):
        self.setup_button_restart()
        self.setup_button_quit()

    def setup_button_restart(self):
        self.button_res = pygame.sprite.Sprite()
        self.button_res.image = tools.load_image("btn_restart.png")

        self.button_res.w, self.button_res.h = self.button_res.image.get_size()
        self.button_res.x, self.button_res.y = const.SCREEN_CENTER - self.button_res.w // 2, 250

        self.button_res.rect = ((self.button_res.x, self.button_res.y),
                                (self.button_res.w, self.button_res.h))
        self.button_res.add(self.sprites)

    def setup_button_quit(self):
        self.button_quit = pygame.sprite.Sprite()
        self.button_quit.image = tools.load_image("btn_quit.png")

        self.button_quit.w, self.button_quit.h = self.button_quit.image.get_size()
        self.button_quit.x, self.button_quit.y = const.SCREEN_CENTER - self.button_quit.w // 2, 285

        self.button_quit.rect = ((self.button_quit.x, self.button_quit.y),
                                 (self.button_quit.w, self.button_quit.h))
        self.button_quit.add(self.sprites)

    def get_event(self, event):
        if all([self.button_res.x <= pygame.mouse.get_pos()[0] <= self.button_res.x + self.button_res.w,
                self.button_res.y <= pygame.mouse.get_pos()[1] <= self.button_res.y + self.button_res.h]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_visible(False)
                self.next = const.LEVEL
                self.done = True
        elif all([self.button_quit.x <= pygame.mouse.get_pos()[0] <= self.button_quit.x + self.button_quit.w,
                  self.button_quit.y <= pygame.mouse.get_pos()[1] <= self.button_quit.y + self.button_quit.h]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self, display, current_time):
        self.current_time = current_time
        display.fill(const.BG_COLOR)
        self.sprites.draw(display)
