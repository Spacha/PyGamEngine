"""
Game object...
"""
from GameEngine.Math import Vector

class GameObject:
	def __init__(self, x, y):
		print("Invoked GameObject.")
		self.position = Vector(x, y)
		self.velocity = Vector()

	def set_position(self, x, y):
		self.position.x = x
		self.position.y = y

	def set_velocity(self, x, y):
		self.position.x = x
		self.position.y = y
