from collections import deque


class Node:
    def __init__(self, amt_children, amt_metadata):
        self.header = (amt_children, amt_metadata)
        self.children = []
        self.metadata = []

    def meta_sum(self):
        return sum(self.metadata) + sum([child.meta_sum() for child in self.children])

    def special_meta_sum(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            s = 0
            for metadata in self.metadata:
                if metadata <= len(self.children) and metadata > 0:  # Index in range
                    s += self.children[metadata-1].special_meta_sum()
            return s


def parse(inp):
    amt_children, amt_metadata = int(inp.popleft()), int(inp.popleft())
    node = Node(amt_children, amt_metadata)
    node.children = [parse(inp) for i in range(amt_children)]
    node.metadata = [int(inp.popleft()) for i in range(amt_metadata)]
    return node


if __name__ == '__main__':
    # content = deque("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split())
    with open("input.txt", 'r') as f:
        content = deque(f.read().split())
    root = parse(content)
    print("Part 1 Sum: ", root.meta_sum())
    print("Part 2 Sum: ", root.special_meta_sum())
