from functools import reduce
from itertools import cycle

with open("input.txt", 'r') as f:
    indata = list(map(int, f.readlines()))
end_frequency = sum(indata)
print("P1:", end_frequency)

seen = set([0])
freq = 0
for x in cycle(indata):
    freq += x
    if freq in seen:
        print("P2", freq)
        break
    else:
        seen.add(freq)
