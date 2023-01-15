import pygame

from data import tools


class LiveBar(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.lives_1_image = tools.load_image("lives/1.png")
        self.lives_2_image = tools.load_image("lives/2.png")
        self.lives_3_image = tools.load_image("lives/3.png")

        self.image = self.lives_3_image

        self.w, self.h = self.image.get_size()
        self.x, self.y = 15, 604
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def change_image(self, lives):
        if lives == 3:
            self.image = self.lives_3_image
        elif lives == 2:
            self.image = self.lives_2_image
        elif lives == 1:
            self.image = self.lives_1_image
        self.w, self.h = self.image.get_size()

    def update(self):
        self.rect = pygame.rect.Rect(self.x, self.y, self.w, self.h)
