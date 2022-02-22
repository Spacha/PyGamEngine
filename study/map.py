import numpy as np

class Map:
    def __init__(self, data):
        self.data = np.array(data, dtype=int)

    def change_at(self, x, y, change):
        for (change_x, change_y), data in np.ndenumerate(change):
            self.data[x + change_x, y + change_y] = data

    def __str__(self):
        return str(self.data)

map = Map([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

print("Before change")
print(map)

class ExplosionBall:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.x = x
        self.y = y
        self.compile_map_patch()

    def compile_map_patch(self):
        self.map_patch = np.array([], dtype=int) # MapPatch([]) or something as wrapper for these?
        # populate the change map
        # how about if the change map must be reactive to the environment? If the map has hard rock, it doesn't break that easy?
        # then these maps could be weighted: more weight, more destruction!

    def change_map(self):
        self.radius

ball = np.array([
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
])
map.change_at(5, 5, ball)

print("After change")
print(map)