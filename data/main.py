import constants as c
import tools
from states import main_menu, level


def main():
    run_it = tools.Control()
    state_dict = {c.MAIN_MENU: main_menu.Menu(),
                  c.LEVEL: level.Level()}

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()
