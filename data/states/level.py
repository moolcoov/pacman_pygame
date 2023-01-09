import pygame

from data import constants as const
from data import tools
from data.components import pacman, grid, point


class LevelState(tools.State):
    def __init__(self):
        super().__init__()
        self.points = pygame.sprite.AbstractGroup()
        self.sprites = pygame.sprite.AbstractGroup()
        self.startup()

    def startup(self):
        self.setup_bg()
        self.setup_pacman()
        self.setup_points()

    def setup_bg(self):
        self.background = pygame.sprite.Sprite
        self.background.image = tools.load_image("level_bg.png")
        self.background.x, self.background.y = 0, 0
        self.background.w, self.background.h = self.background.image.get_size()
        self.background.rect = ((self.background.x, self.background.y), (self.background.w, self.background.h))

    def setup_pacman(self):
        self.pacman = pacman.Pacman(self.sprites)

    def setup_points(self):
        print(grid.cells.items())
        for coords in grid.cells.values():
            if coords[2] == "s" or coords[2] == "b":
                point.Point(coords[2], coords[0], coords[1], self.points)

    def get_event(self, event):
        self.pacman.get_event(event)

    def draw(self, display):
        display.blit(self.background.image, self.background.rect)
        self.sprites.draw(display)
        self.points.draw(display)

    def update_points(self):
        for point_t in self.points.sprites():
            point_t.update()
            if pygame.sprite.collide_rect(self.pacman, point_t):
                print("rr")
                point_t.kill()

    def update_sprites(self):
        self.pacman.update()
        self.update_points()

    def update(self, display):
        display.fill(const.BG_COLOR)
        self.update_sprites()
        self.draw(display)
