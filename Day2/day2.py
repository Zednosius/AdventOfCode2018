from functools import reduce
from itertools import combinations

with open("input.txt", 'r') as f:
    data = f.readlines()

# Keep a map of the counted letters


def counter(s):
    return reduce(lambda m, x: {**m, x: m.get(x, 0)+1}, s, {})


def sum_rule(twos, threes, m):
    if all(v in m.values() for v in [2, 3]):
        return (twos+1, threes+1)
    elif 2 in m.values():
        return (twos+1, threes)
    elif 3 in m.values():
        return (twos, threes+1)
    else:
        return (twos, threes)


counted = reduce(lambda li, line: [*li, counter(line)], data, [])
count_filtered = filter(lambda m: any(v in set((2, 3)) for v in m.values()), counted)
checksum_parts = reduce(lambda tup, m: sum_rule(*tup, m), count_filtered, (0, 0))
print(checksum_parts)
print(checksum_parts[0]*checksum_parts[1])


def difference(s1, s2):
    return reduce(lambda c, s: c + 1 if s[0] != s[1] else c, zip(s1, s2), 0)


def same(s1, s2):
    return [s[0] if s[0] == s[1] else "" for s in zip(s1, s2)]

# Part 2


pairs = list(combinations(data, 2))
print(pairs)
differences = map(lambda s: difference(*s), pairs)
res = list(filter(lambda x: x[1] <= 1, enumerate(differences)))
s1, s2 = pairs[res[0][0]]
print("".join(same(s1, s2)))
