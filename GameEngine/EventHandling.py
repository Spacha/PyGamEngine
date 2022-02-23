"""
Event actions...
"""
class EventActions:
    def __init__(self):
        # a dictionary containing action for each event registered
        self.actions = {}

    def register(self, event, callback):
        """
            Register a new with a callback
        """
        self.actions[event] = callback

    def handle(self, events):
        """
            Handle a list of events.
        """
        for event in events:
            try:
                # call the callback if found
                self.actions[event.type](event)
            except KeyError:
                continue

"""
Keyboard actions...
"""
class KeyboardActions:
    def __init__(self):
        # a dictionary containing action for each event registered
        self.actions_down = {}
        self.actions_up = {}

    def down(self, key, action):
        # does not handle mod keys -> need another method for that (ctrlDown...)
        self.actions_down[key] = action

    def up(self, key, action):
        # dos not handle mod keys -> need another method for that (ctrlDown...)
        self.actions_up[key] = action

    def handle_down(self, code, key, mod):
        # does not (yet) handle mod keys
        try:
            self.actions_down[key]()
        except KeyError:
            return

    def handle_up(self, key, mod):
        # does not (yet) handle mod keys
        try:
            self.actions_up[key]()
        except KeyError:
            return

"""
Mouse actions...
"""
class MouseActions:
    def __init__(self):
        self.move_handlers = []
        self.down_handlers = []
        self.up_handlers = []
    def move(self, handler):
        self.move_handlers.append(handler)
    def down(self, handler):
        self.down_handlers.append(handler)
    def up(self, handler):
        self.up_handlers.append(handler)
    def handle_moved(self, pos, rel, buttons):
        for handler in self.move_handlers:
            handler(pos, rel, buttons)
    def handle_down(self, pos, button):
        for handler in self.down_handlers:
            handler(pos, button)
    def handle_up(self, pos, button):
        for handler in self.up_handlers:
            handler(pos, button)

"""
Inherit this in your state if you want to have mouse interaction in GUI.
"""
class UIMouseHandler:
    def __init__(self):
        self.hovered = []
        self.pressed = []
        self.key_actions = KeyboardActions()
        self.mouse_actions = MouseActions()

    def init(self, app):
        self.mouse_actions.move(self.mouse_moved)
        self.mouse_actions.down(self.mouse_down)
        self.mouse_actions.up(self.mouse_up)

    def state_enter(self, prev_state):
        """
        When state is entered, reset the state of
        each interactive UI element.
        """
        while self.hovered:
            self.hovered.pop().reset()
        while self.pressed:
            self.pressed.pop().reset()

    def mouse_moved(self, pos, rel, buttons):
        for elem in self.elements:

            # ABSTRACT THIS IF-ELSE, SAME USED IN OTHERS AS WELL

            if not elem.interactive: continue
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