import pygame.sprite

from data import tools


class Point(pygame.sprite.Sprite):
    def __init__(self, point_type, cell_x, cell_y, *groups):
        super().__init__(*groups)
        self.point_type = point_type
        self.setup_image()
        self.w, self.h = self.image.get_size()
        self.x, self.y = cell_x - self.w // 2, cell_y - self.h // 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def setup_image(self):
        if self.point_type == "s":
            self.image = tools.load_image("point_s.png")
        elif self.point_type == "b":
            self.image = tools.load_image("point_b.png")

    def update(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
