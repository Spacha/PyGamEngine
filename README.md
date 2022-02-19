# PyGamEngine
A simple 2D game engine implemented in python using Pygame 2.

# Architecture

## Game
The main class containing the core functionality of the game engine:
* Event registration and handling (game.register_handler(pg.KEYDOWN, game.handle_keydown, etc...).
* Master update: control the physics and world udpdate. These could be separated to their separate classes, though (PhysicsEngine, World).
* Master render: control the rendering of the screen. COuld be separated to class (Renderer).
* Hold the dictionary of all game objects.

## GameObject
A generic class describing an object that lives in the world.

This is never used as is, but it is extended to make different objects (player, ground, enemy, projectile, ...)

GameObject has:
* physical properties: solidity / staticity / ...
* bounding box for collision detection
* object-level update that is called by the master update
* object-level render that is called by the master renderer

## BoundingBox
Describes a solid object's area of collision.
* Point: simplest, very cheap performance-wise
* Rectangle: simple, cheap performance-wise
* Circle: simple, cheap performance-wise
* Collection of these: can be heavy depending of the number of elements

# Other notes

## World map (ground)
The world map must have different collision detection. I would love to have destructable ground. It could be stored as a matrix of integers, where different integer represent different material (non-destructable, destructable, air). Each integer would have a ground element associated with, each having their own color/texture, hardness and solidity.
