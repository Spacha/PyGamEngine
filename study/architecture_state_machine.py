import sys, time
import pygame as pg
from GameEngine.EventHandling import EventActions, KeyboardActions, MouseActions
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
        self.mouse_actions = MouseActions()
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
    def change_state(self, state):
        self.state.change(state)
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

    """ Event Handlers:
        The basic event handlers (handler_*) first call the current state's own
        handler and then call the master event handler.
    """
    def handle_keydown(self, event):
        code, key, mod = event.unicode, event.key, event.mod
        for handler in [self.state.handler(), self]:
            handler.key_actions.handle_down(code, key, mod)

    def handle_keyup(self, event):
        key, mod = event.key, event.mod
        for handler in [self.state.handler(), self]:
            handler.key_actions.handle_up(code, key, mod)

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
        self.key_actions = KeyboardActions()
        self.mouse_actions = MouseActions()
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

class UIElement:
    def __init__(self):
        self.mouse_interactive = False
    def make_graphic(self):
        pass
class InteractiveUIElement(UIElement):
    def __init__(self, callback):
        self.mouse_interactive = True
        self.callback = callback
        self.hovered = False
        self.pressed = False
    def mouse_enter(self, buttons):
        print("Enter Button!")
        self.hovered = True
    def mouse_leave(self, buttons):
        print("Leave Button!")
        self.hovered = False
    def mouse_press(self, button):
        print("Press Button!")
        self.pressed = True
    def mouse_release(self, button):
        print("Release Button!")
        self.pressed = False
    def click(self): # mouse released on button
        self.callback()
class Button(InteractiveUIElement):
    def __init__(self, text, pos, callback):
        super().__init__(callback)
        self.text = text
        self.x, self.y = pos
        self.callback = callback
        self.make_graphic()
    def make_graphic(self):
        self.font = pg.font.SysFont("segoeui", 18)
        self.content = self.font.render(self.text, True, Colors.BLACK)
        self.size = self.content.get_size()
        self.surface = pg.Surface(self.size)
        self.update_surface()
        self.width, self.height = self.size
    def update_surface(self):
        self.surface.fill(Colors.WHITE if not self.hovered else Colors.RED)
        self.surface.blit(self.content, (0, 0))
    def mouse_enter(self, buttons):
        super().mouse_enter(buttons)
        self.update_surface()
    def mouse_leave(self, buttons):
        super().mouse_leave(buttons)
        self.update_surface()

class Text(UIElement):
    def __init__(self, text, pos):
        self.mouse_interactive = False  # should be required by UIElement
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
        self.width, self.height = self.surface.get_size()
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
        super().__init__()
        self.elements = []
    def init(self, app):
        self.app = app
        self.mouse_actions.move(self.mouse_moved)  # MouseUI
        self.mouse_actions.down(self.mouse_down)   # MouseUI
        self.mouse_actions.up(self.mouse_up)       # MouseUI
        self.hovered = []  # MouseUI
        self.pressed = []  # MouseUI
        self.fps_text = Text("", (70, 10))
        self.elements += [
            self.fps_text,
            Button("Lobby", (10, 10), callback=self.go_lobby),  # MouseUI
            Button("Exit",  (10, 40), callback=self.go_quit)  # MouseUI
        ]
        print("MainMenu initialized")
    def state_enter(self, prev_state):
        # start capturing input
        pass
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

    ### TODO: Mouse actions in a UI mouse handler ###
    def mouse_moved(self, pos, rel, buttons):
        # print(pos, rel, buttons)
        for elem in self.elements:

            # ABSTRACT THIS IF-ELSE, SAME USED IN OTHERS AS WELL

            if not elem.mouse_interactive: continue
            if (elem.x <= pos[0] <= elem.x + elem.width and
                elem.y <= pos[1] <= elem.y + elem.height):
                if elem not in self.hovered:  # element is just entered
                    self.hovered.append(elem)
                    elem.mouse_enter(buttons)
                    #elem.hover(buttons)
            elif elem in self.hovered:  # element not under mouse
                self.hovered.remove(elem) # isn't the fastes't?
                elem.mouse_leave(buttons)

    def mouse_down(self, pos, button):
        for elem in self.hovered:  # only check for elements that are currently hovered
            if button == 1:
                if elem not in self.pressed:  # element is just entered
                    self.pressed.append(elem)
                    elem.mouse_press(button)
                    #elem.hover(button)

    def mouse_up(self, pos, button):
        for elem in self.pressed:  # only check for elements that are currently hovered
            if button == 1:
                if elem in self.hovered:  # if still hover --> click
                    elem.click()
                self.pressed.remove(elem)
                elem.mouse_release(button)

    ### Actions (callbacks) ###
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

class Game(AppState):
    def __init__(self):
        super().__init__()
        self.objects = {}
    def init(self, app):
        self.app = app
        print("Game initialized")
    def state_enter(self, prev_state):
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
