from opensimplex import OpenSimplex
import CONSTS

class WorldGenerator():

    def __init__(self, a = CONSTS.SEED):
        self.simplex = OpenSimplex(seed = a)

    def pct50(self, x, y):
        x = x/CONSTS.FEATURE_SIZE
        y = y/CONSTS.FEATURE_SIZE

        if self.simplex.noise2d(x, y) > .5:
            return 1
        else:
            return 0.5

    def get(self, x, y):
        return self.pct50(x, y)
