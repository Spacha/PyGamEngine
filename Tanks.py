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
        #               Window
        #----------------------------------------
        
        self.window.set_title("Tanks!")

        #----------------------------------------
        #            Create world
        #----------------------------------------
        #world = World()
        player = Player()
        self.add_obj(player)

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
        super().run()
        self.running = True  # this is never set False...
        while self.running:
            self.loop()

    def update(self):
        super().update()

    def render(self):
        super().render()
        pg.display.update()

    def loop(self):
        """ . """
        print(self.delta)
        self.handle_events()
        self.update()
        self.render()
        self.tick()