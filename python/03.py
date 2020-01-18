#!/usr/bin/python3

import re
import sys

WIDTH = 1000
HEIGHT = 1000

def parse_claim(claim):
    m = re.match(r'^#(\d+)\s+@\s+(\d+),(\d+):\s+(\d+)x(\d+)\s*$', claim)
    if not m:
        sys.exit('Invalid claim {}'.format(claim))
    return tuple(int(value) for value in m.groups())
    
def mark_fabric(claims):
    fabric = [0] * (WIDTH * HEIGHT)
    for claim in claims:
        for x in range(claim[1], claim[1] + claim[3]):
            for y in range(claim[2], claim[2] + claim[4]):
                fabric[y * WIDTH + x] += 1        
    return fabric
    
def overlaps(fabric, claim):
    for x in range(claim[1], claim[1] + claim[3]):
        for y in range(claim[2], claim[2] + claim[4]):
            if fabric[y * WIDTH + x] > 1:
                return True
    return False

with open('../input/03.txt') as infile:
    claims = [parse_claim(line) for line in infile]

fabric = mark_fabric(claims)
overlapping = sum(1 for sqinch in fabric if sqinch > 1)
    
print("Overlapping square inches:", overlapping)

for claim in claims:
    if not overlaps(fabric, claim):
        print("Claim with no overlap:", claim[0])
