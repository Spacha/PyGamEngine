"""
State Machine. Manages the application state(s) and transitions between them.
"""
class StateMachine:
    def __init__(self):
        self.state_handlers = {}
        self._start = None

    def start(self):
        """ Enter the start state. """
        if self._start is None:
            raise Exception("Start state is not set! Set it using 'set_start(state)'.")

        self.handler(self._start).state_enter(None)
        self.set_state(self._start)

    def change(self, next_state):
        """ Change state and call state_leave & state_enter. """
        # notify the previous state of leave
        self.handler().state_leave(next_state)
        prev_state = self.current
        self.set_state(next_state)
        # notify the new state of enter
        self.handler().state_enter(prev_state)

    def handler(self, state=None):
        """
        Return the state handler of @satate. If not
        given, current state handler is returned.
        """
        state = state if state is not None else self.current
        return self.state_handlers[state]

    def define_state(self, state, handler):
        """ Bind a handler to state. """
        self.state_handlers[state] = handler

    def set_start(self, start):
        """ Set @state to be the start state. """
        self._start = start

    def set_state(self, state):
        """
        Set a new state as current. NOTE: Use change_state
        when transitioning between states!
        """
        self.current = state

    def get_state(self):
        """ Get the current state. """
        return self.current

    def get_states(self):
        """ Return a dict containing all the registered states. """
        return self.state_handlers


""" abstract AppState
Extend this to create application states (e.g. main menu, game, ...).
"""
class AppState:
    def __init__(self):
        """
        Pre-initializes the state. The application
        has not been created yet.
        """
        pass

    def init(self):
        """
        Initializes the components of the state.
        The application is initialized.
        """
        raise NotImplementedError

    def state_enter(self, prev_state):
        """ The state is being entered from another state. """
        raise NotImplementedError

    def state_leave(self, next_state):
        """ The state is being left to another state. """
        raise NotImplementedError

    def update(self, delta):
        """ Update state. """
        raise NotImplementedError

    def draw(self, scr):
        """ Draw state. """
        raise NotImplementedError
