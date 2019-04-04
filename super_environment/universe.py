'''
Universe should hold any environment classes
World, Tile, Map, Force, Entities etc...

The world will consist of layers of bool arrays
The entity layer will consist of entity objects.

In the prototype:
#1. Walls, impassable.
#2. Plants, grow.
#3. Entities, can move.

'''
import numpy as np
import tcod
import keys

class World():
    action_space = {tcod.KEY_KP8: 'N', 
                    tcod.KEY_KP9: 'NE', 
                    tcod.KEY_KP6: 'E', 
                    tcod.KEY_KP3: 'SE', 
                    tcod.KEY_KP2: 'S', 
                    tcod.KEY_KP1: 'SW', 
                    tcod.KEY_KP4: 'W', 
                    tcod.KEY_KP7: 'NW', 
                    tcod.KEY_KP5: 'Wait'}
    action_choices = tuple(action_space)

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.entities = {}

    def entity_make_action(self, entity, action):
        pos = keys.handle(action.vk, entity.x, entity.y, self.width, self.height)
        if pos == (None, None):
            return
        apos = (entity.x, entity.y)
        rpos = pos
        try:
            self.entity_make_interact(self.entities[apos], apos, self.entities[rpos], rpos)
        except KeyError as e:
            print(e)
            self.entity_make_move(apos, rpos)

    def entity_make_move(self, ipos, fpos):
        """
        ipos: initial position, fpos: final position
        """
        self.entities[fpos] = self.entities.pop(ipos)
        self.entities[fpos].x, self.entities[fpos].y = fpos

    def entity_make_interact(self, ant, apos, rnt, rpos):
        """
        apos: actor position, rpos: receiver position 
        ant: actor entity, rnt: receiver entity
        """
        print(f'Interact between {ant}, and {rnt}')