import sys, time
import pygame as pg

from GameEngine.utils import Colors
from GameEngine.Application import Application
from GameEngine.States import StateMachine, AppState
from GameEngine.EventHandling import (
    EventActions,
    KeyboardActions,
    MouseActions,
    UIMouseHandler)

from UserInterface.UIElements import Button, Text

################################################################################
# Game-specific
################################################################################

from enum import Enum, auto
class GameStates(Enum):
    MAIN_MENU  = auto()
    GAME_LOBBY = auto()
    GAME       = auto()

class MainMenu(AppState, UIMouseHandler):
    def __init__(self):
        UIMouseHandler.__init__(self)
        self.elements = []

    def init(self, app):
        UIMouseHandler.init(self, app)
        self.app = app
        self.fps_text = Text("", (70, 10))
        self.elements += [
            self.fps_text,
            Button("Lobby", (10, 10), callback=self.go_lobby),  # MouseUI
            Button("Exit",  (10, 40), callback=self.go_quit)  # MouseUI
        ]
        print("MainMenu initialized")

    def state_enter(self, prev_state):
        # start capturing input
        UIMouseHandler.state_enter(self, prev_state)

    def state_leave(self, next_state):
        # stop capturing input
        pass

    def update(self, delta):
        # TODO: use custom events
        if self.app.frame % 100:
            self.fps_text.set_text( "FPS: {}".format(round(self.app.actual_fps())) )

    def draw(self, scr):
        for elem in self.elements:
            scr.blit(elem.surface, (elem.x, elem.y))

    #----------------------------------------
    #               Actions
    #----------------------------------------

    def go_lobby(self):
        self.app.change_state(GameStates.GAME_LOBBY)
    def go_quit(self):
        # game.change_state(GameStates.QUIT)
        print("Quitting.")
        self.app.quit()

class GameLobby(AppState):
    def __init__(self):
        super().__init__()
    def init(self, app):
        self.app = app
        print("GameLobby initialized")
    def state_enter(self, prev_state):
        print("Entered: Game lobby.")
        self.app.change_state(GameStates.GAME)
    def state_leave(self, next_state):
        pass
    def update(self, delta):
        pass
    def draw(self, scr):
        pass
    def add_obj(self, obj):
        pass
    def delete_obj(self, obj_id):
        pass
    def add_particle(self, particle):
        pass
    def delete_particle(self, particle_id):
        pass

class Game(AppState, UIMouseHandler):
    def __init__(self):
        UIMouseHandler.__init__(self)
        self.objects = {}
        self.elements = []
    def init(self, app):
        UIMouseHandler.init(self, app)
        self.app = app
        self.key_actions.down(pg.K_ESCAPE, self.go_main_menu)
        print("Game initialized")

    def state_enter(self, prev_state):
        UIMouseHandler.state_enter(self, prev_state)
        print("Entered: Game.")

    def state_leave(self, next_state):
        pass

    def update(self, delta):
        pass

    def draw(self, scr):
        pass

    def add_obj(self, obj):
        pass

    def delete_obj(self, obj_id):
        pass

    def add_particle(self, particle):
        pass

    def delete_particle(self, particle_id):
        pass

    def go_main_menu(self):
        self.app.change_state(GameStates.MAIN_MENU)


state_machine = StateMachine()
state_machine.define_state(GameStates.MAIN_MENU,  MainMenu())
state_machine.define_state(GameStates.GAME_LOBBY, GameLobby())
state_machine.define_state(GameStates.GAME,       Game())
state_machine.set_start(GameStates.MAIN_MENU)

app = Application((800, 200), 60.0, state_machine)
app.key_actions.down(pg.K_q, app.quit )

app.start()
