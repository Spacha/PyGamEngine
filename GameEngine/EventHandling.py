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
