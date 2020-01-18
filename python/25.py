#!/usr/bin/python3


def manhattan_distance(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])+abs(a[3]-b[3])


def count_constellations(coords):
    num = 0
    src = coords
    while src:
        prev_size = 0
        constellation = [src.pop()]
        while len(constellation) != prev_size:
            prev_size = len(constellation)
            new_src = []
            for coord1 in src:
                for coord2 in constellation:
                    if manhattan_distance(coord1, coord2) <= 3:
                        constellation.append(coord1)
                        break
                else:
                    new_src.append(coord1)
            src = new_src
        num += 1
    return num


def main():
    with open('../input/25.txt') as infile:
        coords = [tuple(map(int, line.strip().split(','))) for line in infile]
        print(count_constellations(coords))


if __name__ == "__main__":
    main()
