import os
import pygame as pg
import tools
import constants as c

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

GFX = tools.load_graphics(os.path.join("resources", "graphics"))
