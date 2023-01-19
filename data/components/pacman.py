import pygame

from data import tools
from data.components import grid


class Pacman(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.default_image = tools.load_image("pacman/pacman_default.png")
        self.up_image = tools.load_image("pacman/pacman_up.png")
        self.down_image = tools.load_image("pacman/pacman_down.png")
        self.left_image = tools.load_image("pacman/pacman_left.png")
        self.right_image = tools.load_image("pacman/pacman_right.png")

        self.image = self.default_image
        self.mask = pygame.mask.from_surface(self.image)

        self.cell = (22, 12.5)

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

        self.points = 0
        self.big_point_mode = False

        self.pressed = set()
        self.speed = 2
        self.step = 1

    def update_cell(self):
        for cell, coords in grid.cells.items():
            if all([(self.x + self.w // 2) == coords[0],
                    (self.y + self.h // 2) == coords[1]]):
                self.cell = cell

        if self.cell == grid.default_cell:
            self.step = 0.5
        else:
            self.step = 1

        if self.cell == (13, -2):
            self.x, self.y = grid.cells[(13, 26)][0] - self.w // 2, grid.cells[(13, 26)][1] - self.h // 2
        if self.cell == (13, 27):
            self.x, self.y = grid.cells[(13, -1)][0] - self.w // 2, grid.cells[(13, -1)][1] - self.h // 2

    def update_image(self, direction):
        if direction == "up":
            self.image = self.up_image
        elif direction == "down":
            self.image = self.down_image
        elif direction == "left":
            self.image = self.left_image
        elif direction == "right":
            self.image = self.right_image

        self.w, self.h = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

    def get_event(self, event):
        """
        Event handler
        :param event: {pygame.event} Event
        """
        if event.type == pygame.KEYDOWN:
            self.pressed.add(event.key)
        if event.type == pygame.KEYUP:
            try:
                self.pressed.remove(event.key)
            except KeyError:
                pass

    def move(self):
        """
        Moves the pacman
        """
        self.update_cell()

        # Keyboard events handler
        for event_key in self.pressed:
            if event_key == pygame.K_UP:
                if all([(self.cell[0] - self.step, self.cell[1]) in grid.cells,
                        int(self.x + self.w // 2) == grid.cells[self.cell][0]]):
                    self.update_image("up")
                    self.y -= self.step * self.speed

            if event_key == pygame.K_DOWN:
                if all([(self.cell[0] + self.step, self.cell[1]) in grid.cells,
                        int(self.x + self.w // 2) == grid.cells[self.cell][0]]):
                    self.update_image("down")
                    self.y += self.step * self.speed

            if event_key == pygame.K_LEFT:
                if all([(self.cell[0], self.cell[1] - self.step) in grid.cells,
                        int(self.y + self.h // 2) == grid.cells[self.cell][1]]):
                    self.update_image("left")
                    self.x -= self.step * self.speed

            if event_key == pygame.K_RIGHT:
                if all([(self.cell[0], self.cell[1] + self.step) in grid.cells,
                        int(self.y + self.h // 2) == grid.cells[self.cell][1]]):
                    self.update_image("right")
                    self.x += self.step * self.speed

    def update(self):
        self.move()
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
