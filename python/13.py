#!/usr/bin/python3

import sys


CURVE_FSLASH = {'<': 'v', '>': '^', '^': '>', 'v': '<'}
CURVE_BSLASH = {'<': '^', '>': 'v', '^': '<', 'v': '>'}
INTERSECTION_LEFT  = {'<': 'v', '>': '^', '^': '<', 'v': '>'}
INTERSECTION_RIGHT = {'<': '^', '>': 'v', '^': '>', 'v': '<'}


class Cart:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.track = '-' if direction in '<>' else '|'
        self.intersection_dir = 0
        self.crashed = False
    def print(self):
        print(self.position, self.direction, self.track)


class TrackSystem:
    def __init__(self, track_map, track_width):
        self.track_map = track_map
        self.track_width = track_width
        self.cart_positions = set()
        self.carts = []
        for i, c in enumerate(track_map):
            if c in '<>^v':
                self.cart_positions.add(i)
                self.carts.append(Cart(i, c))
    def move_carts(self, remove_collided=False):
        self.carts.sort(key=lambda cart: cart.position)
        remove_crashed_carts = False
        for cart in self.carts:
            if cart.crashed:
                continue
            old_pos = cart.position
            if cart.direction == '<':
                new_pos = old_pos - 1
            elif cart.direction == '>':
                new_pos = old_pos + 1
            elif cart.direction == '^':
                new_pos = old_pos - self.track_width
            elif cart.direction == 'v':
                new_pos = old_pos + self.track_width
            self.cart_positions.remove(old_pos)
            self.track_map[old_pos] = cart.track
            if new_pos not in self.cart_positions:
                cart.position = new_pos
                self.cart_positions.add(new_pos)
                cart.track = self.track_map[new_pos]
                if cart.track == '+':
                    if cart.intersection_dir == 0:
                        cart.direction = INTERSECTION_LEFT[cart.direction]
                    elif cart.intersection_dir == 2:
                        cart.direction = INTERSECTION_RIGHT[cart.direction]
                    cart.intersection_dir = (cart.intersection_dir + 1) % 3
                elif cart.track == '/':
                    cart.direction = CURVE_FSLASH[cart.direction]
                elif cart.track == '\\':
                    cart.direction = CURVE_BSLASH[cart.direction]
                self.track_map[new_pos] = cart.direction
            else:
                if remove_collided:
                    remove_crashed_carts = True
                    cart.crashed = True
                    self.cart_positions.remove(new_pos)
                    for tmp in self.carts:
                        if tmp.position == new_pos:
                            self.track_map[new_pos] = tmp.track
                            tmp.crashed = True
                else:
                    self.track_map[new_pos] = 'X'
                    return (new_pos % self.track_width, new_pos // self.track_width)
        if remove_crashed_carts:
            self.carts = [cart for cart in self.carts if not cart.crashed]
            self.cart_positions = {cart.position for cart in self.carts}
            if len(self.carts) == 0:
                sys.exit('No more carts')
            elif len(self.carts) == 1:
                last_cart_pos = self.carts[0].position
                return (last_cart_pos % self.track_width, last_cart_pos // self.track_width)
        return None
    def print(self):
        for i in range(0, len(self.track_map), self.track_width):
            print(''.join(self.track_map[i:i+self.track_width]))


def main():
    cart_width = None
    cart_height = 0
    cart_map = []
    with open('../input/13.txt') as infile:
        for line in infile:
            stripped = line.rstrip('\n')
            if cart_width is None:
                cart_width = len(stripped)
            elif len(stripped) != cart_width:
                sys.exit('error in map')
            cart_map.extend(stripped)

    tracks1 = TrackSystem(cart_map.copy(), cart_width)
    while True:
        result = tracks1.move_carts()
        if result is not None:
            print(*result, sep=',')
            break

    tracks2 = TrackSystem(cart_map.copy(), cart_width)
    while True:
        result = tracks2.move_carts(remove_collided=True)
        if result is not None:
            print(*result, sep=',')
            break


if __name__ == "__main__":
    main()
