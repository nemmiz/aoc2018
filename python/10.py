#!/usr/bin/python3

import re
import sys

class Points:
    def __init__(self):
        self.xpos = []
        self.ypos = []
        self.xvel = []
        self.yvel = []
        self.num_points = 0
        self.time = 0
        self.bounds = [0, 0, 0, 0]
    def append(self, x, y, dx, dy):
        self.xpos.append(x)
        self.ypos.append(y)
        self.xvel.append(dx)
        self.yvel.append(dy)
        self.num_points += 1
    def calculate_bounds(self):
        self.bounds[0] = min(self.xpos)
        self.bounds[1] = min(self.ypos)
        self.bounds[2] = max(self.xpos)
        self.bounds[3] = max(self.ypos)
    def move(self):
        for i in range(self.num_points):
            self.xpos[i] += self.xvel[i]
            self.ypos[i] += self.yvel[i]
        self.time += 1
        self.calculate_bounds()
    def move_back(self):
        for i in range(self.num_points):
            self.xpos[i] -= self.xvel[i]
            self.ypos[i] -= self.yvel[i]
        self.time -= 1
        self.calculate_bounds()
    def bounds_area(self):
        width = self.bounds[2] - self.bounds[0] + 1
        height = self.bounds[3] - self.bounds[1] + 1
        return width * height
    def visualize(self):
        width = self.bounds[2] - self.bounds[0] + 1
        height = self.bounds[3] - self.bounds[1] + 1
        pixels = [' '] * (width * height)
        for i in range(self.num_points):
            x = self.xpos[i] - self.bounds[0]
            y = self.ypos[i] - self.bounds[1]
            pixels[y * width + x] = '#'
        for i in range(0, len(pixels), width):
            print(''.join(pixels[i:i+width]))


def main():
    points = Points()
    
    with open('../input/10.txt') as infile:
        for line in infile:
            m = re.match(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>', line)
            if not m:
                sys.exit('input error')
            points.append(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))

    points.move_back()
    old_area = points.bounds_area()

    points.move()
    new_area = points.bounds_area()

    initial_growth_direction = new_area > old_area
    growth_direction = initial_growth_direction

    while growth_direction == initial_growth_direction:
        old_area = new_area
        points.move()
        new_area = points.bounds_area()
        growth_direction = new_area > old_area
    
    points.move_back()
    points.visualize()
    print('Time taken:', points.time, 'seconds')


if __name__ == "__main__":
    main()
