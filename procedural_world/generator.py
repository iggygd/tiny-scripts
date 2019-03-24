import game
import itertools
import math
from scipy.spatial import Voronoi, Delaunay
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import cascaded_union
from opensimplex import OpenSimplex
from pyqtree_git import Index
import numpy as np

def generate(size, number, iter = 1, seed = 0, redundancy = 2):
    x_ = np.random.randint(-size, size, number).tolist()
    y_ = np.random.randint(-size, size, number).tolist()
    points = list(set(zip(x_, y_)))

    print('STAGE ONE-TERRAIN INITIALIZATION')
    print('Generating points and polygons')
    points, polygons = clipped_voronoi(points, size, relax = True, iterations = iter)
    types = get_types(points, seed, size)
    neighbours, _ = get_neighbours(points, polygons, size)

    '''
    Rework? -Oct11
    print('STAGE TWO-TERRAIN MODIFICATION')
    print('Removing redundant tiles')
    remove_index = get_surrounded_oceans(points, types, neighbours,
    ('WATER', 'MOUNTAIN', 'PLAINS', 'FOREST'), ('WATER', 'MOUNTAIN'))
    for point in remove_index:
        points.remove(point)
    points, polygons = clipped_voronoi(points, size, relax = False, iterations = iter)
    types = get_types(points, seed, size)
    neighbours, _ = get_neighbours(points, polygons, size)
    '''

    print('STAGE THREE-WATER MODIFICATION')
    print('Merging polygons')
    DISALLOWED = ('WATER')
    #Change later to be variable and multiple types of disallowed tiles as well
    allowed_polygons = []
    disallowed_polygons = []
    for index, polygon in enumerate(polygons):
        if types[index] not in DISALLOWED:
            allowed_polygons.append(polygon)
        else:
            disallowed_polygons.append(polygon)

    merged_allowed_polygons = cascaded_union(allowed_polygons)
    merged_disallowed_polygons = cascaded_union(disallowed_polygons)

    print('Splitting water polygons')
    num_bg = int(np.sqrt(number))

    x_bg = np.random.randint(-size, size, num_bg).tolist()
    y_bg = np.random.randint(-size, size, num_bg).tolist()
    points_bg = list(set(zip(x_bg, y_bg)))

    points_bg, polygons_bg = clipped_voronoi(points_bg, size, relax = True, iterations = 23)
    types_bg = get_types(points_bg, seed, size)

    points_bg = isolate_of_type(points_bg, types_bg, 'WATER')
    points_bg, polygons_bg = clipped_voronoi(points_bg, size, relax = False)

    water_polygons = []
    for poly in polygons_bg:
        intersected_polygons = poly.intersection(merged_disallowed_polygons)
        if intersected_polygons.is_empty:
            print('empty')
        if isinstance(intersected_polygons, MultiPolygon):
            for separate_polygon in intersected_polygons:
                water_polygons.append(separate_polygon)
        else:
            water_polygons.append(intersected_polygons)

    water_polygons = merge_small(water_polygons, size)
    water_points = [(poly.centroid.x, poly.centroid.y) for poly in water_polygons]
    water_types = ['WATER' for poly in water_polygons]

    land_points, land_polygons, land_types = remove_of_type(points, polygons, types, 'WATER')

    print('Merge water and land to full list')
    points = water_points + land_points
    polygons = water_polygons + land_polygons
    types = water_types + land_types

    neighbours, _ = get_neighbours(points, polygons, size)

    print('STAGE FOUR-PLACE SUPPLY CENTERS')
    print('FINISHED')
    return (points, polygons, neighbours, types, merged_allowed_polygons, merged_disallowed_polygons,
    water_polygons)

def merge_small(polygons, size):
    spa_dex = Index(bbox=(-size, -size, size, size))
    areas = [poly.area for poly in polygons]
    threshold_area = max(areas)*0.05

    merged_polygons = polygons.copy()
    small_polygons = []
    for poly in polygons:
        spa_dex.insert(poly, poly.bounds)
        if poly.area < threshold_area:
            small_polygons.append(poly)

    for poly in small_polygons:
        close = spa_dex.intersect(poly.bounds)
        for close_poly in close:
            if poly is close_poly:
                continue
            else:
                if poly.touches(close_poly):
                    merged = poly.union(close_poly)

                    merged_polygons.remove(poly)
                    merged_polygons.remove(close_poly)
                    spa_dex.remove(poly, poly.bounds)
                    spa_dex.remove(close_poly, close_poly.bounds)
                    merged_polygons.append(merged)
                    spa_dex.insert(merged, merged.bounds)
                    break

    return merged_polygons

