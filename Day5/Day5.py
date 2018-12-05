from collections import deque


def case_mismatch(c1, c2):
    """Returns true if case is the only difference"""
    return abs(ord(c1)-ord(c2)) == 32


def reaction(out, inp):
    while len(inp) > 1:
        c1, c2 = inp.popleft(), inp.popleft()

        if not case_mismatch(c1, c2):
            out.append(c1)
            inp.appendleft(c2)
        else:
            if len(out) > 0:
                inp.appendleft(out.pop())

    if len(inp) == 1:
        out.append(inp[0])


def alchemy(chain):
    out = deque()
    reaction(out, chain)
    return out


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        chain = deque(f.readlines()[0].strip())

        result = alchemy(chain)
        print("Length: ", len(result))
