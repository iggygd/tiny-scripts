from PIL import Image
import timeit

WIDTH = 64
HEIGHT = 64

def bitmap():
    im = Image.new('1', (WIDTH,HEIGHT))
    px = im.load()

    for i in range(WIDTH):
        for j in range(HEIGHT):
            print(px[i, j])

def matrix():
    arr = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

    for ia in arr:
        for elem in ia:
            print(elem)

a = timeit.timeit(stmt='bitmap()', setup="from __main__ import bitmap", number=100)
b = timeit.timeit(stmt='matrix()', setup="from __main__ import matrix", number=100)

print(a, b)
