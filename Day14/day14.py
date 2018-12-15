from collections import deque


def scoreboardize(num):
    i = 1
    scores = deque()
    if num == 0:
        return deque((0,))
    while i <= num:
        scores.appendleft((num % (i*10)) // i)
        i *= 10
    return scores


def main(board, inp):
    elf1 = board[0]
    elf2 = board[1]
    idx1 = 0
    idx2 = 1
    while len(board) < inp + 10:
        board.extend(scoreboardize(elf1+elf2))
        rot1, rot2 = elf1+1, elf2+1

        board.rotate(-rot1-idx1)
        elf1 = board[0]

        board.rotate(-rot2+rot1+idx1-idx2)
        elf2 = board[0]

        board.rotate(rot2+idx2)

        idx1 = (rot1 + idx1) % len(board)
        idx2 = (rot2 + idx2) % len(board)
    return board


if __name__ == '__main__':
    puzzle_in = 320851
    # puzzle_in = 9
    # for i in range(0, 20):
    #     print(scoreboardize(i))

    # Part 1
    board = main(deque([3, 7]), puzzle_in)
    board.rotate(10)

    for i in range(10):
        print(board.popleft(), end="")
    print()
