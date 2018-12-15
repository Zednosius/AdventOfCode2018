from collections import defaultdict
import re
from pprint import pprint
pattern = re.compile(r"((?:#|\.){5}) => (#|\.)")


def parse(line, transitions):
    m = pattern.match(line)
    print(m.group(1), m.group(2))
    transitions[m.group(1)[2]][m.group(1)] = m.group(2)


def get_adj(state, index):
    return "".join([state.get(idx, '.') for idx in range(index-2, index+3)])


def print_state(state):
    for i in range(min(state), max(state)+1):
        print(state[i], end="")
    print()


def count_dots(state, start, stop, step=1):
    count = 0
    # print(state)
    for i in range(start, stop, step):
        # print(i, state[i])
        if state[i] == "#":
            break
        else:
            count += 1
    return count


def main(state, transitions, gens=20):
    print_state(state)
    for gen in range(gens):
        # Part 2
        if gen >= 110:  # manually checked value
            # The potted plants reaches a steady state where every potted plants jumps
            # on pot to the right every generation.
            state = {k+(gens - gen): state[k] for k in state}
            break
        # Part 1
        else:
            new_state = {k: transitions[v].get(get_adj(state, k)) for k, v in state.items()}

            _min, _max = min(new_state), max(new_state)
            left_dots = count_dots(state, _min, _max)
            right_dots = count_dots(state, _max, _min, -1)
            print(_min, _max)
            print(gen)
            # print(left_dots, right_dots)
            # Grow more if needed
            if left_dots < 5:
                for i in range(_min-1, _min-5+left_dots, -1):
                    new_state[i] = '.'
            else:
                for i in range(_min, _min+left_dots-5, 1):
                    del new_state[i]

            if right_dots < 5:
                for i in range(_max+1, _max+5-right_dots, 1):
                    new_state[i] = '.'
            else:
                for i in range(_max-right_dots+5, _max, 1):
                    del new_state[i]

            state = new_state
            print_state(state)
            print(sum([k if v == '#' else 0 for k, v in state.items()]))
    print()
    return sum([k if v == '#' else 0 for k, v in state.items()])


if __name__ == '__main__':

    with open("input.txt", "r") as f:
        initial = {i: v for i, v in enumerate(f.readline().split()[2])}
        transitions = {'#': {}, '.': {}}
        f.readline()  # Skips blank line
        print(initial)
        for line in f:
            parse(line, transitions)

    length = len(initial)
    for k in range(5):
        if initial[length-k-1] == '#':
            break
    for i in range(length, length + 5-k):
        initial[+i] = "."

    for k in range(5):
        if initial[k] == '#':
            break
    for i in range(0, k-5, -1):
        initial[i] = '.'

    pprint(initial)
    pprint(transitions)

    print("Potted plants after 20:", main(initial, transitions))
    print("Potted plants after 50bil:", main(initial, transitions, gens=50000000000))
