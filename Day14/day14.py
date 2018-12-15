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


def compare_sub_deques(d1, d2):
    """Compares equality from the start of both deques"""
    for i in range(min(len(d1), len(d2))):
        # print(d1[0], " -- ", d2[0])
        if d1[0] != d2[0]:
            d1.rotate(i)
            d2.rotate(i)
            return False
        else:
            d1.rotate(-1)
            d2.rotate(-1)
    d1.rotate(i+1)
    d2.rotate(i+1)
    return True


def main(board, inp, p2=None):
    elf1 = board[0]
    elf2 = board[1]
    idx1 = 0
    idx2 = 1
    checked = 0
    found_p2_idx = -1
    found_p1_idx = -1
    found = False
    while len(board) < inp + 10 or not found:
        board.extend(scoreboardize(elf1+elf2))
        rot1, rot2 = elf1+1, elf2+1

        board.rotate(-rot1-idx1)
        elf1 = board[0]

        board.rotate(-rot2+rot1+idx1-idx2)
        elf2 = board[0]

        board.rotate(rot2+idx2)

        if p2 and len(board) > len(p2) and not found:
            board.rotate(-checked)
            # print()
            # print(p2, board)
            for i in range(0, len(board)-len(p2)+1-checked):
                # print(board[0], end=":")
                if compare_sub_deques(board, p2):
                    found_p2_idx = i+checked
                    found = True
                    board.rotate(-1)
                    break
                board.rotate(-1)
            board.rotate(i+1+checked)
            checked = checked+i+1
            # print(";;", board)
            # print(p2, board)

        idx1 = (rot1 + idx1) % len(board)
        idx2 = (rot2 + idx2) % len(board)
        if len(board) == inp + 10:
            found_p1_idx = len(board)-10
    return board, found_p1_idx, found_p2_idx


if __name__ == '__main__':
    puzzle_in = 320851
    p2 = deque([3, 2, 0, 8, 5, 1])
    # puzzle_in = 9
    # p2 = deque([0, 1, 2, 4, 5])
    # p2 = deque([5, 9, 4, 1, 4])
    # for i in range(0, 20):
    #     print(scoreboardize(i))

    # Part 1
    board, p1_idx, p2_count = main(deque([3, 7]), puzzle_in, p2)
    print(board, p1_idx)
    board.rotate(-p1_idx)

    for i in range(10):
        print(board.popleft(), end="")
    print()
    print("Recipes to the left:", p2_count)
