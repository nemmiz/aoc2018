#!/usr/bin/python3

import sys
import heapq


def next_move(came_from, start, goals):
    shortest_length = None
    move_to = None
    first_readorder_goal = None
    for goal in goals:
        if goal not in came_from:
            continue
        length = 0
        current = goal
        while came_from[current] != start:
            current = came_from[current]
            length += 1
        if shortest_length is None or length < shortest_length or (length == shortest_length and goal < first_readorder_goal):
            shortest_length = length
            move_to = current
            first_readorder_goal = goal
    return move_to


class Unit:
    def __init__(self, position, unit_type, attack_power):
        self.position = position
        self.attack_power = attack_power
        self.health = 200
        self.unit_type = unit_type
    def __repr__(self):
        return '<{},{},{}>'.format(self.unit_type, self.position, self.health)
    def __str__(self):
        return '{} ({})'.format(self.unit_type, self.health)


class Cave:
    def __init__(self, data, elf_attack_power):
        lines = data.split()
        width = len(lines[0])
        for line in lines:
            if len(line) != width:
                sys.exit('map data error')
        self.data = list('\n'.join(lines))
        self.width = width + 1
        self.elves = [Unit(i, 'E', elf_attack_power) for i, c in enumerate(data) if c == 'E']
        self.goblins = [Unit(i, 'G', 3) for i, c in enumerate(data) if c == 'G']
        self.full_turns = 0
    def print(self):
        print(''.join(self.data))
    def adjacent(self, position):
        return (position-self.width, position-1, position+1, position+self.width)
    def adjacent_to(self, position, target_type):
        return any((True for pos in self.adjacent(position) if self.data[pos] == target_type))
    def count_elves(self):
        return sum((1 for elf in self.elves if elf.health > 0))
    def tick(self):
        turn_order = [t for t in self.elves + self.goblins if t.health > 0]
        turn_order.sort(key=lambda unit: unit.position)
        for unit in turn_order:
            if unit.health <= 0:
                continue
            if unit.unit_type == 'E':
                targets = self.goblins
                target_type = 'G'
            else:
                targets = self.elves
                target_type = 'E'
            targets = [t for t in targets if t.health > 0]
            if not targets:
                return True
            adjacent_to_target = self.adjacent_to(unit.position, target_type)
            if not adjacent_to_target:
                move_targets = {adj for target in targets for adj in self.adjacent(target.position) if self.data[adj] == '.'}
                paths = self.find_paths(unit.position)
                move_to = next_move(paths, unit.position, move_targets)
                if move_to is not None:
                    self.data[unit.position] = '.'
                    unit.position = move_to
                    self.data[unit.position] = unit.unit_type
                    adjacent_to_target = any((True for pos in self.adjacent(unit.position) if self.data[pos] == target_type))
            if adjacent_to_target:
                lowest_health = 999
                lowest_health_target = None
                lowest_position = None
                adjacent_targets = [pos for pos in self.adjacent(unit.position) if self.data[pos] == target_type]
                for target in targets:
                    if target.position in adjacent_targets:
                        if target.health < lowest_health or (target.health == lowest_health and target.position < lowest_position):
                            lowest_health = target.health
                            lowest_health_target = target
                            lowest_position = target.position
                lowest_health_target.health -= unit.attack_power
                if lowest_health_target.health <= 0:
                    self.data[lowest_health_target.position] = '.'
        self.full_turns += 1
        return False
    def find_paths(self, start):
        open_set = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        while open_set:
            current = heapq.heappop(open_set)[1]
            for i, adj in enumerate((current-self.width, current-1, current+1, current+self.width)):
                if self.data[adj] != '.':
                    continue
                new_cost = 1 + i if current == start else cost_so_far[current] + 10
                if adj not in cost_so_far or new_cost < cost_so_far[adj]:
                    cost_so_far[adj] = new_cost
                    priority = new_cost
                    heapq.heappush(open_set, (priority, adj))
                    came_from[adj] = current
        return came_from
    def print_battle_results(self):
        total_health = sum((unit.health for unit in self.elves+self.goblins if unit.health > 0))
        print('Full turns:', self.full_turns)
        print('Total health:', total_health)
        print('Battle result:', self.full_turns * total_health)

    
def part_1(map_data):
    cave = Cave(map_data, 3)
    done = False
    while not done:
        done = cave.tick()
    cave.print_battle_results()


def part_2(map_data):
    strength = 4
    while True:
        cave = Cave(map_data, strength)
        initial_elves = cave.count_elves()
        done = False
        failed = False
        while not done:
            done = cave.tick()
            if cave.count_elves() < initial_elves:
                done = True
                failed = True
        if failed:
            strength += 1
        else:
            cave.print_battle_results()
            break


def main():
    with open('../input/15.txt') as infile:
        map_data = infile.read()

    print('Part 1:')
    part_1(map_data)

    print('\nPart 2:')
    part_2(map_data)
    

if __name__ == "__main__":
    main()