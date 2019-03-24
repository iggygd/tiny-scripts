import pygame as pg
import unit
import chunk as ch
import sys
import camera
import math
import threading
import worldgen

import CONSTS

class World():

    def __init__(self, size):
        pg.init()
        self.ssize = size
        self.screen = pg.display.set_mode((size[0], size[1]))
        pg.display.set_caption("It goes on.")
        self.clock = pg.time.Clock()

        self.world_generator = worldgen.WorldGenerator()
        self.loaded = []
        self.player = unit.Player((0,0))
        self.heroes = [self.player]
        self.camera = camera.Camera((int(-size[0]/2),int(-size[0]/2)))

        self.chunker_ready = False


    def display(self):
        for chunk in self.loaded:
            worldPos = chunk.pos[0]*CONSTS.SIZE, chunk.pos[1]*CONSTS.SIZE
            try:
                self.screen.blit(chunk.surface, self.camera.apply(worldPos))
            except AttributeError:
                print("chunk.surface does not exist, maybe generating")

        pg.display.flip()

    def update(self):
        self.clock.tick(60)

    def chunker(self, heroes, maximum):
        for hero in heroes:
            for chunk in self.loaded:
                distance = max(abs(hero.wpos[0] - chunk.pos[0]), abs(hero.wpos[1] - chunk.pos[1]))

                if distance > maximum:
                    self.unload(chunk)

            for i in range(-maximum, maximum + 1):
                for j in range(-maximum, maximum + 1):
                    self.load((hero.wpos[0] + i, hero.wpos[1] + j))

    def load(self, pos):
        for chunk in self.loaded:
            if chunk.pos == pos:
                return None
        else:
            self.loaded.append(ch.Chunk(CONSTS.SIZE, pos, self.world_generator))

    def unload(self, chunk):
        self.loaded.remove(chunk)

    def playerUpdate(self, left, right, up, down):
        if left:
            self.player.update((self.player.pos[0] - 1, self.player.pos[1]))
        if right:
            self.player.update((self.player.pos[0] + 1, self.player.pos[1]))
        if up:
            self.player.update((self.player.pos[0], self.player.pos[1] - 1))
        if down:
            self.player.update((self.player.pos[0], self.player.pos[1] + 1))

    def cameraUpdate(self, target):
        self.camera.update((target.pos[0] + int(-self.ssize[0]/2 + CONSTS.SIZE/2), target.pos[1] + int(-self.ssize[0]/2 + CONSTS.SIZE/2)))

    def run(self):
        self.running = True
        left, right, up, down = False, False, False, False

        threading.Thread(target=self.chunkerThread).start()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        left = True
                    if event.key == pg.K_RIGHT:
                        right = True
                    if event.key == pg.K_UP:
                        up = True
                    if event.key == pg.K_DOWN:
                        down = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        left = False
                    if event.key == pg.K_RIGHT:
                        right = False
                    if event.key == pg.K_UP:
                        up = False
                    if event.key == pg.K_DOWN:
                        down = False
                if event.type == pg.QUIT:
                    self.running = False
                    sys.exit(0)

            self.screen.fill((0,0,0))

            self.chunker_ready = True
            self.playerUpdate(left, right, up, down)
            self.cameraUpdate(self.player)
            self.display()
            self.update()

    def chunkerThread(self):
        while self.running:
            if self.chunker_ready:
                self.chunker(self.heroes, CONSTS.MAXIMUM_RANGE)
                self.chunker_ready = False
            else:
                pass
