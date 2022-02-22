import sys, time
import pygame as pg
from GameEngine.EventHandling import EventActions, KeyboardActions
from GameEngine.utils import Colors

class Application:
    def __init__(self, scr_size, max_fps, state_machine):
        self.scr_size = scr_size
        self.max_fps = max_fps
        pg.init()
        self.scr = pg.display.set_mode(self.scr_size)
        self.clock = pg.time.Clock()
        self.started_at = time.time()
        self.delta = 1.0
        self.state = state_machine
        self.actions = EventActions()
        self.key_actions = KeyboardActions()
        self.register_actions()
        # init states
        print("Game (Pygame) initialized.")
        for state, state_handler in self.state.get_states().items():
            state_handler.init(self)
    def start(self):
        self.frame = 0 # handle large frame number wrapover!
        self.state.start()
        self.is_running = True
        self.main_loop()
    def handle_events(self):
        pass
    def update(self):
        #if self.in_game: game.update(self.delta)
        self.scr.fill(Colors.BLACK)
        self.state.handler().update(self.scr)  # pass update event to the state
        pass
    def draw(self):
        #if self.in_game: game.draw(self.scr)
        self.state.handler().draw(self.scr)  # pass draw event to the state
        pg.display.update()
        pass
    def tick(self):
        self.frame += 1
        # ticks the clock and returns the delta time
        self.delta = self.clock.tick(self.max_fps) / 1000.0
        #self.delta = self.clock.get_time() / 1000.0
    def actual_fps(self):
        # return 1.0 / self.delta
        return self.clock.get_fps()
    def main_loop(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.tick()
    def register_actions(self):
        """ . """
        self.actions.register(pg.QUIT,               self.quit)
        self.actions.register(pg.KEYDOWN,            self.handle_keydown)
        self.actions.register(pg.KEYUP,              self.handle_keyup)
        self.actions.register(pg.MOUSEMOTION,        self.handle_mousemove)
        self.actions.register(pg.MOUSEBUTTONDOWN,    self.handle_mousedown)
        self.actions.register(pg.MOUSEBUTTONUP,      self.handle_mouseup)

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
    def quit(self, event = None):
        """ Graceful exit from the game. """
        pg.quit()
        sys.exit()

class StateMachine:
    def __init__(self):
        self.state_handlers = {}
    def get_states(self):
        return self.state_handlers
    def set_start(self, start):
        self._start = start
    def start(self):
        if self._start is None:
            raise Exception("Start state is not set! Set it using 'set_start(state)'.")
        self.handler(self._start).state_enter(None)
        self.set_state(self._start)
    def set_state(self, state):
        self.current = state
    def get_state(self):
        return self.current
    def change(self, next_state):
        self.handler().state_leave(next_state)  # notify the previous state of leave
        prev_state = self.current
        self.set_state(next_state)
        self.handler().state_enter(prev_state)  # notify the new state of enter
    def handler(self, state=None): # handle the current state by default
        state = state if state is not None else self.current
        try:
            return self.state_handlers[state]
        except KeyError:
            print("No paska.", state, self.state_handlers)
    def define_state(self, state, handler):
        self.state_handlers[state] = handler

class AppState: # abstract
    def __init__(self):                 # initializes the state (not in use yet!)
        pass
    def init(self):                     # initializes the components of the state -> game is already initialized!
        raise NotImplementedError
    def state_enter(self, prev_state):  # the state is being entered
        raise NotImplementedError
    def state_leave(self, next_state):  # the state is being left
        raise NotImplementedError
    def update(self, delta):            # update internal state
        raise NotImplementedError
    def draw(self, scr):                # draw state
        raise NotImplementedError        

################################################################################
# Game-specific
################################################################################

class GraphicsObject:
    def make_graphic(self):
        pass
class Button(GraphicsObject):
    def __init__(self, text, pos, callback):
        self.text = text
        self.x, self.y = pos
        self.callback = callback
        self.make_graphic()
    def make_graphic(self):
        self.font = pg.font.SysFont("segoeui", 18)
        self.content = self.font.render(self.text, True, Colors.BLACK)
        self.size = self.content.get_size()
        self.surface = pg.Surface(self.size)
        self.surface.fill(Colors.WHITE)
        self.surface.blit(self.content, (0, 0))
        self.rect = pg.Rect(self.x, self.y, self.size[0], self.size[1])
    def mouse_hit(self, button):
        pass
class Text(GraphicsObject):
    def __init__(self, text, pos):
        self.text = text
        self.x, self.y = pos
        self.make()
    def make(self):
        self.font = pg.font.SysFont("segoeui", 26)
        self.update_surface()
        #self.rect = self.content.get_rect()
        #self.surface = pg.Surface(self.size)
        #self.surface.blit(self.content, (0, 0))
    def update_surface(self):
        self.surface = self.font.render(self.text, True, Colors.WHITE)
    def set_text(self, text):
        self.text = text
        self.update_surface()

from enum import Enum, auto
class GameStates(Enum):
    MAIN_MENU  = auto()
    GAME_LOBBY = auto()
    GAME       = auto()

class MainMenu(AppState):
    def __init__(self):
        self.elements = []
    def init(self, app):
        self.app = app
        self.fps_text = Text("", (70, 10))
        self.elements += [
            self.fps_text,
            Button("Lobby", (10, 10), callback=self.go_lobby),
            Button("Exit",  (10, 40), callback=self.go_quit)
        ]
        print("MainMenu initialized")
    def state_enter(self, prev_state):
        pass
    def state_leave(self, next_state):
        pass
    def update(self, delta):
        # TODO: use custom events
        if self.app.frame % 100:
            self.fps_text.set_text( "FPS: {}".format(round(self.app.actual_fps())) )

    def draw(self, scr):
        for elem in self.elements:
            scr.blit(elem.surface, (elem.x, elem.y))
    def add_obj(self, obj):
        pass
    def delete_obj(self, obj_id):
        pass
    def add_particle(self, particle):
        pass
    def delete_particle(self, particle_id):
        pass
    ### Actions (callbacks) ###
    def go_lobby(self):
        self.game.change_state(GameStates.GAME_LOBBY)
    def go_quit(self):
        # game.change_state(GameStates.QUIT)
        print("Quitting.")
        self.game.quit()

class GameLobby(AppState):
    def __init__(self):
        pass
    def init(self, app):
        self.app = app
        print("GameLobby initialized")
    def state_enter(self, prev_state):
        pass
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

class Game(AppState):
    def __init__(self):
        self.objects = {}
    def init(self, app):
        self.app = app
        print("Game initialized")
    def state_enter(self, prev_state):
        pass
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

state_machine = StateMachine()
state_machine.define_state(GameStates.MAIN_MENU,  MainMenu())
state_machine.define_state(GameStates.GAME_LOBBY, GameLobby())
state_machine.define_state(GameStates.GAME,       Game())
state_machine.set_start(GameStates.MAIN_MENU)

#app_settings AppSettings()
#app_settings.window_title = "Paskaaks täs"
app = Application((800, 200), 60.0, state_machine)
app.key_actions.down(pg.K_q, app.quit )

app.start()
