import math

import pygame

from data import constants as const
from data import tools
from data.components import grid


class Ghost(pygame.sprite.Sprite):
    def __init__(self, start_time, *groups):
        super().__init__(*groups)
        self.rect = None
        self.start_time = start_time
        self.current_time = 0.0
        self.type = None
        self.image = None
        self.mask = None
        self.cell = (0, 0)
        self.v_cell = (0, 0)
        self.home_cell = (0, 0)
        self.w, self.h = 0, 0
        self.x, self.y = 0, 0
        self.mode = None
        self.step = 0
        self.speed = 2
        self.direction = "right"
        self.exit_timer = 0.0
        self.tunnel_timer = 0.0
        self.frighten_timer = 0.0
        self.last_pacman_points = 0
        self.closed = False
        self.turn = (0, 0)

    def update_image(self):
        if any([self.mode == "chase", self.mode == "scatter"]):
            self.image = tools.load_image(f"ghosts/{self.type}/{self.direction}.png")
        if any([self.mode == "frightened", self.mode == "caught"]):
            self.image = tools.load_image(f"ghosts/{self.mode}.png")

        self.w, self.h = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

    def update_exit(self, pacman, major_ghost):
        if self.closed:
            if any([self.exit_timer == 0.0, pacman.points > self.last_pacman_points]):
                self.exit_timer = self.current_time
                self.last_pacman_points = pacman.points

            if self.type == "speedy":
                if any([pacman.points >= 30, (self.current_time - self.exit_timer) / 1000 >= 4]):
                    self.exit_timer = 0.0
                    self.closed = False
                    self.mode = major_ghost.mode if major_ghost.mode != "caught" else "frightened"
                    self.speed = major_ghost.speed if major_ghost.mode != "caught" else 1
            if self.type == "bashful":
                if any([pacman.points >= 60, (self.current_time - self.exit_timer) / 1000 >= 8]):
                    self.exit_timer = 0.0
                    self.closed = False
                    self.mode = major_ghost.mode if major_ghost.mode != "caught" else "frightened"
                    self.speed = major_ghost.speed if major_ghost.mode != "caught" else 1
            if self.type == "pockey":
                if any([pacman.points >= 80, (self.current_time - self.exit_timer) / 1000 >= 12]):
                    self.exit_timer = 0.0
                    self.closed = False
                    self.mode = major_ghost.mode if major_ghost.mode != "caught" else "frightened"
                    self.speed = major_ghost.speed if major_ghost.mode != "caught" else 1

    def update_fright(self, pacman, major_ghost):
        if any([pacman.big_point_mode]):
            self.mode = "frightened"
            self.direction = "right"
            self.speed = 1
            self.frighten_timer = self.current_time

        if any([all([(self.current_time - self.frighten_timer) / 1000 >= 8, self.frighten_timer != 0.0]),
                all([(major_ghost.frighten_timer - self.current_time) / 1000 >= 8, self.frighten_timer != 0.0])]):
            self.frighten_timer = 0.0
            if self.mode != "caught":
                self.mode = "chase"
                self.speed = 2
                self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
        return pacman.big_point_mode

    def update_tunnel(self):
        if any([self.cell == (13, -2), self.cell == (13, 27)]):
            if self.cell == (13, -2):
                self.cell = (13, 26)
                self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
            elif self.cell == (13, 27):
                self.cell = (13, -1)
                self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2

        if all([any([-2 <= self.cell[1] < 5, 20 < self.cell[1] <= 27]), self.cell[0] == 13]):
            self.speed = 1
            self.tunnel_timer = self.current_time

        if all([(self.current_time - self.tunnel_timer) / 1000 >= 1, self.tunnel_timer]):
            self.speed = 2
            self.tunnel_timer = 0.0
            self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2

    def update_caught(self):
        if self.mode == "caught":
            if self.cell == self.home_cell:
                self.mode = "chase"
                self.speed = 2

    def update_scatter(self):
        if any([self.mode == "chase", self.mode == "scatter"]):
            if (self.current_time - self.start_time) / 1000 == 0:
                self.mode = "scatter"
            if (self.current_time - self.start_time) / 1000 >= 7:
                self.mode = "chase"
            if (self.current_time - self.start_time) / 1000 >= 27:
                self.mode = "scatter"
            if (self.current_time - self.start_time) / 1000 >= 34:
                self.mode = "chase"
            if (self.current_time - self.start_time) / 1000 >= 54:
                self.mode = "scatter"
            if (self.current_time - self.start_time) / 1000 >= 59:
                self.mode = "chase"
            if (self.current_time - self.start_time) / 1000 >= 79:
                self.mode = "scatter"
            if (self.current_time - self.start_time) / 1000 >= 84:
                self.mode = "chase"

    def get_directions(self):
        directions = {}
        if all([any([self.cell == (10, 12), self.cell == (10, 13)]), self.mode == "caught"]):
            if self.cell == (10, 13):
                if self.y + self.h // 2 == grid.cells[(self.cell[0], self.cell[1] - self.step)][1]:
                    directions[const.LEFT] = (self.cell[0], self.cell[1] - self.step)
            if self.cell == (10, 12):
                if self.y + self.h // 2 == grid.cells[(self.cell[0], int(self.cell[1] + self.step))][1]:
                    directions[const.RIGHT] = (self.cell[0], self.cell[1] + self.step)
        else:
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

        if all([self.direction == const.UP, const.DOWN in directions]):
            directions.pop(const.DOWN)
        if all([self.direction == const.DOWN, const.UP in directions]):
            directions.pop(const.UP)
        if all([self.direction == const.LEFT, const.RIGHT in directions]):
            directions.pop(const.RIGHT)
        if all([self.direction == const.RIGHT, const.LEFT in directions]):
            directions.pop(const.LEFT)

        if self.cell == (13, 12.5):
            return {const.UP: (10, 12.5)}
        if self.cell == (13, 10.5):
            return {const.RIGHT: (13, 12.5)}
        if self.cell == (13, 14.5):
            return {const.LEFT: (13, 12.5)}

        if all([self.cell in grid.NOT_UP, const.UP in directions]):
            directions.pop(const.UP)

        if all([self.mode == "caught", self.cell == (10, 12.5)]):
            return {const.DOWN: (13, 12.5)}

        return directions

    def update_cell(self, pacman):
        for cell, coords in grid.cells.items():
            if all([int(self.x + self.w // 2) == int(coords[0]),
                    int(self.y + self.h // 2) == int(coords[1])]):
                self.cell = cell

        self.update_tunnel()

        if any([self.cell == grid.default_ghost_cell,
                all([self.mode == "caught", any([self.cell == (10, 12), self.cell == (10, 13)])])]):
            self.step = 0.5
        else:
            self.step = 1

        if not self.closed:
            directions = self.get_directions()
            path = 0
            for direction, cell in directions.items():
                if any([self.mode == "chase", self.mode == "frightened"]):
                    path_t = math.sqrt((pacman.x - grid.cells[cell][0]) ** 2 + (pacman.y - grid.cells[cell][1]) ** 2)
                elif self.mode == "caught":
                    path_t = math.sqrt((grid.cells[self.home_cell][0] - grid.cells[cell][0]) ** 2 + (
                            grid.cells[self.home_cell][1] - grid.cells[cell][1]) ** 2)
                elif self.mode == "scatter":
                    path_t = math.sqrt((grid.cells[self.turn][0] - grid.cells[cell][0]) ** 2 + (
                            grid.cells[self.turn][1] - grid.cells[cell][1]) ** 2)

                if all([self.type == "pockey", self.mode == "chase"]):
                    path_t = math.sqrt((pacman.x - grid.cells[cell][0]) ** 2 + (pacman.y - grid.cells[cell][1]) ** 2)
                    if path_t <= 90:
                        path_t = math.sqrt((grid.cells[self.turn][0] - grid.cells[cell][0]) ** 2 + (
                                grid.cells[self.turn][1] - grid.cells[cell][1]) ** 2)

                if any([self.mode == "chase", self.mode == "caught", self.mode == "scatter"]):
                    if any([path_t < path, path == 0]):
                        path = path_t
                        self.v_cell = cell
                        self.direction = direction
                elif self.mode == "frightened":
                    if any([path_t > path, path == 0]):
                        path = path_t
                        self.v_cell = cell
                        self.direction = direction

    def move(self, pacman):
        if self.type == "shadow":
            self.update_cell(pacman)
        elif any([self.type == "speedy", self.type == "bashful"]):
            if self.type == "speedy":
                step = 1
            elif self.type == "bashful":
                step = 2

            if (pacman.cell[0], pacman.cell[1] + step) in grid.cells:
                rect = pygame.rect.Rect(grid.cells[(pacman.cell[0], pacman.cell[1] + step)][0] - self.w // 2,
                                        grid.cells[(pacman.cell[0], pacman.cell[1] + step)][1] - self.h // 2,
                                        pacman.w, pacman.h)
            elif (pacman.cell[0], pacman.cell[1] - step) in grid.cells:
                rect = pygame.rect.Rect(grid.cells[(pacman.cell[0], pacman.cell[1] - step)][0] - self.w // 2,
                                        grid.cells[(pacman.cell[0], pacman.cell[1] - step)][1] - self.h // 2,
                                        pacman.w, pacman.h)
            else:
                rect = pygame.rect.Rect(grid.cells[(pacman.cell[0], pacman.cell[1])][0] - self.w // 2,
                                        grid.cells[(pacman.cell[0], pacman.cell[1])][1] - self.h // 2,
                                        pacman.w, pacman.h)
            self.update_cell(rect)
        elif self.type == "pockey":
            self.update_cell(pacman)

        if (self.x + self.w // 2) > grid.cells[self.v_cell][0]:
            self.x -= self.step * self.speed
        if (self.x + self.w // 2) < grid.cells[self.v_cell][0]:
            self.x += self.step * self.speed
        if (self.y + self.h // 2) > grid.cells[self.v_cell][1]:
            self.y -= self.step * self.speed
        if (self.y + self.h // 2) < grid.cells[self.v_cell][1]:
            self.y += self.step * self.speed

        self.x, self.y = int(self.x), int(self.y)

    def update(self, pacman, current_time, major_ghost):
        self.current_time = current_time
        self.update_exit(pacman, major_ghost)
        big_point_mode = self.update_fright(pacman, major_ghost)
        self.update_caught()
        self.update_scatter()
        self.move(pacman)
        self.update_image()
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        return big_point_mode


class GhostShadow(Ghost):
    def __init__(self, start_time, *groups):
        super().__init__(start_time, *groups)
        self.type = "shadow"
        self.mode = "scatter"

        self.update_image()

        self.cell = (10, 12.5)
        self.v_cell = self.cell
        self.home_cell = (13, 12.5)

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

        self.turn = grid.RIGHT_UP_TURN
        self.step = 0.5


class GhostSpeedy(Ghost):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.type = "speedy"
        self.mode = "scatter"
        self.closed = True

        self.update_image()

        self.cell = (13, 12.5)
        self.v_cell = self.cell
        self.home_cell = (13, 12.5)

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

        self.turn = grid.LEFT_UP_TURN
        self.step = 0.5


class GhostBashful(Ghost):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.type = "bashful"
        self.mode = "scatter"
        self.closed = True

        self.update_image()

        self.cell = (13, 10.5)
        self.v_cell = self.cell
        self.home_cell = (13, 12.5)

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

        self.turn = grid.RIGHT_DOWN_TURN
        self.step = 0.5


class GhostPockey(Ghost):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.type = "pockey"
        self.mode = "scatter"
        self.closed = True

        self.update_image()

        self.cell = (13, 14.5)
        self.v_cell = self.cell
        self.home_cell = (13, 12.5)

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

        self.turn = grid.LEFT_DOWN_TURN
        self.step = 0.5
