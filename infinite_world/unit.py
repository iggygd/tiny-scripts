import CONSTS

class Unit:

    def __init__(self, pos):
        self.pos = pos
        self.wpos = int(pos[0]/CONSTS.SIZE), int(pos[1]/CONSTS.SIZE)

    def update(self, pos):
        self.pos = pos
        self.wpos = int(pos[0]/CONSTS.SIZE), int(pos[1]/CONSTS.SIZE)

class Player(Unit):

    def __init__(self, pos):
        super().__init__(pos)
