import game
import generator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from numpy import asarray, concatenate, ones
from shapely.geometry import Polygon, MultiPolygon
import random

def display():
    pass

def test():
    aPoints = np.random.randint(-512, 512, 128).tolist()
    bPoints = np.random.randint(-512, 512, 128).tolist()
    points = []
    for i in range(len(aPoints)):
        points.append([aPoints[i], bPoints[i]])

    points = np.asarray(points)

    from scipy.spatial import Voronoi, voronoi_plot_2d
    from scipy.spatial import Delaunay
    vor = Voronoi(points, qhull_options = '')
    tri = Delaunay(points)

    #print(vor.point_region)
    #print(tri.points)

    print(points[0])
    indices, indptr = tri.vertex_neighbor_vertices
    neighbors = indptr[indices[0]:indices[0+1]]
    print(neighbors)
    for index in neighbors:
        print(points[index])

    voronoi_plot_2d(vor)
    plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
    plt.plot(points[:,0], points[:,1], 'o')
    plt.show()

def gameTest():
    world_size = 16384
    #points, polygons, neighbours, type, allowed = generator.generate(8192,2048,iter = 2)
    #points, polygons, neighbours, type, allowed = generator.generate(8192,2048,iter = 2,seed=random.getrandbits(64))
    points, polygons, neighbours, type, allowed, disallowed, bg = generator.generate(world_size,8192,iter = 2,seed=random.getrandbits(64)) #random.getrandbits(64)
    fig = plt.figure(0, figsize=(9,9), dpi=100)
    plt.subplots_adjust(bottom = 0)
    plt.subplots_adjust(top = 1)
    plt.subplots_adjust(right = 1)
    plt.subplots_adjust(left = 0)
    plt.axis('off')
    ax = fig.add_subplot(111)
    ax.set_xlim(-world_size, world_size)
    ax.set_ylim(-world_size, world_size)
    #Change to a,b,c,d... later
    for i, pair in enumerate(zip(points, polygons, neighbours, type)):
        #print(str(i)+'/'+str(len(points)))
        polygon = [p for p in pair[1].exterior.coords]
        if pair[3] == 'MOUNTAIN':
            plt.fill(*zip(*polygon), 'k', alpha=0.6)
        elif pair[3] == 'FOREST':
            plt.fill(*zip(*polygon), color='#030D03', alpha=0.8, edgecolor='k')
        elif pair[3] == 'PLAINS':
            plt.fill(*zip(*polygon), 'g', alpha=0.6, edgecolor='k')
        elif pair[3] == 'DESERT':
            plt.fill(*zip(*polygon), 'y', alpha=0.6, edgecolor='k')
        elif pair[3] == 'ICE':
            plt.fill(*zip(*polygon), 'w', alpha=0.6, edgecolor='k')
        else:
            plt.fill(*zip(*polygon), color='#00008b', alpha=0.6, edgecolor='k')
        #plt.plot(pair[0][0], pair[0][1], 'go')
        #plt.annotate(str(points.index(pair[0])), pair[0])
        #for index in pair[2]:
        #    plt.plot([pair[0][0], points[index][0]], [pair[0][1], points[index][1]], 'ro-', markersize=1)

    fig2 = plt.figure(1, figsize=(9,9), dpi=100)
    plt.subplots_adjust(bottom = 0)
    plt.subplots_adjust(top = 1)
    plt.subplots_adjust(right = 1)
    plt.subplots_adjust(left = 0)
    plt.axis('off')
    ax = fig2.add_subplot(111)
    ax.set_xlim(-world_size, world_size)
    ax.set_ylim(-world_size, world_size)

    if isinstance(allowed, MultiPolygon):
        for poly in allowed.geoms:
            path = pathify(poly)
            patch = PathPatch(path, facecolor='g', edgecolor='k', alpha=0.4)
            ax.add_patch(patch)
    else:
        path = pathify(allowed)
        patch = PathPatch(path, facecolor='g', edgecolor='k', alpha=0.4)
        ax.add_patch(patch)


    fig3 = plt.figure(2, figsize=(9,9), dpi=100)
    plt.subplots_adjust(bottom = 0)
    plt.subplots_adjust(top = 1)
    plt.subplots_adjust(right = 1)
    plt.subplots_adjust(left = 0)
    plt.axis('off')
    ax = fig3.add_subplot(111)
    if isinstance(disallowed, MultiPolygon):
        for poly in disallowed.geoms:
            path = pathify(poly)
            patch = PathPatch(path, facecolor='k', edgecolor='k', alpha=0.4)
            ax.add_patch(patch)
    else:
        path = pathify(disallowed)
        patch = PathPatch(path, facecolor='g', edgecolor='k', alpha=0.4)
        ax.add_patch(patch)
    ax.set_xlim(-world_size, world_size)
    ax.set_ylim(-world_size, world_size)

    fig4 = plt.figure(3, figsize=(9,9), dpi=100)
    plt.subplots_adjust(bottom = 0)
    plt.subplots_adjust(top = 1)
    plt.subplots_adjust(right = 1)
    plt.subplots_adjust(left = 0)
    plt.axis('off')
    ax = fig4.add_subplot(111)
    for poly in bg:
        if isinstance(poly, MultiPolygon):
            for poly_ in poly.geoms:
                path = pathify(poly_)
                patch = PathPatch(path, facecolor='b', edgecolor='k', alpha=0.4)
                ax.add_patch(patch)
        else:
            path = pathify(poly)
            patch = PathPatch(path, facecolor='b', edgecolor='k', alpha=0.4)
            ax.add_patch(patch)
    ax.set_xlim(-world_size, world_size)
    ax.set_ylim(-world_size, world_size)

    fig.savefig('debug_whole.png', dpi=300)
    fig2.savefig('debug_unmerged.png', dpi=300)
    fig3.savefig('debug_merged.png', dpi=300)
    plt.show()

def ring_coding(ob):
    # The codes will be all "LINETO" commands, except for "MOVETO"s at the
    # beginning of each subpath
    n = len(ob.coords)
    codes = ones(n, dtype=Path.code_type) * Path.LINETO
    codes[0] = Path.MOVETO
    return codes

def pathify(polygon):
    # Convert coordinates to path vertices. Objects produced by Shapely's
    # analytic methods have the proper coordinate order, no need to sort.
    vertices = concatenate(
                    [asarray(polygon.exterior)]
                    + [asarray(r) for r in polygon.interiors])
    codes = concatenate(
                [ring_coding(polygon.exterior)]
                + [ring_coding(r) for r in polygon.interiors])
    return Path(vertices, codes)

gameTest()
