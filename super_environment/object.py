import tcod
import random
import numpy as np
np.set_printoptions(threshold=np.inf)

class Entity():
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def act(self, env):
        raise NotImplementedError

class User(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self, env):
        return None

    def act(self, env):
        key = tcod.console_wait_for_keypress(True)
        return key

class NPC(Entity):
    pass

class RandomWalk(NPC):
    def act(self, env):
        choice = random.choice(env.action_choices)
        return tcod.Key(pressed=True, vk=choice)

class Consumable(Entity):
    pass