import os
import pygame
from data import constants as const

CAPTION = const.CAPTION

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption(const.CAPTION)
display = pygame.display.set_mode(const.SCREEN_SIZE)
