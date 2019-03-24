from pygame import Rect

class Camera:

    def __init__(self, pos):
        self.pos = pos

    def apply(self, pos):
        return int(pos[0] - self.pos[0]), int(pos[1] - self.pos[1])

    def update(self, pos):
        self.pos = pos
