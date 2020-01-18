#!/usr/bin/python3


import re
import sys


def addr(regs, inst): 
    regs[inst[3]] = regs[inst[1]] + regs[inst[2]]
def addi(regs, inst):
    regs[inst[3]] = regs[inst[1]] + inst[2]
def mulr(regs, inst):
    regs[inst[3]] = regs[inst[1]] * regs[inst[2]]
def muli(regs, inst):
    regs[inst[3]] = regs[inst[1]] * inst[2]
def banr(regs, inst):
    regs[inst[3]] = regs[inst[1]] & regs[inst[2]]
def bani(regs, inst):
    regs[inst[3]] = regs[inst[1]] & inst[2]
def borr(regs, inst):
    regs[inst[3]] = regs[inst[1]] | regs[inst[2]]
def bori(regs, inst):
    regs[inst[3]] = regs[inst[1]] | inst[2]
def setr(regs, inst):
    regs[inst[3]] = regs[inst[1]]
def seti(regs, inst):
    regs[inst[3]] = inst[1]
def gtir(regs, inst):
    regs[inst[3]] = 1 if inst[1] > regs[inst[2]] else 0
def gtri(regs, inst):
    regs[inst[3]] = 1 if regs[inst[1]] > inst[2] else 0
def gtrr(regs, inst):
    regs[inst[3]] = 1 if regs[inst[1]] > regs[inst[2]] else 0
def eqir(regs, inst):
    regs[inst[3]] = 1 if inst[1] == regs[inst[2]] else 0
def eqri(regs, inst):
    regs[inst[3]] = 1 if regs[inst[1]] == inst[2] else 0
def eqrr(regs, inst):
    regs[inst[3]] = 1 if regs[inst[1]] == regs[inst[2]] else 0


OPCODES = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr,
}


def task_1(befores, afters, instructions):
    at_least_3_matches = 0
    for before, after, inst in zip(befores, afters, instructions):
        matches = 0
        for opcode, opcode_function in OPCODES.items():
            regs = before.copy()
            opcode_function(regs, inst)
            if regs == after:
                matches += 1
        if matches >= 3:
            at_least_3_matches += 1
    print(at_least_3_matches)


def task_2(befores, afters, instructions):
    possible_numbers = {}
    for before, after, inst in zip(befores, afters, instructions):
        for opcode, opcode_function in OPCODES.items():
            regs = before.copy()
            opcode_function(regs, inst)
            if regs == after:
                opcode_number = inst[0]
                if opcode in possible_numbers:
                    possible_numbers[opcode].add(opcode_number)
                else:
                    possible_numbers[opcode] = {opcode_number}
    opcode_numbers = {}
    while possible_numbers:
        for op, nums in possible_numbers.items():
            if len(nums) == 1:
                opcode, number = op, nums.pop()
                break
        opcode_numbers[number] = opcode
        del possible_numbers[opcode]
        for nums in possible_numbers.values():
            nums.discard(number)
    regs = [0, 0, 0, 0]
    for inst in instructions[len(befores):]:
        OPCODES[opcode_numbers[inst[0]]](regs, inst)
    print(regs[0])


def main():
    befores = []
    afters = []
    instructions = []

    with open('../input/16.txt') as infile:
        for line in infile:
            m = re.match('^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$', line)
            if m:
                instructions.append(tuple(map(int, m.group(1, 2, 3, 4))))
                continue
            m = re.match('^Before:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]\s*$', line)
            if m:
                befores.append(list(map(int, m.group(1, 2, 3, 4))))
                continue
            m = re.match('^After:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]\s*$', line)
            if m:
                afters.append(list(map(int, m.group(1, 2, 3, 4))))
                continue
    
    task_1(befores, afters, instructions)
    task_2(befores, afters, instructions)
    

if __name__ == "__main__":
    main()