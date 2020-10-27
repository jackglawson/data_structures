class NTreeNode:
    def __init__(self, n):
        self.n = n
        self.children = []

    def make_children(self):
        self.children = [NTreeNode(self.n) for _ in range(self.n)]

    def __repr__(self):
        return 'Node with {} children'.format(len(self.children))


class NTree:
    """
    A tree in which each node has exactly n or 0 children. e.g.:
    n = 4: Quadtree
    n = 8: Octree
    """
    def __init__(self, n):
        self.n = n
        self.root = NTreeNode(self.n)


