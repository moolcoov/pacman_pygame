import pygame
from data import tools
from data import constants as const


class MainMenuState(tools.State):
    def __init__(self):
        super().__init__()

        self.sprites = pygame.sprite.AbstractGroup()
        self.color = "#2D2D2D"

        self.startup()

    def startup(self):
        pygame.mouse.set_visible(True)
        self.setup_title()
        self.setup_buttons()

    def setup_title(self):
        self.title = pygame.sprite.Sprite()
        self.title.image = tools.load_image("main_title.png")
        self.title.rect = (((const.SCREEN_SIZE[0] // 2) - self.title.image.get_size()[0] // 2, 150),
                           self.title.image.get_size())
        self.title.add(self.sprites)

    def setup_buttons(self):
        self.setup_button_play()
        self.setup_button_quit()

    def setup_button_play(self):
        self.button_play = pygame.sprite.Sprite()
        self.button_play.image = tools.load_image("btn_play.png")

        self.button_play.w, self.button_play.h = self.button_play.image.get_size()
        self.button_play.x, self.button_play.y = const.SCREEN_CENTER - self.button_play.w // 2, 255

        self.button_play.rect = ((self.button_play.x, self.button_play.y),
                                 (self.button_play.w, self.button_play.h))
        self.button_play.add(self.sprites)

    def setup_button_quit(self):
        self.button_quit = pygame.sprite.Sprite()
        self.button_quit.image = tools.load_image("btn_quit.png")

        self.button_quit.w, self.button_quit.h = self.button_quit.image.get_size()
        self.button_quit.x, self.button_quit.y = const.SCREEN_CENTER - self.button_quit.w // 2, 290

        self.button_quit.rect = ((self.button_quit.x, self.button_quit.y),
                                 (self.button_quit.w, self.button_quit.h))
        self.button_quit.add(self.sprites)

    def get_event(self, event):

        if all([self.button_play.x <= pygame.mouse.get_pos()[0] <= self.button_play.x + self.button_play.w,
                self.button_play.y <= pygame.mouse.get_pos()[1] <= self.button_play.y + self.button_play.h]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONUP:
                print("play")
        elif all([self.button_quit.x <= pygame.mouse.get_pos()[0] <= self.button_quit.x + self.button_quit.w,
                  self.button_quit.y <= pygame.mouse.get_pos()[1] <= self.button_quit.y + self.button_quit.h]):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONUP:
                self.quit = True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self, display):
        display.fill(self.color)
        self.sprites.draw(display)
