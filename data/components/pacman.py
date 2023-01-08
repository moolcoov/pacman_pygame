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
        self.cell = (22, 12.5)

        self.w, self.h = self.image.get_size()
        self.x, self.y = grid.cells[self.cell][0] - self.w // 2, grid.cells[self.cell][1] - self.h // 2

        self.in_x_cell = True
        self.in_y_cell = True

        self.pressed = None
        self.speed = 4
        self.step = 1

        self.clock = pygame.time.Clock()
        self.speed = 2

    def update_cell(self):
        for cell, coords in grid.cells.items():
            if all([(self.x + self.w // 2) == coords[0],
                    (self.y + self.h // 2) == coords[1]]):
                self.cell = cell
        print(self.cell)
        print(self.x + self.w // 2, grid.cells[self.cell][0])

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

    def get_event(self, event):
        """
        Event handler
        :param event: {pygame.event} Event
        """
        if event.type == pygame.KEYDOWN:
            self.pressed = event.key
        if event.type == pygame.KEYUP:
            self.pressed = None

    def move(self):
        """
        Moves the pacman
        """
        # Moves from start position
        if self.cell == grid.default_cell:
            self.step = 0.5
        else:
            self.step = 1

        self.update_cell()

        # Keyboard events handler
        if self.pressed == pygame.K_UP:
            if all([(self.cell[0] - self.step, self.cell[1]) in grid.cells,
                    int(self.x + self.w // 2) == grid.cells[self.cell][0]]):
                self.update_image("up")
                self.y -= self.step * self.speed

        if self.pressed == pygame.K_DOWN:
            if all([(self.cell[0] + self.step, self.cell[1]) in grid.cells,
                    int(self.x + self.w // 2) == grid.cells[self.cell][0]]):
                self.update_image("down")
                self.y += self.step * self.speed

        if self.pressed == pygame.K_LEFT:
            if all([(self.cell[0], self.cell[1] - self.step) in grid.cells,
                    int(self.y + self.h // 2) == grid.cells[self.cell][1]]):
                self.update_image("left")
                self.x -= self.step * self.speed

        if self.pressed == pygame.K_RIGHT:
            if all([(self.cell[0], self.cell[1] + self.step) in grid.cells,
                    int(self.y + self.h // 2) == grid.cells[self.cell][1]]):
                self.update_image("right")
                self.x += self.step * self.speed

    def update(self):
        self.move()
        self.rect = ((self.x, self.y), (self.w, self.h))
