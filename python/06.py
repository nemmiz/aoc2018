#!/usr/bin/python3

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def closest_distance(xcoords, ycoords, x, y):
    n = len(xcoords)
    best_distance = manhattan(xcoords[0], ycoords[0], x, y)
    for i in range(1, n):
        distance = manhattan(xcoords[i], ycoords[i], x, y)
        if distance < best_distance:
            best_distance = distance
    return best_distance


def closest_exclusive_point(xcoords, ycoords, x, y):
    point_id = None
    distance = closest_distance(xcoords, ycoords, x, y)
    for i, point in enumerate(zip(xcoords, ycoords)):
        if manhattan(x, y, point[0], point[1]) == distance:
            if point_id is None:
                point_id = i
            else:
                return None
    return point_id


def total_distance_less_than(xcoords, ycoords, x, y, n):
    total_distance = 0
    for pt in zip(xcoords, ycoords):
        total_distance += manhattan(pt[0], pt[1], x, y)
        if total_distance > n:
            return False
    return True


def main():
    xcoords = []
    ycoords = []

    with open('../input/06.txt') as infile:
        for line in infile:
            strx, stry = line.split(',')
            xcoords.append(int(strx))
            ycoords.append(int(stry))

    minx = min(xcoords)
    maxx = max(xcoords)
    miny = min(ycoords)
    maxy = max(ycoords)

    infinite = set()
    for x in range(minx, maxx+1):
        infinite.add(closest_exclusive_point(xcoords, ycoords, x, miny))
        infinite.add(closest_exclusive_point(xcoords, ycoords, x, maxy))
    for y in range(miny+1, maxy):
        infinite.add(closest_exclusive_point(xcoords, ycoords, minx, y))
        infinite.add(closest_exclusive_point(xcoords, ycoords, maxx, y))
        
    areas = [0] * len(xcoords)
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            point_id = closest_exclusive_point(xcoords, ycoords, x, y)
            if point_id is not None:
                areas[point_id] += 1

    finite_areas = [area for i, area in enumerate(areas) if i not in infinite]
    print('The largest finite area is:', max(finite_areas))

    safe_region_size = 0
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            if total_distance_less_than(xcoords, ycoords, x, y, 10000):
                safe_region_size += 1

    print('The safe region size is:', safe_region_size)


if __name__ == "__main__":
    main()