def remove_of_type(points, polygons, types, typ):
    allowed_points = []
    allowed_polygons = []
    allowed_types = []
    for index, point in enumerate(points):
        if types[index] != typ:
            allowed_points.append(point)
            allowed_polygons.append(polygons[index])
            allowed_types.append(types[index])

    return allowed_points, allowed_polygons, allowed_types

def isolate_of_type(points, types, typ):
    allowed = []
    for index, point in enumerate(points):
        if types[index] == typ:
            allowed.append(point)

    return allowed

def get_surrounded_oceans(points, types, neighbours, half, surrounded):
    remove_index = []
    for index, point in enumerate(points):
        if types[index] in half and np.random.choice([True, False]):
            remove_index.append(point)
            continue

        for neighbour in neighbours[index]:
            if types[neighbour] in surrounded:
                ocean = True
            else:
                ocean = False
                break

        if ocean:
            remove_index.append(point)

    return remove_index

def quad_grad(point, size):
    dist = np.linalg.norm(point)
    line = -1/size*dist

    return line

def radial_grad(x, y):
    pass

def get_types(points, seed, size):
    '''
    Make values a config file rather than hard-coded
    Change feature size to be a variable
    Change modes to be variable (ie. islands, continent)
    '''
    sim = OpenSimplex(seed)
    sim2 = OpenSimplex(seed+1)
    types = []
    for point in points:
        large_noise = sim.noise2d(point[0]/8192, point[1]/8192)
        small_noise = sim2.noise2d(point[0]/4092, point[1]/4092) + 0.75
        grad = quad_grad(point, size) - 0.25
        val = large_noise + small_noise + grad
        if val >= .75:
            types.append('MOUNTAIN')
        elif val >= -.25:
            pol = (1/size)*point[1]
            if pol >= .75:
                types.append('ICE')
            elif pol >= -.75:
                bio = sim.noise2d(point[0]/4092, point[1]/4092)
                if bio >= .25:
                    types.append('FOREST')
                elif bio >= -.5:
                    types.append('PLAINS')
                elif bio >= -.75:
                    types.append('DESERT')
                else:
                    types.append('PLAINS')
            else:
                types.append('ICE')
        else:
            types.append('WATER')

    return types

def relax_points(polygons):
    points = []
    for polygon in polygons:
        points.append([polygon.centroid.x, polygon.centroid.y])

    return points

def clipped_voronoi(points, size, relax = False, iterations = 1):
    if type(points) is np.ndarray:
        pass
    else:
        points = np.asarray(points)

    polygons = []
    vor = Voronoi(points)

    regions, vertices = finite_polygons(vor)
    box = Polygon([[-size, -size], [-size, size], [size, size], [size, -size]])

    for region in regions:
        polygon = vertices[region]
        poly = Polygon(polygon)
        poly = poly.intersection(box)
        polygons.append(poly)

    if relax:
        while iterations > 0:
            points = relax_points(polygons)
            polygons.clear()

            vor = Voronoi(points)
            regions, vertices = finite_polygons(vor)

            for region in regions:
                polygon = vertices[region]
                poly = Polygon(polygon)
                poly = poly.intersection(box)
                polygons.append(poly)
            iterations -= 1


    if type(points) is np.ndarray:
        points = points.tolist()
    else:
        pass

    return points, polygons

def bbox(regions, vertices, vor):
    min_x = vor.min_bound[0] - 0.1
    max_x = vor.max_bound[0] + 0.1
    min_y = vor.min_bound[1] - 0.1
    max_y = vor.max_bound[1] + 0.1

    mins = np.tile((min_x, min_y), (vertices.shape[0], 1))
    bounded_vertices = np.max((vertices, mins), axis=0)
    maxs = np.tile((max_x, max_y), (vertices.shape[0], 1))
    bounded_vertices = np.min((bounded_vertices, maxs), axis=0)

    return Polygon([[min_x, min_y], [min_x, max_y], [max_x, max_y], [max_x, min_y]])

def finite_polygons(vor, radius = None):
    """
    from https://gist.github.com/pv/8036995
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

def get_neighbours(points, polygons, size):

    '''
    Can be optimized using a spatial tree. -October7,2018
    ***Already optimized*** -October8,2018
    '''
    spa_dex = Index(bbox=(-size, -size, size, size))
    #Build Tree
    for index, point in enumerate(points):
        spa_dex.insert(point, polygons[index].bounds)

    print('Starting neighbour search')
    neighbours = [[] for _ in range(len(polygons))]
    for index, point in enumerate(points):
        closest = spa_dex.intersect(polygons[index].bounds)

        for close_point in closest:
            close_index = points.index(close_point)
            if point is close_point:
                continue
            elif polygons[index].intersects(polygons[close_index]):
                neighbours[index].append(close_index)

    return neighbours, spa_dex
