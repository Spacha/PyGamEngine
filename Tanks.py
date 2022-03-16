import pygame as pg
from GameObjects.Tank import *

from GameEngine.Core import Game
from ConnectionManager import ConnectionManager as Server

class GameActivity:
    def __init__(self, server, player=None):
        self.server = server
        self.player = player

    def set_player(self, player):
        self.player = player

    def shoot(self, player=None):
        if player is None or player == self.player:  # None => current player, not opponent
            player = self.player
            #self._async_server_update('shoot')
            self.server.update('shoot')
        player.shoot()


"""
The actual game...
"""
class Tanks(Game):
    # *args, **kwargs
    def __init__(self, scr_size, max_fps):
        super().__init__(scr_size, max_fps)
        print("Invoked Tanks.")
        self.server = Server('localhost', 8765)
        self.game_activity = GameActivity(self.server)

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
        player = Tank()
        self.add_obj(player)

        self.game_activity.set_player(player)

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

        self.key_actions.down( pg.K_x,     self.game_activity.shoot )
        self.key_actions.down( pg.K_SPACE, lambda: player.jump() )

        self.server.connect('js-room', 'Spacha')

    def run(self):
        super().run()
        self.running = True  # this is never set False...
        while self.running:
            self.loop()

    def handle_events(self):
        super().handle_events()
        #if activity:
        #    self.server.update(activity)

    def update(self):
        super().update()

    def loop(self):
        """ . """
        self.handle_events()
        self.update()
        self.draw()
        self.tick()
