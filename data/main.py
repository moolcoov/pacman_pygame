from data.tools import Control
from data import constants as const
from data import setup
from data.states import main_menu, level, game_over


def main():
    control = Control(setup.CAPTION)
    states = {
        const.MAIN_MENU: main_menu.MainMenuState()
    }
    control.setup_states(states, const.MAIN_MENU)
    control.main()
