import math
import numpy as np
import generator
import time

class BasicTile():
    def __init__(self, rotatable, mirrorable, _, bytestring):
        self.rotatable = (int(rotatable) == 1)
        self.mirrorable = (int(mirrorable) == 1)
        self.base = np.fromstring(bytestring, dtype=np.uint8).reshape(3,3)
        if self.rotatable:
            self.rotations = tuple(np.rot90(self.base, i) for i in range(1,4))
        if self.mirrorable:
            self.mirror = np.flip(self.base, 0)
            self.mir_rot = tuple(np.rot90(self.mirror, i) for i in range(1,4))

    def flat(self):
        all = [self.base]
        if self.rotatable:
            all.extend(self.rotations)
        if self.mirrorable:
            all.extend([self.mirror])
            all.extend(self.mir_rot)

        return all

def basic_enc(file):
    with open(file, 'r') as file:
        for chunk in iter(lambda: file.read(16), ""):
            params, chunk = chunk.split('\n',1)
            chunk = chunk.replace('\n','')
            yield params, chunk

class Container():
    def __init__(self, width, height, file):
        self.width = width
        self.height = height
        self.tiles = np.array([[Tile(i,j) for j in range(height)] for i in range(width)])
        self.defs = [BasicTile(*params, chunk) for params, chunk in basic_enc(file)]
        l = []
        for tile in self.defs:
            l.extend(tile.flat())
        self.neighbours = generator.build_neighbour_map(l)

        generator.full(self.neighbours, self.tiles, n=int(math.sqrt(width*height)/2))

    def random_tiles(self, n):
        flat = self.tiles.flatten()
        return np.random.choice(flat, n)

class Tile():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tile = None

    def get_tile_as(self):
        return self.tile[:3], self.tile[3:6], self.tile[6:9]

    def __repr__(self):
        try:
            return str(self.tile[5])
        except TypeError:
            return '00'

def new_world(x, y):
    world = None
    while world is None:
        try:
            #Large sizes are very slow... algorithm could be better
            #Try chaining small worlds next to each other
            world = Container(x,y, 'basic')
        except:
            continue
    tiles = []
    for i in world.tiles:
        a = []
        b = []
        c = []
        for j in i:
            x,y,z = j.get_tile_as()
            a.extend(x), b.extend(y), c.extend(z)
        tiles.append(a), tiles.append(b), tiles.append(c)
    map_ = np.array(tiles).astype(np.uint8)

    return world, map_


if __name__ == '__main__':
    size = (9,16)
    #Large sizes are very slow... algorithm could be better
    #Try chaining small maps next to each other
    world, map_ = new_world(*size)

    import tcod
    tcod.console_set_custom_font("terminal16x16_gs_ro.png", tcod.FONT_LAYOUT_ASCII_INROW)
    y, x = map_.shape
    tcod.console_init_root(x, y, 'Generator')

    key = tcod.Key()
    mouse = tcod.Mouse()
    draw = True
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        for i, row in enumerate(map_):
            tcod.console_print(0, 0, i, row.tostring())
        tcod.console_flush()
        if key.pressed:
            break
        #time.sleep(2) #change to timer and thread when you can
        world, map_ = new_world(*size)
        
        