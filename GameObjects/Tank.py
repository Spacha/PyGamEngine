from math import radians
from GameEngine.GameObject import *
from GameEngine.Math import Vector

class Barrel:
    def __init__(self, parent, position, length):
        # position could be the barrel base position
        # in relation to parent's center
        self.parent = parent
        self.position = position
        self.length = length

    def direction(self):
        """ Direction (unit) vector. """
        return Vector(cos(self.angle), sin(self.angle))

    def base_position(self):
        """ In global coordinates. """
        return parent.position + self.position

    def tip_position(self):
        """ In global coordinates. """
        return self.base_position() + self.direction() * self.length

"""
Player...
"""
class Tank(GameObject):
    def __init__(self):
        super().__init__()
        print("Invoked Player.")

        self.width = 30
        self.height = 10

        # Barrel
        self.barrel = Barrel(0, -self.height / 2, 10)  # place the barrel to the top-middle of the tank
        
        self.fire_power = 100.0

        self.aim_rate = radians(0.0)
        self.max_aim_rate = radians(90)
        self.barrel_angle_limit = (radians(0.0), radians(85.0))

    def update(self, delta):
        super().update(delta)
        self.barrel.angle += self.aim_rate * delta

        # Limit barrel movement
        if self.barrel.angle < self.min_barrel_angle:
            self.barrel.angle = self.min_barrel_angle
        elif self.barrel.angle > self.max_barrel_angle:
            self.barrel.angle = self.max_barrel_angle

    def draw(self, scr):
        pass

    #----------------------------------------
    #                Actions
    #----------------------------------------

    def aim_up(self):
        self.aim_rate -= (-1 if aim else 1) * self.max_aim_rate

    def aim_down(self):
        self.aim_rate += (-1 if aim else 1) * self.max_aim_rate

    def shoot(self):
        print("Shooting!")
        #projectile = ExplosiveProjectile()
        #projectile.set_position(self.barrel.tip_position())
        #projectile.set_velocity(self.velocity + self.barrel.direction() * self.fire_power)

        #self.game.add_obj(projectile)
