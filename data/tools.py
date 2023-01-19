import os

import pygame


class Control:
    """
    Main game class
    """

    def __init__(self, caption):
        """
        Inits base statement
        :param caption: (str) caption for screen
        """
        self.current_time = 0.0
        self.display = pygame.display.get_surface()
        self.caption = caption
        self.keys = pygame.key.get_pressed()
        self.states = None
        self.state = None
        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60

    def setup_states(self, states, default_state):
        """
        Setup states for the game
        :param states: (dictionary): Dictionary of states
        :param default_state: (state): Base state
        """
        self.states = states
        self.state = states[default_state](self.current_time, None)

    def flip_state(self):
        props = self.state.cleanup()
        self.state = self.states[self.state.next](self.current_time, props)

    def update(self):
        """
        Updates the current state
        """
        self.current_time = pygame.time.get_ticks()
        if self.state.quit:
            self.running = False
        elif self.state.done:
            self.flip_state()
        self.state.update(self.display, self.current_time)

    def event_loop(self):
        """
        Event processing loop
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state.get_event(event)

    def main(self):
        """
        Main loop of the game
        """
        self.running = True
        while self.running:
            self.event_loop()
            self.update()
            pygame.display.update()
            self.clock.tick(self.fps)


class State(object):
    """
    A parent class for all of states
    """

    def __init__(self):
        self.quit = False
        self.done = False
        self.next = None
        self.props = {}

    def get_event(self, event: pygame.event):
        pass

    def cleanup(self):
        """
        Cleans state up, call if state is done
        :return: (dictionary): props
        """
        self.done = False
        return self.props


def load_image(filename):
    fullname = os.path.join('resources', "graphics", filename)
    image = pygame.image.load(fullname)
    return image
