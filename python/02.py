#!/usr/bin/python3

from itertools import combinations

def part1(lines):
    two_of = 0
    three_of = 0
    for line in lines:
        counts = [0] * 26
        for c in line.rstrip():
            counts[ord(c) - 97] += 1
        if 2 in counts:
            two_of += 1
        if 3 in counts:
            three_of += 1
    print(two_of * three_of)

def part2(lines):
    for comb in combinations(lines, 2):
        num = sum(1 for a, b in zip(*comb) if a != b)
        if num == 1:
            print(''.join([a for a, b in zip(*comb) if a == b]))
            break

with open('../input/02.txt') as f:
    lines = [line.rstrip() for line in f]

part1(lines)
part2(lines)
