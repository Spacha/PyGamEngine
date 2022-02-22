from math import sin, cos, sqrt
from utils import unsupported

"""
2D Vector.
"""
class Vector:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def length(self, other):
        return sqrt(self.x**2 + self.y**2)

    def direction(self, other):
        # returns the unit vector (direction only)
        return sqrt(self.x**2 + self.y**2)

    def angle(self, other):
        # returns the angle of the vector in radians
        return NotImplemented

    def __mul__(self, other):
        # multiply vector by scalar
        if type(other) in [int, float]:
            return Vector(self.x * other, self.y * other)
        else:
            unsupported('*', self, other)

    def __truediv__(self, other):
        # divide vector by scalar
        if type(other) in [int, float]:
            return Vector(self.x / other, self.y / other)
        else:
            unsupported('/', self, other)

    def __add__(self, other):
        # sum two vectors
        if type(other) is Vector:
            return Vector(self.x + other.x, self.y + other.y)
        else:
            unsupported('+', self, other)

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
