#!/usr/bin/python3


import re


class ScanMap:
    def __init__(self, filename):
        self.minx = 9999999
        self.miny = 9999999
        self.maxx = -9999999
        self.maxy = -9999999
        hstrips = []
        vstrips = []

        with open(filename) as infile:
            for line in infile:
                m = re.match('^x=(\d+), y=(\d+)\.\.(\d+)\s*$', line)
                if m:
                    x = int(m.group(1))
                    y_first = int(m.group(2))
                    y_last = int(m.group(3))
                    self.minx = min(self.minx, x)
                    self.maxx = max(self.maxx, x)
                    self.miny = min(self.miny, y_first)
                    self.maxy = max(self.maxy, y_last)
                    vstrips.append((x, y_first, y_last))
                    continue
                m = re.match('^y=(\d+), x=(\d+)\.\.(\d+)\s*$', line)
                if m:
                    y = int(m.group(1))
                    x_first = int(m.group(2))
                    x_last = int(m.group(3))
                    self.minx = min(self.minx, x_first)
                    self.maxx = max(self.maxx, x_last)
                    self.miny = min(self.miny, y)
                    self.maxy = max(self.maxy, y)
                    hstrips.append((y, x_first, x_last))
                    continue

        self.not_counted = self.miny-1 if self.miny > 1 else 0
        self.minx = min(self.minx, 500) - 1
        self.maxx = max(self.maxx, 500) + 1
        self.miny = min(self.miny, 1)
        self.maxy = max(self.maxy, 1)
        self.width = self.maxx - self.minx + 1
        self.height = self.maxy - self.miny + 1    
        self.data = [['.']*self.width for _ in range(self.height)]

        for strip in hstrips:
            y = strip[0] - self.miny
            for x in range(strip[1]-self.minx, strip[2]-self.minx+1):
                self.data[y][x] = '#'
        for strip in vstrips:
            x = strip[0] - self.minx
            for y in range(strip[1]-self.miny, strip[2]-self.miny+1):
                self.data[y][x] = '#'

    def print_map(self):
        for line in self.data:
            print(''.join(line))

    def write_map(self, filename):
        with open(filename, 'w') as outfile:
            for line in self.data:
                outfile.write(''.join(line))
                outfile.write('\n')

    def simulate(self):
        self.pour(500-self.minx, -1)
        running_water = -self.not_counted
        still_water = 0
        for line in self.data:
            for c in line:
                if c == '~':
                    still_water += 1
                elif c == '|':
                    running_water += 1
        print(still_water + running_water)
        print(still_water)

    def pour(self, x, y):
        while True:
            if (y+1) >= self.height:
                return
            below = self.data[y+1][x]
            if below == '#' or below == '~':
                break
            elif below == '|':
                return
            self.data[y+1][x] = '|'
            y += 1
        mid = x
        while True:
            left_blocked = False
            x = mid - 1
            while True:
                assert(x >= 0)
                if self.data[y][x] == '#':
                    left_blocked = True
                    break
                elif self.data[y+1][x] in '.|':
                    break
                x -= 1
            left_x = x
            right_blocked = False
            x = mid + 1
            while True:
                assert(x < self.width)
                if self.data[y][x] == '#':
                    right_blocked = True
                    break
                elif self.data[y+1][x] in '.|':
                    break
                x += 1
            right_x = x
            if left_blocked and right_blocked:
                for x in range(left_x+1, right_x):
                    self.data[y][x] = '~'
                y -= 1
            elif left_blocked:
                for x in range(left_x+1, right_x+1):
                    self.data[y][x] = '|'
                self.pour(right_x, y)
                break
            elif right_blocked:
                for x in range(left_x, right_x):
                    self.data[y][x] = '|'
                self.pour(left_x, y)
                break
            else:
                for x in range(left_x, right_x+1):
                    self.data[y][x] = '|'
                self.pour(left_x, y)
                self.pour(right_x, y)
                break


def main():
    scan_map = ScanMap('../input/17.txt')
    scan_map.simulate()


if __name__ == "__main__":
    main()