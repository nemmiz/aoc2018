#!/usr/bin/python3

import re


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


def main():
    iptr_reg = 0
    instructions = []

    with open('../input/21.txt') as infile:
        for line in infile:
            m = re.match('^#ip (\d+)\s*$', line)
            if m:
                iptr_reg = int(m.group(1))
                continue
            m = re.match('^(\w{4}) (\d+) (\d+) (\d+)\s*$', line)
            if m:
                instructions.append((m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))))
                continue

    iptr = 0
    regs = [0, 0, 0, 0, 0, 0]
    exit_values = set()
    last_added = None
    try:
        while True:
            # The code exits when regs[0] == regs[3] at instruction 28.
            # The lower bound is regs[3] when instruction 28 is first reached.
            # Upper bound is the last value of regs[3] before the values start repeating.
            if iptr == 28:
                if not exit_values:
                    print('Lower bound:', regs[3])
                if regs[3] in exit_values:
                    print('Upper bound:', last_added)
                    break
                else:
                    exit_values.add(regs[3])
                    last_added = regs[3]
            regs[iptr_reg] = iptr
            inst = instructions[iptr]
            OPCODES[inst[0]](regs, inst)
            iptr = regs[iptr_reg] + 1
    except IndexError:
        pass
    

if __name__ == "__main__":
    main()