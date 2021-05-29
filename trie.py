'''
Module with trie class realisation.
'''
class Trie:
    '''
    Class for trie realisation.
    '''
    words = []

    def __init__(self) -> None:
        '''
        Initialize class parameters.
        '''
        self.children = {}
        self.end_of_word = False
        self.weight = -1
        self.lst_of_words = []


    def add(self, item: str, weight: int) -> None:
        '''
        Add weighted word to the trie.
        '''
        index = 0

        while index < len(item):
            key = item[index]

            if not key in self.children:
                node = Trie()
                self.children[key] = node

            self = self.children[key]

            if index == len(item) - 1:
                self.end_of_word = True
                self.weight = weight
            else:
                self.end_of_word = False

            index += 1


    def search(self, item: str):
        '''
        Search for the word in the trie.
        '''
        if self.end_of_word and len(item) == 0:
            return True

        first = item[:1]
        string = item[1:]

        if first in self.children:
            return self.children[first].search(string)
        return False


    def traversal(self, item: str):
        '''
        Traveres the trie.
        '''
        if self.end_of_word:
            Trie.words.append((item, self.weight))

        for index in self.children:
            string = item + index
            self.children[index].traversal(string)
