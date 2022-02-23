import sys, time
import pygame as pg
from GameEngine.EventHandling import EventActions, KeyboardActions, MouseActions

"""
Application manages the whole... application.
"""
class Application:
    def __init__(self, scr_size, max_fps, state_machine):
        
        self.scr_size = scr_size
        self.max_fps = max_fps
        self.state = state_machine
        
        # init Pygame
        pg.init()
        self.scr = pg.display.set_mode(self.scr_size)
        self.clock = pg.time.Clock()

        self.started_at = time.time()
        self.delta = 1.0

        # init actions
        self.actions = EventActions()
        self.key_actions = KeyboardActions()
        self.mouse_actions = MouseActions()
        self.register_actions()

        # init states
        for state, state_handler in self.state.get_states().items():
            state_handler.init(self)

    #----------------------------------------
    #              Lifecycle
    #----------------------------------------

    def start(self):
        """ Starts the application and enters the main loop. """
        self.frame = 0
        self.state.start()
        self.is_running = True
        self.main_loop()

    def main_loop(self):
        """ The main application loop. """
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.tick()

    def handle_events(self):
        """ Handle events in queue by passing them to the action handler. """
        self.actions.handle( pg.event.get() )

    def update(self):
        """ Master update. """
        self.scr.fill( (0,0,0) )
        # pass update event to the current state
        self.state.handler().update(self.delta)

    def draw(self):
        """ Master draw. """
        self.state.handler().draw(self.scr)  # pass draw event to the state
        pg.display.update()

    def tick(self):
        """ Ticks the clock and stores the delta time from last frame. """
        self.frame += 1
        self.delta = self.clock.tick(self.max_fps) / 1000.0

    def change_state(self, state):
        """ Change application state to @state. """
        self.state.change(state)

    #----------------------------------------
    #           Event handling
    #----------------------------------------

    def register_actions(self):
        """ Register action handlers for different events. """
        self.actions.register(pg.QUIT,               self.quit)
        self.actions.register(pg.KEYDOWN,            self.handle_keydown)
        self.actions.register(pg.KEYUP,              self.handle_keyup)
        self.actions.register(pg.MOUSEMOTION,        self.handle_mousemove)
        self.actions.register(pg.MOUSEBUTTONDOWN,    self.handle_mousedown)
        self.actions.register(pg.MOUSEBUTTONUP,      self.handle_mouseup)

    # Event Handlers:
    # The basic event handlers (handler_*) first call the current state's own
    # handler and then call the master event handler.

    def handle_keydown(self, event):
        code, key, mod = event.unicode, event.key, event.mod
        for handler in [self.state.handler(), self]:
            handler.key_actions.handle_down(code, key, mod)

    def handle_keyup(self, event):
        key, mod = event.key, event.mod
        for handler in [self.state.handler(), self]:
            handler.key_actions.handle_up(key, mod)

    def handle_mousemove(self, event):
        pos, rel = event.pos, event.rel
        buttons = event.buttons
        for handler in [self.state.handler(), self]:
            handler.mouse_actions.handle_moved(pos, rel, buttons)

    def handle_mousedown(self, event):
        pos, button = event.pos, event.button
        for handler in [self.state.handler(), self]:
            handler.mouse_actions.handle_down(pos, button)

    def handle_mouseup(self, event):
        pos, button = event.pos, event.button
        for handler in [self.state.handler(), self]:
            handler.mouse_actions.handle_up(pos, button)

    def quit(self, event=None):
        """ Graceful exit from the game. """
        pg.quit()
        sys.exit()

    #----------------------------------------
    #           Other methods
    #----------------------------------------

    def actual_fps(self):
        """ Returns the realized FPS averaged from last few seconds. """
        return self.clock.get_fps()