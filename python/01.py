#!/usr/bin/python3

from itertools import cycle

with open('../input/01.txt') as f:
    numbers = [int(line) for line in f]

seen = set()
freq = 0

for number in cycle(numbers):
    if freq in seen:
        break
    seen.add(freq)
    freq += number

print(sum(numbers), freq, sep='\n')        
