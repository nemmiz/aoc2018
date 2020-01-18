#!/usr/bin/python3

class CircularLinkedListNode:
    def __init__(self, value, prev_node, next_node):
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node

class CircularLinkedList:
    def __init__(self, initial_value):
        initial_node = CircularLinkedListNode(initial_value, None, None)
        initial_node.prev_node = initial_node
        initial_node.next_node = initial_node
        self.current_node = initial_node
    def move_clockwise(self, amount):
        while amount > 0:
            self.current_node = self.current_node.next_node
            amount -= 1
    def move_counter_clockwise(self, amount):
        while amount > 0:
            self.current_node = self.current_node.prev_node
            amount -= 1
    def insert(self, value):
        prev_node = self.current_node.prev_node
        next_node = self.current_node
        new_node = CircularLinkedListNode(value, prev_node, next_node)
        prev_node.next_node = new_node
        next_node.prev_node = new_node
        self.current_node = new_node
    def delete(self):
        prev_node = self.current_node.prev_node
        next_node = self.current_node.next_node
        prev_node.next_node = next_node
        next_node.prev_node = prev_node
        self.current_node.prev_node = None
        self.current_node.next_node = None
        value = self.current_node.value
        self.current_node = next_node
        return value
    def delete_all(self):
        current_node = self.current_node
        while current_node is not None:
            next_node = current_node.next_node
            current_node.prev_node = None
            current_node.next_node = None
            current_node = next_node
        self.current_node = None


def play(players, last_marble):
    scores = [0] * (players+1)
    marbles = CircularLinkedList(0)
    current_player = 1

    for marble in range(1, last_marble+1):
        if (marble % 23) == 0:
            marbles.move_counter_clockwise(7)
            scores[current_player] += (marbles.delete() + marble)
        else:
            marbles.move_clockwise(2)
            marbles.insert(marble)

        current_player += 1
        if current_player > players:
            current_player = 1

    marbles.delete_all()
    winning_score = max(scores)
    winning_player = scores.index(winning_score)
    print('Player', winning_player, 'wins with a score of', winning_score)


def play_slow(players, last_marble):
    scores = [0] * (players+1)
    marbles = [0]
    current_player = 1
    current_marble_index = 0

    for marble in range(1, last_marble+1):
        if (marble % 23) == 0:
            pop_index = current_marble_index - 7
            if pop_index < 0:
                pop_index += len(marbles)
            pop_value = marbles.pop(pop_index)
            scores[current_player] += (pop_value + marble)
            current_marble_index = pop_index
        else:
            new_index = ((current_marble_index + 1) % len(marbles)) + 1
            marbles.insert(new_index, marble)
            current_marble_index = new_index

        current_player += 1
        if current_player > players:
            current_player = 1

    winning_score = max(scores)
    winning_player = scores.index(winning_score)
    print('Player', winning_player, 'wins with a score of', winning_score)


def main():
    play(470, 72170)
    play(470, 7217000)


if __name__ == "__main__":
    main()
