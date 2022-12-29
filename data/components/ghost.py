import pygame as pg
from .. import setup


class Ghost:
    pass


class GhostShadow(Ghost):
    def __init__(self):
        self.icon = setup.GFX['ghost_shadow']


class GhostSpeedy(Ghost):
    def __init__(self):
        self.icon = setup.GFX['ghost_speedy']


class GhostBashful(Ghost):
    def __init__(self):
        self.icon = setup.GFX['ghost_bashful']


class GhostPockey(Ghost):
    def __init__(self):
        self.icon = setup.GFX['ghost_pockey']
