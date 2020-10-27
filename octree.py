class OctreeNode:
    def __init__(self, eow: bool = False):
        self.eow = eow  # end of word
        self.children = {}

    def add(self, char, final_char: bool = False):
        assert char not in self.children.keys()
        self.children[char] = TrieNode(final_char)

    def __repr__(self):
        return '{} {}'.format('eow' if self.eow else '', self.children, )