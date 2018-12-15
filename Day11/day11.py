import numpy as np
from math import sin, cos, radians
from operator import sub


def test():
    assert main(8)[2, 4] == 4
    assert main(57)[121, 78] == -5
    assert main(39)[216, 195] == 0
    assert main(71)[100, 152] == 4
    print("Tests completed")


def main(grid_serial):
    grid = np.zeros((300, 300))
    x, y = np.indices((300, 300)) + 1
    rack_ids = x + 10

    grid = rack_ids*y
    grid = grid + grid_serial
    grid = grid * rack_ids
    grid = np.floor_divide(np.mod(grid, 1000), 100) - 5
    return grid


def calculate_3by3(grid):
    x, y = np.indices((300, 300))
    x, y = x[1:-1, 1:-1], y[1:-1, 1:-1]  # Cut off the outer columns and rows
    sum_grid = np.zeros((300, 300))
    sum_grid[x, y] = grid[x, y]
    for angle in range(0, 360, 45):
        sum_grid[x, y] += grid[x+round(cos(radians(angle))), y+round(sin(radians(angle)))]
    return sum_grid


if __name__ == '__main__':
    # test()
    grid = main(7165)
    print(grid)
    sums = calculate_3by3(grid)
    print(sums)
    max_index = np.unravel_index(np.argmax(sums), (300, 300))
    print("Max index: ", max_index)  # Is the top left corner of 3by3
    print("Max value: ", sums[max_index])
