# NOTE: Not in the core of the engine; rather in Physics section.

"""
Game object...
"""
from GameEngine.Math import Vector

class BoundingBox:
	def __init__(self):
		pass

class GameObject:
	def __init__(self, x=0, y=0):
		print("Invoked GameObject.")
		self.position = Vector(x, y)
		self.velocity = Vector(0, 0)

	def set_bounding_box(self, bounding_box):
		self.bounding_box = bounding_box

	def set_position(self, x, y):
		self.position.x = x
		self.position.y = y

	def set_velocity(self, x, y):
		self.velocity.x = x
		self.velocity.y = y
