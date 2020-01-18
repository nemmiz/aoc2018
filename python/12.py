#!/usr/bin/python3

import io


class Pots:
    def __init__(self, initial, rules):
        self.first_index = 0
        self.data = bytearray()

        while len(initial) % 8 != 0:
            initial = initial + '.'

        initial = initial.replace('#', '1').replace('.', '0')
        for i in range(0, len(initial), 8):
            self.data.append(int(initial[i:i+8], 2))
        self.adjust_size()

        self.rules = []
        for i in range(4096):
            byte = rules[(i >> 7) & 31]
            byte = (byte << 1) | rules[(i >> 6) & 31]
            byte = (byte << 1) | rules[(i >> 5) & 31]
            byte = (byte << 1) | rules[(i >> 4) & 31]
            byte = (byte << 1) | rules[(i >> 3) & 31]
            byte = (byte << 1) | rules[(i >> 2) & 31]
            byte = (byte << 1) | rules[(i >> 1) & 31]
            byte = (byte << 1) | rules[i & 31]
            self.rules.append(byte)

    def adjust_size(self):
        if self.data[0] == 0:
            if self.data[1] == 0:
                del self.data[0]
                self.first_index += 8
        else:
            self.data.insert(0, 0)
            self.first_index -= 8
        if self.data[-1] == 0:
            if self.data[-2] == 0:
                del self.data[-1]
        else:
            self.data.append(0)
        
    def print(self):
        buf = io.StringIO()
        for b in self.data:
            buf.write('{:08b}'.format(b))
        print(self.first_index, buf.getvalue())

    def process(self):
        rule_index = 0
        data = self.data
        rules = self.rules

        rule_index = (data[0] << 2 | data[1] >> 6)
        data[0] = rules[rule_index]

        for i in range(1, len(data)-1):
            rule_index = ((rule_index & 0b1100) << 8) | (data[i] << 2) | (data[i+1] >> 6)
            data[i] = rules[rule_index]

        rule_index = ((rule_index & 0b1100) << 8) | (data[-1] << 2)
        data[-1] = rules[rule_index]
        self.adjust_size()

    def pots_sum(self):
        result = 0
        for i, b in enumerate(self.data):
            for bit in range(8):
                if (b >> (7 - bit)) & 1:
                    result += (self.first_index + i*8 + bit)
        return result


def main():
    rules = [0] * 32
    with open('../input/12.txt') as infile:
        for i, line in enumerate(infile):
            if i == 0:
                initial_state = line[15:-1]
            elif i >= 2:
                line = line.replace('#', '1').replace('.', '0')
                key = int(line[0:5], 2)
                value = int(line[9], 2)
                rules[key] = value

    pots = Pots(initial_state, rules)
    for i in range(20):
        pots.process()
    print(pots.pots_sum())

    # For the second task (50 billion generations) there's a recurring pattern
    # for values 5*10^N where N >= 3. In my input, the value grows like:
    #    500 => 21684
    #   5000 => 201684
    #  50000 => 2001684
    # 500000 => 20001684
    # ...and so on. So a dirty solution to get to 50 billion is to take the
    # result for 500 and insert the zeros
    # pattern for 5000, 50000, 500000, etc. and go from there.
    pots = Pots(initial_state, rules)
    for i in range(500):
        pots.process()
    tmp = str(pots.pots_sum())
    print(tmp[:1]+'00000000'+tmp[1:])


if __name__ == "__main__":
    main()
