#!/usr/bin/python3

import re
import io
import sys


def distance(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

def intersects(a, b):
    return (abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])) <= (a[3]+b[3])


class BoundingBox:
    def __init__(self):
        self.minx = None
        self.miny = None
        self.minz = None
        self.maxx = None
        self.maxy = None
        self.maxz = None
    def calculate_bounds(self, nanobots):
        self.minx, self.miny, self.minz = nanobots[0][:3]
        self.maxx, self.maxy, self.maxz = nanobots[0][:3]
        for nanobot in nanobots:
            self.minx = min(self.minx, nanobot[0]-nanobot[3])
            self.miny = min(self.miny, nanobot[1]-nanobot[3])
            self.minz = min(self.minz, nanobot[2]-nanobot[3])
            self.maxx = max(self.maxx, nanobot[0]+nanobot[3])
            self.maxy = max(self.maxy, nanobot[1]+nanobot[3])
            self.maxz = max(self.maxz, nanobot[2]+nanobot[3])
    def copy(self):
        ret = BoundingBox()
        ret.minx = self.minx
        ret.miny = self.miny
        ret.minz = self.minz
        ret.maxx = self.maxx
        ret.maxy = self.maxy
        ret.maxz = self.maxz
        return ret
    def print(self):
        print('Box=<({},{},{}),({},{},{})>'.format(self.minx, self.miny, self.minz, self.maxx, self.maxy, self.maxz))
    def split(self):
        w = self.maxx - self.minx
        h = self.maxy - self.miny
        d = self.maxz - self.minz
        largest = max(w, h, d)
        if w == largest:
            a = self.copy()
            a.maxx = self.minx + w//2
            b = self.copy()
            b.minx = self.minx + w//2 + 1
        elif h == largest:
            a = self.copy()
            a.maxy = self.miny + h//2
            b = self.copy()
            b.miny = self.miny + h//2 + 1
        elif d == largest:
            a = self.copy()
            a.maxz = self.minz + d//2
            b = self.copy()
            b.minz = self.minz + d//2 + 1
        return a, b
    def collides_with(self, nanobot):
        cx, cy, cz = nanobot[:3]
        cx = max(min(cx, self.maxx), self.minx)
        cy = max(min(cy, self.maxy), self.miny)
        cz = max(min(cz, self.maxz), self.minz)
        return intersects((cx, cy, cz, 0), nanobot)
    def size(self):
        w = self.maxx - self.minx + 1
        h = self.maxy - self.miny + 1
        d = self.maxz - self.minz + 1
        return w * h * d


def check_box(box, nanobots, result):
    n = len(nanobots)
    if n < result[0]:
        return
    if box.size() == 1:
        if n > result[0]:
            result[0] = n
            result[1] = distance((0,0,0), (box.minx,box.miny,box.minz))
        elif n == result[0]:
            dist = distance((0,0,0), (box.minx,box.miny,box.minz))
            if result[1] is None or dist < result[1]:
                result[1] = dist
    else:
        a, b = box.split()
        check_box(a, [nb for nb in nanobots if a.collides_with(nb)], result)
        check_box(b, [nb for nb in nanobots if b.collides_with(nb)], result)


def distance_to_best_coord(box, nanobots):
    initial_guess = max(len(nanobots)-30, 0)
    result = [initial_guess, None]
    check_box(box, nanobots, result)
    return result[1]


def main():
    nanobots = []

    with open('../input/23.txt') as infile:
        for line in infile:
            m = re.match('^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)\s*$', line)
            assert m
            nanobots.append(tuple(map(int, m.groups())))

    nanobots.sort(key=lambda nb: nb[3], reverse=True)
    print(sum((1 for nanobot in nanobots if distance(nanobots[0], nanobot) <= nanobots[0][3])))

    box = BoundingBox()
    box.calculate_bounds(nanobots)
    print(distance_to_best_coord(box, nanobots))
    

if __name__ == "__main__":
    main()