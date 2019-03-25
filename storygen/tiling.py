import numpy as np

class BasicTile():
    def __init__(self, rotatable, mirrorable, _, bytestring):
        self.rotatable = (int(rotatable) == 1)
        self.mirrorable = (int(mirrorable) == 1)
        print(self.__dict__)
        self.base = np.fromstring(bytestring, dtype=np.uint8).reshape(3,3)
        if self.rotatable:
            self.rotations = (np.rot90(self.base, i) for i in range(1,4))
        if self.mirrorable:
            self.mirror = np.flip(self.base, 0)
            self.mir_rot = (np.rot90(self.mirror, i) for i in range(1,4))

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
        self.tiles = np.array([[Tile(i,j) for i in range(height)] for j in range(width)])

    def random_tiles(self, n):
        flat = self.tiles.flatten()
        return np.random.choice(flat, n)

class Tile():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self.__dict__)


if __name__ == '__main__':
    for params, chunk in basic_enc('basic'):
        BasicTile(*params, chunk)

    world = Container(8,8, 'basic')
