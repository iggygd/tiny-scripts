import CONSTS
import pygame as pg
import threading
import worldgen

from PIL import Image
from pathlib import Path

class Chunk():

    def __init__(self, size, pos, generator):
        root = Path('./world/'+str(CONSTS.SEED))
        filepath = root / (str(pos[0])+','+str(pos[1])+'.bmp')
        if not root.exists():
            root.mkdir(exist_ok=True)

        self.pos = pos
        if not self.fromFile(pos, root):
            im = Image.new(CONSTS.IMAGE_MODE, (size,size))
            px = im.load()

            for i in range(size):
                for j in range(size):
                    px[i, j] = int(generator.get(i+pos[0]*size,j+pos[1]*size)*255)

            im.save(filepath)
            im.close()
            self.surface = pg.image.load(str(filepath))

    def fromFile(self, pos, root):
        filepath = root / (str(pos[0])+','+str(pos[1])+'.bmp')
        if filepath.exists():
            self.surface = pg.image.load(str(filepath))
            return True
        else:
            return False
