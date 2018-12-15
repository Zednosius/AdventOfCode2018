def scoreboardize(num):
    i = 1
    scores = []
    if num == 0:
        return [0]
    while i <= num:
        scores.insert(0, ((num % (i*10)) // i))
        i *= 10
    return scores


def compare_subarr(l1, s_idx1, l2, s_idx2):
    """Compares equality from the start of both arrays"""
    for i in range(min(len(l1)-s_idx1, len(l2)-s_idx2)):
        # print(l1[s_idx1+i], " -- ", l2[s_idx2+i])
        if l1[s_idx1+i] != l2[s_idx2+i]:
            return False
    return True


def main(board, inp, p2=None):
    elf1 = 0
    elf2 = 1

    checked = 0
    found_p2_idx = -1
    found_p1_idx = -1
    found = False
    while len(board) < inp + 10 or not found:
        board.extend(scoreboardize(board[elf1]+board[elf2]))
        elf1 = (elf1+board[elf1]+1) % len(board)
        elf2 = (elf2+board[elf2]+1) % len(board)

        if p2 and len(board) > len(p2) and not found:
            for i in range(checked, len(board)-len(p2)+1):
                if compare_subarr(board, checked, p2, 0):
                    found_p2_idx = checked
                    found = True
                    break
                checked = checked+1
        if len(board) == inp + 10:
            found_p1_idx = len(board)-10
    return board, found_p1_idx, found_p2_idx


if __name__ == '__main__':
    puzzle_in = 320851
    # p2 = deque([3, 2, 0, 8, 5, 1])
    p2 = ([3, 2, 0, 8, 5, 1])
    # puzzle_in = 9
    # p2 = ([0, 1, 2, 4, 5])
    # p2 = ([5, 9, 4, 1, 4])
    # p2 = ([5, 1, 5, 8, 9, 1, 6, 7, 7, 9])
    # for i in range(0, 20):
    #     print(scoreboardize(i))

    # Part 1
    board, p1_idx, p2_count = main(([3, 7]), puzzle_in, p2)
    print(board[p1_idx:p1_idx+10])
    print()
    print("Recipes to the left:", p2_count)
