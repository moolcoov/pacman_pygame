import pygame

from data import constants as const
from data import tools
from data.components import pacman, grid, point, live_bar, ghost


class LevelState(tools.State):
    def __init__(self, start_time, props):
        super().__init__()
        self.props = props
        self.start_time = start_time
        self.points = pygame.sprite.AbstractGroup()
        self.ghosts = pygame.sprite.AbstractGroup()
        self.sprites = pygame.sprite.AbstractGroup()
        self.startup()

    def startup(self):
        self.setup_props()
        self.setup_bg()
        self.setup_score()
        self.setup_live_bar()
        self.setup_pacman()
        self.setup_points()
        self.setup_ghosts()

    def setup_props(self):
        if not self.props:
            self.props = {
                const.LEVEL: "1",
                const.SCORE: "0",
                const.TOTAL_SCORE: "0",
                const.LIVES: "3"
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

    def setup_live_bar(self):
        self.live_bar = live_bar.LiveBar(self.sprites)

    def setup_pacman(self):
        self.pacman = pacman.Pacman(self.sprites)

    def setup_points(self):
        for coords in grid.cells.values():
            if any([coords[2] == "s", coords[2] == "b"]):
                point.Point(coords[2], coords[0], coords[1], self.sprites, self.points)

    def setup_ghosts(self):
        self.ghost_shadow = ghost.GhostShadow(self.sprites, self.ghosts)

    def get_event(self, event):
        self.pacman.get_event(event)

    def cleanup(self):
        self.done = False
        if self.props[const.LIVES] == "0":
            self.props[const.LEVEL] = "1"
            self.props[const.SCORE] = "0"
            self.props[const.LIVES] = "3"
        else:
            self.props[const.LEVEL] = str(int(self.props[const.LEVEL]) + 1)
            self.props[const.SCORE] = "0"
        self.pacman.kill()
        self.startup()
        return self.props

    def draw_score(self, display):
        display.blit(self.level, (142, 0))
        display.blit(self.level_score, (142, 21))
        display.blit(self.total, (288, 0))
        display.blit(self.total_score, (288, 21))

    def draw(self, display):
        display.blit(self.background.image, self.background.rect)
        self.draw_score(display)
        self.sprites.draw(display)

    def update_score(self):
        self.level = self.font.render(f"LEVEL {self.props[const.LEVEL]}", True, const.WHITE_COLOR)
        self.level_score = self.font.render(self.props[const.SCORE], True, const.WHITE_COLOR)
        self.total_score = self.font.render(self.props[const.TOTAL_SCORE], True, const.WHITE_COLOR)

    def update_lives(self, lives=None):
        if lives:
            self.props[const.LIVES] = str(int(self.props[const.LIVES]) - lives)
            self.pacman.kill()
            for ghost in self.ghosts.sprites():
                ghost.kill()
            self.setup_pacman()
            self.setup_ghosts()
            self.start_time = self.current_time
        if self.props[const.LIVES] == "0":
            pygame.mouse.set_visible(True)
            self.next = const.GAME_OVER
            self.done = True
        self.live_bar.change_image(int(self.props[const.LIVES]))
        self.live_bar.update()

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

    def update_ghosts(self):
        for ghost in self.ghosts.sprites():
            ghost.update(self.pacman.rect)
            if any([pygame.sprite.collide_rect(self.pacman, ghost), self.pacman.cell == ghost.cell]):
                self.update_lives(1)

    def update_sprites(self):
        self.update_score()
        self.update_lives()
        self.pacman.update()
        self.update_points()
        self.update_ghosts()

    def update(self, display, current_time):
        self.current_time = current_time
        display.fill(const.BG_COLOR)
        if (self.current_time - self.start_time) / 1000 > 2:
            self.update_sprites()
        self.draw(display)
