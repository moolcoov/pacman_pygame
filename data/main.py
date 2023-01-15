from data import constants as const
from data import setup
from data.states import main_menu, level, game_over
from data.tools import Control


def main():
    control = Control(setup.CAPTION)
    states = {
        const.MAIN_MENU: main_menu.MainMenuState,
        const.LEVEL: level.LevelState,
        const.GAME_OVER: game_over.GameOverState
    }
    control.setup_states(states, const.MAIN_MENU)
    control.main()
