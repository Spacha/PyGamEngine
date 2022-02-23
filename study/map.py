import numpy as np
import pygame as pg
import os, sys, time

from GameEngine.utils import Colors, PerfTimer

# map is always static
class Material:
    def __init__(self, name, solid, hardness, color, transparent=False):
        self.name = name
        self.solid = solid
        self.hardness = hardness
        self.color = color
        self.transparent = transparent

    def is_bound_to(self, clr):
        if self.transparent:  # if transparent, only alpha matters
            return clr.all(0)
        else:
            return (self.color[0] == clr[0] and
                    self.color[1] == clr[1] and
                    self.color[2] == clr[2])

# hardness = 0-10
MATERIALS = [
    Material("air",  False, 0, Colors.BLACK, True), # 0
    Material("sand", True,  3, Colors.SANDY),       # 1
    Material("rock", True,  8, Colors.GREY),        # 2
]

class Map:
    # map could have a separate "texture", which takes care of the presentation of the map
    def __init__(self, png): # png is typeof pg.Surface
        self.png_to_map(png)

    # patch => replace area with given patch
    # erode => replace area with given patch based on the hardness

    def get_at(self, x, y):
        return self.map[y,x]

    def patch_at(self, x, y, change):
        for (change_x, change_y), data in np.ndenumerate(change):
            self.data[y + change_y, x + change_x] = data

    def erode_at(self, x, y, weights):
        """
        Erodes non-transparent materials on the map base don the 
        """
        for (change_x, change_y), data in np.ndenumerate(change):
            self.data[y + change_y, x + change_x] = data

    def __str__(self):
        return str(self.data)

    def png_to_map(self, png):
        """ . """

        # For each pixel: [0,0,0,0] => False, otherwise True
        #bitmap = np.any(bitmap[::-1], axis=2)

        # Ok, this is different:
        # last element of each pixel value (= alpha) > 0 => True
        #bitmap = bitmap[:,:,-1] > 20
        width, height = png.get_width(), png.get_height()
        buffer = np.array(png.get_buffer(), dtype=int).reshape(height, width, 4) # ordering: [row[bit[r,g,b,a]]]

        self.map = np.zeros((height, width), dtype=int)
        for y, row in enumerate(buffer):
            for x, pixel in enumerate(row):
                for material_id, material in enumerate(MATERIALS):
                    if material.is_bound_to(pixel):
                        self.map[y,x] = material_id

        #for r in buffer[0::4]:
        #    print(r)



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

'''
ball = np.array([
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
])
map.change_at(5, 5, ball)
'''
class Game:
    def __init__(self, scr_size, fps):
        self.scr_size = scr_size
        self.fps = fps

        # Init pygame
        pg.init()
        self.scr = pg.display.set_mode(self.scr_size)
        pg.display.set_caption("Map test")
        self.clock = pg.time.Clock()
        
        # Graphics stuff
        self.background_clr = Colors.BLACK
        self.font_main = pg.font.SysFont('segoeui', 26)

        self.create_map('study/testmap.png')
        #self.create_map('large.png')

    def create_map(self, filename):
        map_img = pg.image.load( os.path.join(*filename.split('/')) )
        self.map = Map(map_img)

    def start_match(self, settings):
        self.match_settings = settings

    def update(self):
        pass
    def draw(self):
        self.scr.fill(self.background_clr)
        
        # draw...

    def tick(self):
        self.clock.tick(self.fps)
        self.delta = self.clock.get_time() / 1000.0

ptimer = PerfTimer()
game = Game((200, 200), 60.0)

match_settings = {
    "map": "large.png",
    "players": 2,
    # other...
}
game.start_match(match_settings)

if not pg.image.get_extended():
    raise Exception("Need extended Pygame to support PNGs.")

exit = False
while not exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True
        if event.type == pg.KEYDOWN:
            # emergency exit
            if event.key == pg.K_q:
                exit = True

    game.update()
    game.draw()
    pg.display.update()
    game.tick()

pg.quit()
sys.exit()
