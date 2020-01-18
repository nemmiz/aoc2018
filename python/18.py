#!/usr/bin/python3


def print_map(map_data):
    for line in map_data:
        print(''.join(line))


def check_surroundings(map_data, x, y):
    width = len(map_data[0])
    height = len(map_data)
    trees = 0
    yards = 0
    for yy in range(y-1, y+2):
        for xx in range(x-1, x+2):
            if x == xx and y == yy:
                continue
            if xx < 0 or yy < 0 or xx >= width or yy >= height:
                continue
            acre = map_data[yy][xx]
            if acre == '|':
                trees += 1
            elif acre == '#':
                yards += 1
    return trees, yards


def step(map_data):
    width = len(map_data[0])
    height = len(map_data)
    new_data = []
    for y in range(height):
        line = []
        for x in range(width):
            trees, yards = check_surroundings(map_data, x, y)
            if map_data[y][x] == '.':
                line.append('|' if trees >= 3 else '.')
            elif map_data[y][x] == '|':
                line.append('#' if yards >= 3 else '|')
            elif map_data[y][x] == '#':
                line.append('.' if trees < 1 or yards < 1 else '#')
        new_data.append(line)
    return new_data


def resource_value(map_data):
    trees = 0
    yards = 0
    for line in map_data:
        for c in line:
            if c == '|':
                trees += 1
            elif c == '#':
                yards += 1
    return trees * yards


def find_cycle(samples):
    i = len(samples) - 2
    last_sample = samples[-1]
    while i >= 0:
        if samples[i] == last_sample:
            break
        i -= 1
    if i == -1:
        return None
    cycle = len(samples) - i - 1
    for i in range(cycle):
        a = -1 - i
        b = a - cycle
        c = b - cycle
        if not (samples[a] == samples[b] == samples[c]):
            return None
    return cycle


def simulate(map_data, times, cycle_threshold=500):
    cycle_check_interval = 100
    samples = []
    for i in range(times):
        map_data = step(map_data)
        samples.append(resource_value(map_data))
        if i >= cycle_threshold:
            if i % cycle_check_interval == 0:
                cycle = find_cycle(samples)
                if cycle:
                    print(samples[i-cycle+((times-i)%cycle)-1])
                    return
    print(resource_value(map_data))


def main():
    with open('../input/18.txt') as infile:
        map_data = [list(line.rstrip('\n')) for line in infile]

    simulate(map_data, 10)
    simulate(map_data, 1000000000)


if __name__ == "__main__":
    main()