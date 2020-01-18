#!/usr/bin/python3

import re


def calculate(data, index, metadata_sum):
    num_children = data[index]
    num_metadata = data[index+1]
    index += 2
    node_value = 0

    if num_children > 0:
        child_values = []
        for i in range(num_children):
            index, metadata_sum, value = calculate(data, index, metadata_sum)
            child_values.append(value)

    for i in range(num_metadata):
        entry = data[index+i]
        metadata_sum += entry
        if num_children > 0:
            if entry >= 1 and entry <= len(child_values):
                node_value += child_values[entry-1]
        else:
            node_value += entry

    return (index + num_metadata, metadata_sum, node_value)


def main():
    with open('../input/08.txt') as infile:
        for line in infile:
            numbers = [int(x.group(0)) for x in re.finditer(r'\d+', line)]
            break

    index, metasum, value = calculate(numbers, 0, 0)
    print(metasum)
    print(value)

if __name__ == "__main__":
    main()
