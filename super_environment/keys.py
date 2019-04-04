import tcod
import numpy as np

def handle(key, x, y, width, height):
    """
    tcod.KEY_KP8: 'N', 
    tcod.KEY_KP9: 'NE', 
    tcod.KEY_KP6: 'E', 
    tcod.KEY_KP3: 'SE', 
    tcod.KEY_KP2: 'S', 
    tcod.KEY_KP1: 'SW', 
    tcod.KEY_KP4: 'W', 
    tcod.KEY_KP7: 'NW', 
    tcod.KEY_KP5: 'Wait'
    """
    
    if key == tcod.KEY_KP8:
        x, y = x, y-1
    elif key == tcod.KEY_KP9:
        x, y = x+1, y-1
    elif key == tcod.KEY_KP6:
        x, y = x+1, y
    elif key == tcod.KEY_KP3:
        x, y = x+1, y+1
    elif key == tcod.KEY_KP2:
        x, y = x, y+1
    elif key == tcod.KEY_KP1:
        x, y = x-1, y+1
    elif key == tcod.KEY_KP4:
        x, y = x-1, y
    elif key == tcod.KEY_KP7:
        x, y = x-1, y-1
    elif key == tcod.KEY_KP5:
        x, y = None, None

    try:
        if x < 0 or y < 0:
            x, y = None, None
        elif x >= width or y >= height:
            x, y = None, None
        return x, y
    except TypeError:
        return None, None