class World():
    def __init__(self, w, h):
        self.width = w
        self.height = h

class ExternalTile():
    '''
    Algorithm
    1. Evenly distribute starting tiles in world (eg. City, Mountain Top, Ocean Depth)
    2. Determine possible neighbours
        (eg.
        "Village": [Farmland, Plains, Forest, Ocean],
        "Mountain Top": [Valley, Mountain Hill, Cliff])
    '''
    def __init__(self):
        self.inside = InternalTile(self, exits) 

class InternalTile():
    '''
    Algorithm
    1. Randomly insert default locations for tile
    2. Determine possible neighbours 
        (eg. 
        "Tavern" : [Road, Shed, N, NE, E, SE, S, SW, W, NW],
        "Cave" : [Outside, Treasure_Room])
    3. Iterate until connections to [N, NE, E, SE, S, SW, W, NW] which are exits, are all fulfilled
    '''
    def __init__(self, exits):
        self.network = Network(exits)

class Network():
