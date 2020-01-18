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


def incf(regs, inst):
    """incf (increase factor)
    Increases the value in register C until reg[A] * reg[C] = reg[B].
    If the value in register C is less than the value in register B
    but the condition cannot be met, reg[C] will be set to reg[B].
    If the value in register C is greater than the value in register B
    it will only be increased once.
    """
    if (regs[inst[1]] * regs[inst[3]]) < regs[inst[2]]:
        q, r = divmod(regs[inst[2]], regs[inst[1]])
        if r == 0:
            regs[inst[3]] = q
        else:
            regs[inst[3]] += max(1, regs[inst[2]]-regs[inst[3]])
    else:
        regs[inst[3]] += max(1, regs[inst[2]]-regs[inst[3]])


def incd(regs, inst):
    """incd (increase until divisible)
    Increases the value in register C until the value in register A is
    evenly divisible by it. If the value in register A cannot be evenly
    divided, or if the reg[C] > reg[A], the value in register C will
    only be increased once."""
    v = regs[inst[3]] + 1
    p = regs[inst[1]]
    if v < p:
        while p % v != 0:
            v += 1
    regs[inst[3]] = v


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
    'incf': incf,
    'incd': incd,
}


def main():
    iptr_reg = 0
    instructions = []

    with open('../input/19.txt') as infile:
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
    try:
        while True:
            regs[iptr_reg] = iptr
            inst = instructions[iptr]
            OPCODES[inst[0]](regs, inst)
            iptr = regs[iptr_reg] + 1
    except IndexError:
        pass
    print(regs[0])

    iptr = 0
    regs = [1, 0, 0, 0, 0, 0]
    instructions[8] = ('incf', 3, 1, 5)
    instructions[12] = ('incd', 1, 0, 3)
    try:
        while True:
            regs[iptr_reg] = iptr
            inst = instructions[iptr]
            OPCODES[inst[0]](regs, inst)
            iptr = regs[iptr_reg] + 1
    except IndexError:
        pass
    print(regs[0])
    

if __name__ == "__main__":
    main()