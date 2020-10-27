from copy import copy


class TrieNode:
    def __init__(self, eow: bool = False):
        self.eow = eow  # end of word
        self.children = {}

    def add(self, char, final_char: bool = False):
        assert char not in self.children.keys()
        self.children[char] = TrieNode(final_char)

    def __repr__(self):
        return '{} {}'.format('eow' if self.eow else '', self.children, )


class Trie:
    """
    A data structure to efficiently store a list of words. Finds words of length n in O(n).
    """

    def __init__(self, words: list):
        words.sort()  # must be in alphabetical order
        self.root = TrieNode()
        for word in words:
            self._add_word(word)

    def _add_word(self, word: str):
        print(word)
        print(word[0])
        if word in self:
            return

        word = list(word)
        node = self.root
        while word[0] in node.children.keys():
            node = node.children[word.pop(0)]
        while word:
            char = word.pop(0)
            node.add(char, True if not word else False)
            node = node.children[char]

    def find_words(self, letters: list):
        valid_words = set()
        search_candidate = []
        letters_remaining = copy(letters)

        def search(v):
            if v.eow and ''.join(search_candidate) not in valid_words:
                valid_words.add(''.join(search_candidate))

            for l in set(letters_remaining):
                if l in v.children:
                    search_candidate.append(l)
                    letters_remaining.remove(l)
                    search(v.children[l])
                    del search_candidate[-1]
                    letters_remaining.append(l)

        search(self.root)
        return valid_words

    def get_lexicon(self):
        lexicon = set()
        search_candidate = []

        def search(v):
            if v.eow and ''.join(search_candidate) not in lexicon:
                lexicon.add(''.join(search_candidate))

            for l, w in v.children.items():
                search_candidate.append(l)
                search(w)
                del search_candidate[-1]

        search(self.root)
        return lexicon

    def __contains__(self, word: str):
        word = list(word)
        node = self.root
        while word:
            char = word.pop(0)
            try:
                node = node.children[char]
            except KeyError:
                return False
        return True if node.eow else False

    def __repr__(self):
        return str(self.root)
