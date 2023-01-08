import pygame

from data import tools
from data import constants as const
from data.components import pacman


class LevelState(tools.State):
    def __init__(self):
        super().__init__()
        self.sprites = pygame.sprite.AbstractGroup()
        self.startup()

    def startup(self):
        self.setup_bg()
        self.setup_pacman()

    def setup_bg(self):
        self.background = pygame.sprite.Sprite
        self.background.image = tools.load_image("level_bg.png")
        self.background.x, self.background.y = 0, 0
        self.background.w, self.background.h = self.background.image.get_size()
        self.background.rect = ((self.background.x, self.background.y), (self.background.w, self.background.h))

    def setup_pacman(self):
        self.pacman = pacman.Pacman(self.sprites)
        self.pacman.rect = ((0, 0), self.pacman.image.get_size())

    def get_event(self, event):
        self.pacman.get_event(event)

    def draw(self, display):
        display.blit(self.background.image, self.background.rect)
        self.sprites.draw(display)

    def update_sprites(self):
        self.pacman.update()

    def update(self, display):
        display.fill(const.BG_COLOR)
        self.update_sprites()
        self.draw(display)
