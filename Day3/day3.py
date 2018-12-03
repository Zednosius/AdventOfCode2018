import re
import numpy as np
from functools import reduce

reg = re.compile(r"#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<w>\d+)x(?P<h>\d+)")


class Claim:
    def __init__(self, id, left, top, w, h):
        self.id = id
        self.left = left
        self.top = top
        self.right = left+w
        self.bottom = top+h

    def __str__(self):
        return "({},{},{},{},{})".format(self.id, self.left, self.top, self.right, self.bottom)


def parse(line):
    m = reg.match(line)
    return Claim(*tuple(map(int, (m.group('id'), m.group('left'), m.group('top'), m.group('w'), m.group('h')))))


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        data = list(map(parse, f.readlines()))
    sheet = np.zeros((1000, 1000))  # index out of bounds? never heard of it.

    for claim in data:
        sheet[claim.left:claim.right, claim.top:claim.bottom] += 1

    print(np.count_nonzero(sheet > 1))  # Squares with values larger than 1 has overlap.

    # Part 2
    for claim in data:
        if np.all(sheet[claim.left:claim.right, claim.top:claim.bottom] == 1):
            print("Non-overlapping claim: ", claim)
            break
