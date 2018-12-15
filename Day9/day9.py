class CircleNode:
    def __init__(self, value, left=None, right=None):
        """Create a CircleNode with value
        where the left and right are the nodes on this nodes respective side."""

        self.value = value
        self.left = left or self
        self.right = right or self

        # Fix the directions on the existing nodes.
        # Or we won't have a circle
        if not (self.left is self or self.right is self):
            left.right = self
            right.left = self

    def get(self, x=0):
        """
        x=0 returns the current node
        x<0 returns a left node
        x>0 returns a right node
        """
        if x <= -1:
            return self.left.get(x+1)
        elif x == 0:
            return self
        else:
            return self.right.get(x-1)

    def addLeft(self, value):
        """Adds a new node to the left of the current node and returns it"""
        self.left = CircleNode(value, left=self.left, right=self)
        return self.left

    def addRight(self, value):
        """Adds a new node to the right of the current node and returns it"""
        self.right = CircleNode(value, left=self, right=self.right)
        return self.right

    def remove(self):
        """Removes this element from the circle. Returns value and right element"""
        self.left.right = self.right
        self.right.left = self.left
        return self.value, self.right

    def acc_circle(self, li):
        if len(li) == 0 or li[0] is not self:
            li.append(self)
            return self.right.acc_circle(li)
        return li

    def __str__(self):
        return " ".join([str(n.value) for n in self.acc_circle([])])


def play_game(players, marbles):

    circle = CircleNode(0, None, None)
    zero_node = circle
    player = 1
    # print("[{}] ".format("-"), zero_node)
    scores = {player+1: 0 for player in range(players)}
    for marble in range(1, marbles+1):
        if marble % 23 == 0:
            val, circle = circle.get(-7).remove()
            scores[player] += val + marble
        else:
            circle = circle.get(1).addRight(marble)
        # print("[{}] ".format(player), zero_node)
        player = (player % players) + 1

    winner = max(scores.items(), key=lambda x: x[1])
    print("Winner: player {} with {} points".format(*winner))
    return winner[1]


def test_games():
    assert play_game(10, 1618) == 8317
    assert play_game(13, 7999) == 146373
    assert play_game(17, 1104) == 2764
    assert play_game(21, 6111) == 54718


if __name__ == '__main__':
    players = 9
    marbles = 25
    # play_game(9, 25)
    # test_games()
    # Input: 466 players; last marble is worth 71436 points
    play_game(466, 71436)
    play_game(466, 71436*100)  # Sure it's not fast, but it works!
