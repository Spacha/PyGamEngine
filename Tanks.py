import pygame as pg
from GameObjects.Player import *

from GameEngine.Core import Game

"""
The actual game...
"""
class Tanks(Game):
    # *args, **kwargs
    def __init__(self, scr_size, max_fps):
        super().__init__(scr_size, max_fps)
        print("Invoked Tanks.")

    def init(self):
        super().init()

        #----------------------------------------
        #            Create world
        #----------------------------------------
        player = Player()


        #----------------------------------------
        #            Register keys
        #----------------------------------------

        # meta
        self.key_actions.down( pg.K_q,     self.quit )
        # player movement
        self.key_actions.down( pg.K_LEFT,  lambda: player.move_left(True) )
        self.key_actions.up( pg.K_LEFT,    lambda: player.move_left(False) )
        self.key_actions.down( pg.K_RIGHT, lambda: player.move_right(True) )
        self.key_actions.up( pg.K_RIGHT,   lambda: player.move_right(False) )
        # player activity
        self.key_actions.down( pg.K_UP,    lambda: player.aim_up(True) )
        self.key_actions.up( pg.K_UP,      lambda: player.aim_up(False) )
        self.key_actions.down( pg.K_DOWN,  lambda: player.aim_down(True) )
        self.key_actions.up( pg.K_DOWN,    lambda: player.aim_down(False) )

        self.key_actions.down( pg.K_x,     lambda: player.shoot() )
        self.key_actions.down( pg.K_SPACE, lambda: player.jump() )

    def run(self):
        self.running = True
        while self.running:
            self.loop()

    def loop(self):
        """ . """
        self.handle_events()
