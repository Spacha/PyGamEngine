import pygame as pg
from GameEngine.utils import Colors

"""
The base of any UI element.
"""
class UIElement:
    def __init__(self):
        self.interactive = False
    def make(self):
        pass
"""
Interactive UI element.
"""
class InteractiveUIElement(UIElement):
    def __init__(self, callback):
        super().__init__()
        self.interactive = True
        self.callback = callback
        self.hovered = False
        self.pressed = False
    def mouse_enter(self, buttons):
        self.hovered = True
    def mouse_leave(self, buttons):
        self.hovered = False
    def mouse_press(self, button):
        self.pressed = True
    def mouse_release(self, button):
        self.pressed = False
    def click(self): # mouse released on button
        self.callback()

"""
A clickable button.
"""
class Button(InteractiveUIElement):
    def __init__(self, text, pos, callback):
        super().__init__(callback)
        self.text = text
        self.x, self.y = pos
        self.callback = callback
        self.make_graphic()

    def reset(self):  # common for all interactives
        self.hovered = False
        self.pressed = False
        self.update_surface()

    def make_graphic(self):
        """ Pre-render the element's graphics. """
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

"""
A non-interactive text.
"""
class Text(UIElement):
    def __init__(self, text, pos):
        self.interactive = False  # should be required by UIElement
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
        if text == self.text: return  # don't bother
        self.text = text
        self.update_surface()