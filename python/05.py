#!/usr/bin/python3

import re
import sys

def react(units):
    data = units.copy()
    i = 0
    while i < (len(data) - 1):
        if abs(data[i] - data[i+1]) == 32:
            del data[i:i+2]
            i = max(i-1, 0)
        else:
            i += 1
    return len(data)

with open('../input/05.txt') as infile:
    for line in infile:
        data = [ord(char) for char in line]
        break

print('React on input data:', react(data))

for i in range(ord('A'), ord('Z')+1):
    filtered_units = (i, i+32)
    length = react([d for d in data if d not in filtered_units])
    print('{}{} =>'.format(chr(filtered_units[1]), chr(filtered_units[0])), length)
