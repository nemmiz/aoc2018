#!/usr/bin/python3

import io
import sys
import heapq
from collections import namedtuple


# DIR: (index, opposite, x_dir, y_dir)
DIRECTIONS = {
    'N': (0, 1,  0, -1),
    'S': (1, 0,  0,  1),
    'W': (2, 3, -1,  0),
    'E': (3, 2,  1, -0),
}


class Area:
    class Room:
        def __init__(self, position):
            self.neighbors = [None, None, None, None]
            self.position = position
            self.distance = 0

    def __init__(self):
        self.first_room = Area.Room((0,0))
        self.rooms = [self.first_room]
        self.rooms_lookup = {(0,0): self.first_room}

    def add_path(self, x, y, path):
        current_room = self.rooms_lookup[(x,y)]
        for c in path:
            index, opposite, xdir, ydir = DIRECTIONS[c]
            next_room_coord = (x+xdir, y+ydir)
            next_room = self.rooms_lookup.get(next_room_coord)
            if not next_room:
                next_room = Area.Room(next_room_coord)
                self.rooms.append(next_room)
                self.rooms_lookup[next_room_coord] = next_room
            next_room.neighbors[opposite] = current_room
            current_room.neighbors[index] = next_room
            x += xdir
            y += ydir
            current_room = next_room
        return (x, y)

    def print(self):
        minx = 0
        miny = 0
        maxx = 0
        maxy = 0
        for room in self.rooms:
            minx = min(minx, room.position[0])
            maxx = max(maxx, room.position[0])
            miny = min(miny, room.position[1])
            maxy = max(maxy, room.position[1])
        width = maxx - minx + 1
        height = maxy - miny + 1
        line_width = width * 2 + 2
        line_count = height * 2 + 1
        map_data = ['\n' if (i%line_width)==(line_width-1) else ' ' for i in range(line_width*line_count)]
        for room in self.rooms:
            x = room.position[0] - minx
            y = room.position[1] - miny
            pos = (x*2+1)+(y*2+1)*line_width
            map_data[pos] = 'X' if room is self.first_room else '.'
            map_data[pos-line_width] = '#' if room.neighbors[0] is None else '-'
            map_data[pos+line_width] = '#' if room.neighbors[1] is None else '-'
            map_data[pos-1] = '#' if room.neighbors[2] is None else '|'
            map_data[pos+1] = '#' if room.neighbors[3] is None else '|'
            map_data[pos-line_width-1] = '#'
            map_data[pos-line_width+1] = '#'
            map_data[pos+line_width-1] = '#'
            map_data[pos+line_width+1] = '#'
        print(''.join(map_data))

    def find_paths(self):
        open_set = [(0, (0,0))]
        came_from = {(0,0): None}
        cost_so_far = {(0,0): 0}
        max_cost = 0
        while open_set:
            current = heapq.heappop(open_set)[1]
            current_room = self.rooms_lookup[current]
            for neighbor in current_room.neighbors:
                if neighbor:
                    new_cost = cost_so_far[current] + 1
                    if neighbor.position not in cost_so_far or new_cost < cost_so_far[neighbor.position]:
                        cost_so_far[neighbor.position] = new_cost
                        priority = new_cost
                        max_cost = max(max_cost, new_cost)
                        heapq.heappush(open_set, (priority, neighbor.position))
                        came_from[neighbor.position] = current
        rooms_ge_1000 = 0
        for room in self.rooms:
            steps = 0
            current = room.position
            while current != (0,0):
                current = came_from[current]
                steps += 1
            if steps >= 1000:
                rooms_ge_1000 += 1
            room.distance = steps

    def max_room_distance(self):
        max_distance = 0
        for room in self.rooms:
            max_distance = max(max_distance, room.distance)
        return max_distance

    def count_faraway_rooms(self, distance):
        return sum((1 for room in self.rooms if room.distance >= distance))


def loops_back(path):
    x, y = 0, 0
    for c in path:
        _, _, xdir, ydir = DIRECTIONS[c]
        x += xdir
        y += ydir
    return (x == 0 and y == 0)
            

def optimize_choice(choice):
    """Joins path choices that loop back to the original position, e.g. '^(NS|EW)$' => '^NSEW$'"""
    for option in choice:
        if len(option) != 1 or not loops_back(option[0]):
            break
    else:
        return ''.join([option[0] for option in choice])
    return tuple(choice)


def optimize_strlist(strlist):
    """Joins any adjecent strings in a list, e.g. ['N', 'S'] => ['NS']"""
    result = []
    for s in strlist:
        if result and isinstance(s, str) and isinstance(result[-1], str):
            result[-1] = result[-1] + s
        else:
            result.append(s)
    if len(result) > 1 and result[-1] == '':
        result.pop()
    return result


def tokenize(stream, depth):
    mnl = []
    nl = []
    text = []
    c = None
    while True:
        prev = c
        c = stream.read(1)
        if c in 'NSEW':
            text.append(c)
        elif c == '(':
            if text:
                nl.append(''.join(text))
                text = []
            nl.append(optimize_choice(tokenize(stream, depth+1)))
        elif c == ')':
            if text:
                nl.append(''.join(text))
            elif prev == '|':
                nl.append('')
            mnl.append(optimize_strlist(nl))
            break
        elif c == '|':
            nl.append(''.join(text))
            text = []
            mnl.append(optimize_strlist(nl))
            nl = []
        elif c == '$' and depth == 0:
            if text:
                nl.append(''.join(text))
            break
        else:
            sys.exit('parse error')
    if depth == 0:
        return optimize_strlist(nl)
    return optimize_strlist(mnl)


def parse(regex):
    stream = io.StringIO(regex)
    assert stream.read(1) == '^', 'regex must begin with a caret'
    nodes = build_nodes(tokenize(stream, 0), None)
    area = Area()
    create_paths(area, 0, 0, nodes)
    area.find_paths()
    return area


def create_paths(area, x, y, node):
    for n in iterate(node):
        if isinstance(n, TextNode):
            x, y = area.add_path(x, y, node.text)
        elif isinstance(n, ChoiceNode):
            for child in n.children:
                create_paths(area, x, y, child)
            return


TextNode = namedtuple('TextNode', ['text', 'parent_node', 'next_node'])
ChoiceNode = namedtuple('ChoiceNode', ['parent_node', 'next_node', 'children'])


def iterate(node):
    while node:
        yield node
        while node and not node.next_node:
            node = node.parent_node
        if node is not None:
            node = node.next_node


def build_nodes(node_list, parent):
    nodes = None
    for node in reversed(node_list):
        if isinstance(node, str):
            nodes = TextNode(node, parent, nodes)
        elif isinstance(node, tuple):
            nodes = ChoiceNode(parent, nodes, [build_nodes(child, nodes) for child in node])
    return nodes


def main():
    assert 3  == parse("^WNE$").max_room_distance()
    assert 10 == parse("^ENWWW(NEEE|SSE(EE|N))$").max_room_distance()
    assert 18 == parse("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$").max_room_distance()
    assert 23 == parse("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$").max_room_distance()
    assert 31 == parse("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$").max_room_distance()

    with open('../input/20.txt') as infile:
        regex = infile.read()
        area = parse(regex)
        print(area.max_room_distance())
        print(area.count_faraway_rooms(1000))


if __name__ == "__main__":
    main()