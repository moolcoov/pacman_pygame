import sys

import pygame

from data import sentry
from data.main import main

if __name__ == "__main__":
    sentry.init()
    main()
    pygame.quit()
    sys.exit()
