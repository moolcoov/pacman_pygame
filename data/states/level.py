import pygame

from data import constants as const
from data import tools
from data.components import pacman, grid, point


class LevelState(tools.State):
    def __init__(self):
        super().__init__()
        self.props = None
        self.points = pygame.sprite.AbstractGroup()
        self.sprites = pygame.sprite.AbstractGroup()
        self.startup()

    def startup(self):
        self.setup_props()
        self.setup_bg()
        self.setup_score()
        self.setup_pacman()
        self.setup_points()

    def setup_props(self):
        if not self.props:
            self.props = {
                const.LEVEL: "1",
                const.SCORE: "0",
                const.TOTAL_SCORE: "0"
            }

    def setup_bg(self):
        self.background = pygame.sprite.Sprite
        self.background.image = tools.load_image("level_bg.png")
        self.background.x, self.background.y = 0, 0
        self.background.w, self.background.h = self.background.image.get_size()
        self.background.rect = ((self.background.x, self.background.y), (self.background.w, self.background.h))

    def setup_score(self):
        self.font = pygame.font.Font("./resources/fonts/pixel.ttf", 18)
        self.level = self.font.render("LEVEL", True, const.WHITE_COLOR)
        self.level_score = self.font.render("0", True, const.WHITE_COLOR)
        self.total = self.font.render("TOTAL", True, const.WHITE_COLOR)
        self.total_score = self.font.render("0", True, const.WHITE_COLOR)

    def setup_pacman(self):
        self.pacman = pacman.Pacman(self.sprites)

    def setup_points(self):
        for coords in grid.cells.values():
            if coords[2] == "s" or coords[2] == "b":
                point.Point(coords[2], coords[0], coords[1], self.points)

    def get_event(self, event):
        self.pacman.get_event(event)

    def cleanup(self):
        self.done = False
        self.props[const.LEVEL] = str(int(self.props[const.LEVEL]) + 1)
        self.props[const.SCORE] = "0"
        self.pacman.kill()
        self.startup()

    def draw_score(self, display):
        display.blit(self.level, (142, 0))
        display.blit(self.level_score, (142, 21))
        display.blit(self.total, (288, 0))
        display.blit(self.total_score, (288, 21))

    def draw(self, display):
        display.blit(self.background.image, self.background.rect)
        self.draw_score(display)
        self.sprites.draw(display)
        self.points.draw(display)

    def update_score(self):
        self.level = self.font.render(f"LEVEL {self.props[const.LEVEL]}", True, const.WHITE_COLOR)
        self.level_score = self.font.render(self.props[const.SCORE], True, const.WHITE_COLOR)
        self.total_score = self.font.render(self.props[const.TOTAL_SCORE], True, const.WHITE_COLOR)

    def update_points(self):
        if not self.points.sprites():
            self.next = const.LEVEL
            self.done = True
        for point_t in self.points.sprites():
            point_t.update()
            if pygame.sprite.collide_rect(self.pacman, point_t):
                if point_t.point_type == "s":
                    self.props[const.SCORE] = str(int(self.props[const.SCORE]) + const.SMALL_POINT)
                    self.props[const.TOTAL_SCORE] = str(int(self.props[const.TOTAL_SCORE]) + const.SMALL_POINT)
                elif point_t.point_type == "b":
                    self.props[const.SCORE] = str(int(self.props[const.SCORE]) + const.BIG_POINT)
                    self.props[const.TOTAL_SCORE] = str(int(self.props[const.TOTAL_SCORE]) + const.BIG_POINT)
                point_t.kill()

    def update_sprites(self):
        self.update_score()
        self.pacman.update()
        self.update_points()

    def update(self, display):
        display.fill(const.BG_COLOR)
        self.update_sprites()
        self.draw(display)
