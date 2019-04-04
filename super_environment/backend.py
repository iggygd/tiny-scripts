from collections import namedtuple, OrderedDict
from itertools import product
from random import shuffle
import random

import tcod
import numpy as np
import object
import universe

class Engine():
    defs = namedtuple('defs', 'defs max')
    tilemap = defs({
        0: 46, # '.' Open
        1: 35, # '#' Wall
        },
        1
    )
    edef = namedtuple('entity', 'char type')
    entity = defs({
        0: None, # ' ' null
        1: edef(1, object.RandomWalk) # '☺' NPC
        },
        2
    )
    def __init__(self, width, height, render=True):
        """
        args:
            width: tilemap width, height: tilemap height
            env: environment, needs states
            render: render to tcod or not
        """
        self.width = width
        self.height = height
        self.env = universe.World(width, height)

        if render:
            tcod.console_set_custom_font("wanderlust.png", tcod.FONT_LAYOUT_ASCII_INROW)
            tcod.console_init_root(width, height, 'Dungeons')

    def draw(self, env): 
        tcod.console_clear(0)
        for position, entity in env.entities.items():
            tcod.console_put_char(0, entity.x, entity.y, entity.char)
        tcod.console_flush()

    def action(self, env):
        for position, entity in env.entities.items():
            act = entity.act(env)
            env.entity_make_action(entity, act)

    def _debug_random(self, i):
        space = list(product(range(self.width), range(self.height)))
        shuffle(space)

        for pos in space[:i]:
            self.env.entities[pos] = object.RandomWalk(*pos, chr(1))
        print(space[:i])

    def run(self):
        key = tcod.Key()
        mouse = tcod.Mouse()
        update = True

        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
            self.draw(self.env)
            self.action(self.env)

            if key.pressed:
                break

if __name__ == '__main__':
    width = 32
    height = 32
    
    world = Engine(width, height)
    world._debug_random(8)
    world.run()