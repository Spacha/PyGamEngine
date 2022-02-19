import pygame as pg
import numpy as np
import time
import sys

from GameEngine.EventHandling import EventActions, KeyboardActions
from GameEngine.Window import Window

"""
Game...
"""
class Game:
    def __init__(self, scr_size, max_fps):

        self.scr_size = scr_size
        self.max_fps = max_fps

        # Init pygame
        pg.init()
        self.scr = pg.display.set_mode(self.scr_size)
        self.clock = pg.time.Clock()
        self.window = Window()

        self.actions = EventActions()
        self.key_actions = KeyboardActions()
        self.register_actions()

        self.font_main = pg.font.SysFont('segoeui', 26)
        print("Invoked the game engine.")

        self.delta = 0.0

    #----------------------------------------
    #              Lifecycle
    #----------------------------------------

    def init(self):
        """ This should also be defined by the child. """
        pass

    def run(self):
        """ This must be reimplemented by user. """
        self.started_at = time.time()

    def tick(self):
        self.clock.tick(self.max_fps)
        self.delta = self.clock.get_time() / 1000.0

    def quit(self, event = None):
        """ Graceful exit from the game. """
        pg.quit()
        sys.exit()

    #----------------------------------------
    #              Physics
    #----------------------------------------

    def update(self):
        """ Master update. """
        pass

    #----------------------------------------
    #             Rendering
    #----------------------------------------

    def render(self):
        """ Master render. """
        self.scr.fill(( 0 , 0 , 0 ))
        pass
    #----------------------------------------
    #          Object management
    #----------------------------------------

    def add_obj(self, obj):
        pass

    def delete_obj(self, label):
        pass

    def _add_pending_obj(self):
        pass

    def _delete_pending_obj(self):
        pass

    #----------------------------------------
    #           Event handling
    #----------------------------------------
    
    def register_actions(self):
        self.actions.register(pg.QUIT,               self.quit)
        self.actions.register(pg.KEYDOWN,            self.handle_keydown)
        self.actions.register(pg.KEYUP,              self.handle_keyup)
        self.actions.register(pg.MOUSEMOTION,        self.handle_mousemove)
        self.actions.register(pg.MOUSEBUTTONDOWN,    self.handle_mousedown)
        self.actions.register(pg.MOUSEBUTTONUP,      self.handle_mouseup)
        pass

    def handle_events(self):
        self.actions.handle( pg.event.get() )

    def handle_keydown(self, event):
        code, key, mod = event.unicode, event.key, event.mod
        self.key_actions.handle_down(code, key, mod)

    def handle_keyup(self, event):
        key, mod = event.key, event.mod
        self.key_actions.handle_up(key, mod)

    def handle_mousemove(self, event):
        pos, rel = event.pos, event.rel
        buttons = event.buttons
        #self.mouse.actions.moved(pos, rel, buttons)

    def handle_mousedown(self, event):
        pos, buttons = event.pos, event.button
        #self.mouse.actions.down(pos, button)

    def handle_mouseup(self, event):
        pos, buttons = event.pos, event.button
        #self.mouse.actions.up(pos, button)
