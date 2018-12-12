#!/usr/bin/python3

from itertools import cycle

with open('01_input') as inp:
    numbers = [int(line) for line in inp]

seen = set()
freq = 0

for number in cycle(numbers):
    if freq in seen:
        break
    seen.add(freq)
    freq += number

print(sum(numbers), freq)
        
