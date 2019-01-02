#!/usr/bin/python3

import heapq


class Region:
    def __init__(self, coord, geologic_index, erosion_level):
        self.coord = coord
        self.geologic_index = geologic_index
        self.erosion_level = erosion_level
        self.region_type = erosion_level % 3
        self.allowed_tools = ['TC', 'CN', 'TN'][self.region_type]


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.regions = {}

    def get_region(self, coord):
        if coord not in self.regions:
            if coord == (0, 0) or coord == self.target:
                geo = 0
            elif coord[1] == 0:
                geo = coord[0] * 16807
            elif coord[0] == 0:
                geo = coord[1] * 48271
            else:
                w_region = self.get_region((coord[0]-1, coord[1]))
                n_region = self.get_region((coord[0], coord[1]-1))
                geo = w_region.erosion_level * n_region.erosion_level
            ero = (geo + self.depth) % 20183
            self.regions[coord] = Region(coord, geo, ero)
        return self.regions[coord]
        
    def risk_value(self):
        result = 0
        for y in range(self.target[1]+1):
            for x in range(self.target[0]+1):
                region = self.get_region((x, y))
                result += region.region_type
        return result

    def moves(self, tool_coord):
        region = self.get_region(tool_coord[1])
        for allowed in region.allowed_tools.replace(tool_coord[0], ''):
            yield ((allowed, region.coord), 7)
        x, y = region.coord
        if y > 0:
            coord = (x, y-1)
            next_region = self.get_region(coord)
            if tool_coord[0] in next_region.allowed_tools:
                yield ((tool_coord[0], coord), 1)
        if x > 0:
            coord = (x-1, y)
            next_region = self.get_region(coord)
            if tool_coord[0] in next_region.allowed_tools:
                yield ((tool_coord[0], coord), 1)
        coord = (x+1, y)
        next_region = self.get_region(coord)
        if tool_coord[0] in next_region.allowed_tools:
            yield ((tool_coord[0], coord), 1)
        coord = (x, y+1)
        next_region = self.get_region(coord)
        if tool_coord[0] in next_region.allowed_tools:
            yield ((tool_coord[0], coord), 1)

    def distance_to_target(self):
        startpoint = ('T', (0,0))
        endpoint = ('T', self.target)
        open_set = [(0, startpoint)]
        came_from = {startpoint: None}
        cost_so_far = {startpoint: 0}
        while open_set:
            current = heapq.heappop(open_set)[1]
            for next_coord, next_cost in self.moves(current):
                new_cost = cost_so_far[current] + next_cost
                if endpoint in cost_so_far and new_cost > cost_so_far[endpoint]:
                    continue
                if next_coord not in cost_so_far or new_cost < cost_so_far[next_coord]:
                    cost_so_far[next_coord] = new_cost
                    priority = new_cost
                    heapq.heappush(open_set, (priority, next_coord))
                    came_from[next_coord] = current
        return cost_so_far[endpoint]


def main():
    test_cave = Cave(510, (10, 10))
    assert 114 == test_cave.risk_value()
    assert  45 == test_cave.distance_to_target()

    cave = Cave(7740, (12, 763))
    print(cave.risk_value())
    print(cave.distance_to_target())
    

if __name__ == "__main__":
    main()