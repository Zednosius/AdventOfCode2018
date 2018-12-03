import re
import numpy as np
from functools import reduce

reg = re.compile(r"#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<w>\d+)x(?P<h>\d+)")


def parse(line):
    m = reg.match(line)
    return tuple(map(int, (m.group('id'), m.group('left'), m.group('top'), m.group('w'), m.group('h'))))


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        data = list(map(parse, f.readlines()))
    sheet = np.zeros((1000, 1000))  # index out of bounds? never heard of it.
    for (ID, left, top, w, h) in data:
        sheet[left:left+w, top:top+h] += 1

    print(np.count_nonzero(sheet > 1))  # Squares with values larger than 1 has overlap.
