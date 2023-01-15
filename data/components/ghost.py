import math

import pygame

from data import constants as const
from data import tools
from data.components import grid


class Ghost(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.type = None
        self.image = None
        self.cell = (0, 0)
        self.v_cell = (0, 0)
        self.w, self.h = 0, 0
        self.x, self.y = 0, 0
        self.mode = None
        self.step = 0
        self.speed = 2
        self.direction = None

    def set_image(self):
        self.image = tools.load_image(f"ghosts/{self.type}.png")

    def get_directions(self):
        directions = {}
        if (int(self.cell[0] - self.step), self.cell[1]) in grid.cells:
            if self.x + self.w // 2 == grid.cells[(int(self.cell[0] - self.step), self.cell[1])][0]:
                directions[const.UP] = (int(self.cell[0] - self.step), self.cell[1])
        if (int(self.cell[0] + self.step), self.cell[1]) in grid.cells:
            if self.x + self.w // 2 == grid.cells[(int(self.cell[0] + self.step), self.cell[1])][0]:
                directions[const.DOWN] = (int(self.cell[0] + self.step), self.cell[1])
        if (self.cell[0], int(self.cell[1] - self.step)) in grid.cells:
            if self.y + self.h // 2 == grid.cells[(self.cell[0], int(self.cell[1] - self.step))][1]:
                directions[const.LEFT] = (self.cell[0], int(self.cell[1] - self.step))
        if (self.cell[0], int(self.cell[1] + self.step)) in grid.cells:
            if self.y + self.h // 2 == grid.cells[(self.cell[0], int(self.cell[1] + self.step))][1]:
                directions[const.RIGHT] = (self.cell[0], int(self.cell[1] + self.step))

        if self.direction == const.UP and const.DOWN in directions:
            directions.pop(const.DOWN)
        if self.direction == const.DOWN and const.UP in directions:
            directions.pop(const.UP)
        if self.direction == const.LEFT and const.RIGHT in directions:
            directions.pop(const.RIGHT)
        if self.direction == const.RIGHT and const.LEFT in directions:
            directions.pop(const.LEFT)

        return directions

    def update_cell(self, pacman_pos):
        for cell, coords in grid.cells.items():
            if all([int(self.x + self.w // 2) == int(coords[0]),
                    int(self.y + self.h // 2) == int(coords[1])]):
                self.cell = cell

        if self.cell == grid.default_ghost_cell:
            self.step = 0.5
        else:
            self.step = 1

        directions = self.get_directions()
        path = 0
        for direction, cell in directions.items():
            path_t = math.sqrt((pacman_pos.x - grid.cells[cell][0]) ** 2 + (pacman_pos.y - grid.cells[cell][1]) ** 2)
            if path_t < path or path == 0:
                path = path_t
                self.v_cell = cell
                self.direction = direction

    def move(self, pacman_pos):
        self.update_cell(pacman_pos)

        if (self.x + self.w // 2) > grid.cells[self.v_cell][0]:
            self.x -= self.step * self.speed
        if (self.x + self.w // 2) < grid.cells[self.v_cell][0]:
            self.x += self.step * self.speed
        if (self.y + self.h // 2) > grid.cells[self.v_cell][1]:
            self.y -= self.step * self.speed
        if (self.y + self.h // 2) < grid.cells[self.v_cell][1]:
            self.y += self.step * self.speed

        self.x, self.y = int(self.x), int(self.y)

    def update(self, pacman_pos):
        self.move(pacman_pos)
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)


class GhostShadow(Ghost):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.type = "shadow"
        self.set_image()

        self.cell = (10, 12.5)
        self.v_cell = self.cell

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2

        self.mode = "pursuit"
        self.step = 0.5
