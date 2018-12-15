import numpy as np
from math import sin, cos, radians
from operator import sub, add

GS = 300


def test():
    assert main(8)[2, 4] == 4
    assert main(57)[121, 78] == -5
    assert main(39)[216, 195] == 0
    assert main(71)[100, 152] == 4
    print("Tests completed")


def main(grid_serial):
    grid = np.zeros((GS, GS))
    x, y = np.indices((GS, GS)) + 1
    rack_ids = x + 10

    grid = rack_ids*y
    grid = grid + grid_serial
    grid = grid * rack_ids
    grid = np.floor_divide(np.mod(grid, 1000), 100) - 5
    return grid


def calculate_3by3(grid):
    x, y = np.indices((GS, GS))
    x, y = x[1:-1, 1:-1], y[1:-1, 1:-1]  # Cut off the outer columns and rows (did this work accidentally?)
    sum_grid = np.zeros((GS, GS))
    sum_grid[x, y] = grid[x, y]
    for angle in range(0, 360, 45):
        sum_grid[x, y] += grid[x+round(cos(radians(angle))), y+round(sin(radians(angle)))]
    return sum_grid


def sum_slice(mat, x, y, size):
    return np.sum(mat[x+size-1, y:y+size])+np.sum(mat[x:x+size-1, y+size-1])


def calculate_xbyx_slice(grid, size):
    """Calculates the row and column slice that is size-1 indices away"""
    # xx, yy = np.indices((GS, GS))
    # print(xx, yy)
    sum_grid = np.zeros((GS, GS))
    if size == 1:
        sum_grid += grid
        return sum_grid
    else:
        for x in range(GS):
            for y in range(GS):
                # print(x, y)
                if x+size-1 < GS and y+size <= GS:
                    sum_grid[x, y] = np.sum(grid[x+size-1, y:y+size]) + np.sum(grid[x:x+size-1, y+size-1])
                    # assert prev_sum_grid[x, y] + sum_grid[x, y] == np.sum(grid[x:x+size, y:y+size])
        return sum_grid


def calculate_all_sizes(grid):
    sum_grid = np.zeros((GS, GS, GS), dtype=int)
    sum_grid[:, :, 0] += grid
    for size in range(1, GS):
        print(size, end='\r')

        xmask, ymask = np.indices((GS-size, GS-size))  # for size=1, which is a 2x2 the last index is 298
        sum_grid[:, :, size] = sum_grid[:, :, size-1]
        for x in range(size+1):
            sum_grid[xmask, ymask, size] += grid[xmask+x, ymask+size]

        for y in range(size):  # Or we sum x+size,y+size twice
            sum_grid[xmask, ymask, size] += grid[xmask+size, ymask+y]

        # for x in range(GS-size):
        #     for y in range(GS-size):
        #         np.testing.assert_equal((sum_grid[x, y, size]), np.sum(grid[x:x+size+1, y:y+size+1]))
    print()
    return sum_grid


if __name__ == '__main__':
    # test()
    grid = main(7165)
    # grid = main(18)
    print(grid)
    sums = calculate_3by3(grid)
    print(sums)
    max_index = np.unravel_index(np.argmax(sums), (GS, GS))
    print("Max index: ", max_index)  # Is the top left corner of 3by3
    print("Max value: ", sums[max_index])

    sum_grid = calculate_all_sizes(grid)
    max_index = np.unravel_index(np.argmax(sum_grid), (GS, GS, GS))
    print("Max index: ", tuple(map(add, max_index, (1, 1, 1))))
    print("Max value: ", sum_grid[max_index])
