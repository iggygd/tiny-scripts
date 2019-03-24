class Game:
    def __init__(self):
        self.id = id
        self.turn = 0
        self.world = world

class World:
    def __init__(self, size):
        self.size = size
        self.tiles = []
        self.properties = {}

    def add_tile(tile):
        self.tiles.append(tile)

    def load(self):
        pass

    def save(self):
        pass

class Tile:
    def __init__(self):
        self.pos = pos
        self.world = world
        self.neighbours = None
