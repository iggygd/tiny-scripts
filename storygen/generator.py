import numpy as np
import random

def get_neighbours(direction, tile, tiles):
    pass

def build_neighbour_map(tiles):
    indices = {}
    for i, tile in enumerate(tiles):
        for j, nx_tile in enumerate(tiles):
            _compare(tile, nx_tile, indices)
    
    return indices

def _compare(tile_a, tile_b, indices):
    '''
    N : [a[0,:] == b[2,:]]
    E : [a[:,2] == b[:,0]]
    S : [a[2,:] == b[0,:]]
    W : [a[:,0] == b[:,2]]
    '''
    if np.array_equal(tile_a[0,:], tile_b[2,:]):
        _add(tile_a, tile_b, 'E', indices)
    if np.array_equal(tile_a[:,2], tile_b[:,0]):
        _add(tile_a, tile_b, 'N', indices)
    if np.array_equal(tile_a[2,:], tile_b[0,:]):
        _add(tile_a, tile_b, 'W', indices)
    if np.array_equal(tile_a[:,0], tile_b[:,2]):
        _add(tile_a, tile_b, 'S', indices)

def _add(tile_a, tile_b, dir, indices):
    if tile_a.tostring() not in indices:
        indices[tile_a.tostring()] = {}

    try:
        indices[tile_a.tostring()][dir].append(tile_b.tostring())
    except KeyError:
        indices[tile_a.tostring()][dir] = [tile_b.tostring()]

def full(defs, tiles, n=2):
    flat = tiles.flatten()
    spawns = np.random.choice(flat, n).tolist()
    for tile in spawns:
        tile.tile = b'.........'

    while spawns:
        choice = random.choice(spawns)
        try:
            n_choice = random.choice(list(_get_neighbours(choice, tiles).values()))
            n_choice.tile = random.choice(_get_possibilities(defs, n_choice, tiles))
            spawns.append(n_choice)
        except IndexError as e:
            spawns.remove(choice)

def _get_neighbours(tile, tiles, case = None):
    x = tile.x
    y = tile.y
    neighbours = {}
    if _get(x, max(y-1, 0), tiles, case) is not None:
        neighbours['N'] = _get(x, max(y-1, 0), tiles, case)
    if _get(x+1, y, tiles, case) is not None:
        neighbours['E'] = _get(x+1, y, tiles, case)
    if _get(x, y+1, tiles, case) is not None:
        neighbours['S'] = _get(x, y+1, tiles, case)
    if _get(max(x-1, 0), y, tiles, case) is not None:
        neighbours['W'] = _get(max(x-1, 0), y, tiles, case)

    return neighbours

def _get_possibilities(defs, tile, tiles):
    sets = []
    for dir, neighbour in _get_neighbours(tile, tiles, True).items():
        #dir == _opposite(dir)
        try:
            sets.append(set(defs[neighbour.tile][dir]))
        except KeyError:
            continue

    u = set.intersection(*sets)
    if not u:
        return [b'#########']
    else:
        return list(u)

def _get(x, y, tiles, case):
    try:
        tile = tiles[x][y]
        if case is None:
            if tile.tile is None:
                return tiles[x][y]
            else:
                return None
        else:
            if tile.tile is not None:
                return tiles[x][y]
            else:
                return None
    except IndexError as e:
        return None

def _opposite(dir):
    if dir == 'N':
        return 'S'
    elif dir == 'E':
        return 'W'
    elif dir == 'S':
        return 'N'
    elif dir == 'W':
        return 'E'
    