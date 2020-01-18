#!/usr/bin/python3

import io


def print_recipes(recipes, elves):
    s = io.StringIO()
    for i, recipe in enumerate(recipes):
        if i == elves[0]:
            s.write('({})'.format(recipe))
        elif i == elves[1]:
            s.write('[{}]'.format(recipe))
        else:
            s.write(' {} '.format(recipe))
    print(s.getvalue())


def calculate(n):
    recipes = [3, 7]
    current = [0, 1]
    while len(recipes) < (n + 10):
        new_recipe = recipes[current[0]] + recipes[current[1]]
        if new_recipe < 10:
            recipes.append(new_recipe)
        else:
            recipes.append(1)
            recipes.append(new_recipe-10)
        current[0] = (current[0] + 1 + recipes[current[0]]) % len(recipes)
        current[1] = (current[1] + 1 + recipes[current[1]]) % len(recipes)
    print(''.join([str(r) for r in recipes[n:n+10]]))


def count_recipes_before(score_seq):
    recipes = [3, 7]
    current = [0, 1]
    score_len = len(score_seq)
    checked = 0
    while True:
        new_recipe = recipes[current[0]] + recipes[current[1]]
        if new_recipe < 10:
            recipes.append(new_recipe)
        else:
            recipes.append(1)
            recipes.append(new_recipe-10)
        current[0] = (current[0] + 1 + recipes[current[0]]) % len(recipes)
        current[1] = (current[1] + 1 + recipes[current[1]]) % len(recipes)
        while checked <= (len(recipes) - len(score_seq)):
            for i in range(len(score_seq)):
                if score_seq[i] != recipes[checked+i]:
                    break
            else:
                print(checked)
                return
            checked += 1


def main():
    calculate(147061)
    count_recipes_before((1,4,7,0,6,1))


if __name__ == "__main__":
    main()
