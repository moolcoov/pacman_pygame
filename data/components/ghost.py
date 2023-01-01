import pygame as pg
from data import setup


class Ghost:
    def __init__(self):
        self.icon = None
        self.rect = None
    
    def draw(self, display):
        display.blit(self.icon, )


class GhostShadow(Ghost):
    def __init__(self):
        super().__init__()
        self.icon = setup.GFX['ghost_shadow']
        self.type = "shadow"
        self.rect = ((0, 0), (self.icon.get_size()))


class GhostSpeedy(Ghost):
    def __init__(self):
        super().__init__()
        self.icon = setup.GFX['ghost_speedy']
        self.type = "speedy"


class GhostBashful(Ghost):
    def __init__(self):
        super().__init__()
        self.icon = setup.GFX['ghost_bashful']
        self.type = "bashful"


class GhostPockey(Ghost):
    def __init__(self):
        super().__init__()
        self.icon = setup.GFX['ghost_pockey']
        self.type = "pockey"
