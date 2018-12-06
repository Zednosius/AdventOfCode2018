from collections import deque


def case_mismatch(c1, c2):
    """Returns true if case is the only difference"""
    return abs(ord(c1)-ord(c2)) == 32


def reaction(out, inp):
    """Consumes inp and puts the fully reacted polymer in out"""
    while len(inp) > 1:
        c1, c2 = inp.popleft(), inp.popleft()

        if not case_mismatch(c1, c2):
            out.append(c1)
            inp.appendleft(c2)
        else:
            if len(out) > 0:
                inp.appendleft(out.pop())

    if len(inp) == 1:
        out.append(inp.pop())


def alchemy(chain):
    out = deque()
    reaction(out, chain)
    return out


if __name__ == '__main__':
    # Part 1
    with open('input.txt', 'r') as f:
        chain = deque(f.readlines()[0].strip())

        result = alchemy(deque(chain))
        print("Length: ", len(result))

    # Part 2
    letters = set()
    for c in result:
        letters.add(c.lower())

    letter_size = []
    for letter in letters:
        filtered = deque(filter(lambda x: letter != x and letter.upper() != x, chain))
        result = alchemy(filtered)
        letter_size.append((letter, len(result)))
    smallest = min(letter_size, key=lambda x: x[1])
    print(smallest)
