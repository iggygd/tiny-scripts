import gzip
import numpy as np

from functools import reduce

def mnist(path):
    with gzip.open(path, mode='rb') as file:
        assert file.read(2) == b'\x00\x00'
        _dtype = file.read(1)
        _dims = int.from_bytes(file.read(1), byteorder='big')
        _items = int.from_bytes(file.read(4), byteorder='big')

        e_xyz = tuple(int.from_bytes(file.read(4), byteorder='big') for i in range(_dims-1))

        try:
            size = reduce(lambda x, y: x*y, e_xyz)
        except TypeError:
            size = 1

        return np.fromstring(file.read(), dtype=np.uint8).reshape((_items, size))


