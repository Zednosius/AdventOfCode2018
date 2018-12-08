from pprint import pprint
from collections import defaultdict


class Generator:
    def __init__(self, x, y, m_id=None):
        self.id = m_id if m_id is not None else id(self)
        self.x = x
        self.y = y
        self.cells = {}
        self.infinite = False
        self.depth = 0

    def __str__(self):
        return "Gen{}({},{})".format(chr(ord('A')+self.id), self.x, self.y)


def dirs(x, y):
    return (x+1, y), (x-1, y), (x, y+1), (x, y-1)


def get_extremes(generators):
    """Returns two 4-tuples,
     one of generators that lie on an edge of the bounding box and one of the actual coordinates"""
    min_x = None
    min_y = None
    max_x = None
    max_y = None

    for generator in generators:
        if not min_x or generator.x < min_x.x:
            min_x = generator
        if not min_y or generator.y < min_y.y:
            min_y = generator
        if not max_x or generator.x > max_x.x:
            max_x = generator
        if not max_y or generator.y > max_y.y:
            max_y = generator
    return (min_x, min_y, max_x, max_y), (min_x.x, min_y.y, max_x.x, max_y.y)  # Left, Top, Right, Bottom


def manhattan_dist(generator, x, y):
    return abs(x - generator.x) + abs(y - generator.y)


def find_nearest(generators, x, y):
    dist = None
    closest = set()
    for gen in generators:
        gen_dist = manhattan_dist(gen, x, y)

        if dist is None or gen_dist < dist:
            closest = set()
            dist = gen_dist
            closest.add(gen)
        elif gen_dist == dist:
            closest.add(gen)

    return closest


def create_infinite_bound_checker(Left, Top, Right, Bottom):
    def bound_checker(x, y):  # Returns true if point is beyond the infinite bound
        return Left.x <= x <= Right.x and Top.y <= y <= Bottom.y
    return bound_checker


def parse(i, line):
    return Generator(*map(int, line.split(",")), m_id=i)


def pprint_cells(cells, left=0, top=0, right=0, bottom=0):
    print("  ", end=" ")
    for i in range(left, right):
        print(i, end="  ")
    print()
    for y in range(top, bottom):
        print(y, end=": ")
        for x in range(left, right):
            cell = cells.get((x, y), False)

            print("  " if cell is False else chr(ord('A') + cell[0]) +
                  str(cell[1]) if cell[0] is not None else "! ", end=" ")
        print()


def grow(generator, infinites, cells, in_bounds):
    d = generator.depth
    x = generator.x
    y = generator.y
    blocked = True
    for i in range(0, d):
        # Makes a diagonal around the generator 4 cells at a time.
        for cell in ((x-d+i, y-i), (x+i, y-d+i), (x+d-i, y+i), (x-i, y+d-i)):

            maybe_existing_cell = cells.get(cell, False)

            if maybe_existing_cell:
                if maybe_existing_cell[1] == generator.depth:
                    cells[cell] = (None, generator.depth)
                elif maybe_existing_cell[1] > generator.depth:
                    cells[cell] = (generator.id, generator.depth)
            else:
                # If there was an entirely free space, this generator is not blocked
                if not in_bounds(*cell):
                    infinites.add(generator)
                else:
                    blocked = False
                    cells[cell] = (generator.id, generator.depth)
    return blocked


def grow_cycle(generators, infinites, in_bounds, ltrb_coords):
    active = set(generators)
    cells = {(g.x, g.y): (g.id, g.depth) for g in generators}
    while len(active - infinites) > 0:
        # pprint_cells(cells, *ltrb_coords)
        # print("\n---------------\n")
        for generator in generators:
            generator.depth += 1
            blocked = grow(generator, infinites, cells, in_bounds)
            if blocked:  # Stop generator if it is entirely blocked
                active.discard(generator)
    finite = set(generators) - infinites
    return cells, finite


def min_dist_cell(generators, ltrb_coords):
    l, t, r, b = ltrb_coords
    min_dist = None
    min_cell = None
    for y in range(t, b+1):
        for x in range(l, r+1):
            sum_dist = sum([manhattan_dist(gen, x, y) for gen in generators])
            if not min_dist or sum_dist < min_dist:
                min_dist = sum_dist
                min_cell = (x, y)
    return min_cell


def find_cells_with_distance(generators, ltrb_coords, distance=10000):
    cx, cy = (int(sum((gen.x for gen in generators))/len(generators)),
              int(sum((gen.y for gen in generators))/len(generators)))
    # cx, cy = min_dist_cell(generators, ltrb_coords)
    # print("Centroid:", (cx, cy))

    count = 1
    found_distance = True
    d = 1
    while found_distance:
        found_distance = False
        current_cell = (cx-d, cy-d)
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            for i in range(2*d):
                current_cell = (current_cell[0] + dx, current_cell[1] + dy)
                # Count how many are below the distance
                sum_dist = sum([manhattan_dist(gen, *current_cell) for gen in generators])
                # print(sum_dist)
                if sum_dist < distance:
                    count += 1
                    found_distance = True
        d += 1
    return count


if __name__ == '__main__':
    generators = []

    with open("input.txt", 'r') as f:
        for i, line in enumerate(f):
            generators.append(parse(i, line))

    bounders, ltrb_coords = get_extremes(generators)
    cells, finites = grow_cycle(generators, set(bounders), create_infinite_bound_checker(*bounders), ltrb_coords)

    count = defaultdict(int)

    for (_, (cell_id, _)) in cells.items():
        count[cell_id] += 1

    max_area = max([count[finite_gen.id] for finite_gen in finites])
    print("Max area:", max_area)

    within_10k = find_cells_with_distance(generators, ltrb_coords)
    print("Cells within 10k: ", within_10k)
