# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, Delaunay
from shapely.geometry import Polygon
import itertools
from opensimplex import OpenSimplex
from PIL import Image

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()*2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)

# make up data points
aPoints = np.random.randint(-1024, 1024, 256).tolist()
bPoints = np.random.randint(-1024, 1024, 256).tolist()
points = []
for i in range(len(aPoints)):
    points.append([aPoints[i], bPoints[i]])

points = np.asarray(points)

# compute Voronoi tesselation
vor = Voronoi(points)

# plot
regions, vertices = voronoi_finite_polygons_2d(vor)

min_x = vor.min_bound[0] - 0.1
max_x = vor.max_bound[0] + 0.1
min_y = vor.min_bound[1] - 0.1
max_y = vor.max_bound[1] + 0.1

mins = np.tile((min_x, min_y), (vertices.shape[0], 1))
bounded_vertices = np.max((vertices, mins), axis=0)
maxs = np.tile((max_x, max_y), (vertices.shape[0], 1))
bounded_vertices = np.min((bounded_vertices, maxs), axis=0)

box = Polygon([[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]])

# colorize
new_points = []
for region in regions:
    polygon = vertices[region]
    # Clipping polygon
    poly = Polygon(polygon)
    poly = poly.intersection(box)
    #polygon = [p for p in poly.exterior.coords]
    new_points.append([poly.centroid.x, poly.centroid.y])
    #plt.fill(*zip(*polygon), alpha=0.4)

new_points = np.array(new_points)
vor = Voronoi(new_points)

# plot
regions, vertices = voronoi_finite_polygons_2d(vor)

min_x = vor.min_bound[0] - 0.1
max_x = vor.max_bound[0] + 0.1
min_y = vor.min_bound[1] - 0.1
max_y = vor.max_bound[1] + 0.1

mins = np.tile((min_x, min_y), (vertices.shape[0], 1))
bounded_vertices = np.max((vertices, mins), axis=0)
maxs = np.tile((max_x, max_y), (vertices.shape[0], 1))
bounded_vertices = np.min((bounded_vertices, maxs), axis=0)

box = Polygon([[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]])

polygons = []
tmp = OpenSimplex()
for region in regions:
    polygon = vertices[region]
    # Clipping polygon
    poly = Polygon(polygon)
    poly = poly.intersection(box)
    polygons.append(poly)
    polygon = [p for p in poly.exterior.coords]
    if tmp.noise2d(new_points[regions.index(region)][0]/256, new_points[regions.index(region)][1]/256) >= 0:
        plt.fill(*zip(*polygon), 'g', alpha=0.4)
    else:
        plt.fill(*zip(*polygon), 'b', alpha=0.4)

print(new_points)
for poly1, poly2 in itertools.combinations(polygons, 2):
    if poly1.touches(poly2):
        p1_i = polygons.index(poly1)
        p2_i = polygons.index(poly2)
        print('Polygon, ', p1_i, 'touches Polygon', p2_i)
        plt.plot([new_points[p1_i][0], new_points[p2_i][0]], [new_points[p1_i][1], new_points[p2_i][1]], 'ro-' )
im = Image.new('RGB', (2048, 2048))
px = im.load()
for x in range(-1024, 1024):
    for y in range(-1024, 1024):
        if tmp.noise2d(x/256, y/256) >= 0:
            px[x+1024,y+1024] = (102, 153, 102)
        else:
            px[x+1024,y+1024] = (0, 119, 190)
im = im.transpose(Image.FLIP_TOP_BOTTOM)
im.save('back.png')


plt.plot(new_points[:, 0], new_points[:, 1], 'o')
for i in range(len(new_points)):
    plt.annotate(str(i), new_points[i])
plt.axis('equal')
plt.xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
plt.ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)


plt.savefig('voro.png', dpi=300)
plt.show()
