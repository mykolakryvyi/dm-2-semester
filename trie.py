class Trie:
    def __init__(self) -> None:
        self.children = {}
        self.end_of_word = False
        self.weight = -1
        self.lst_of_words = []

    def add(self, item, weight) -> None:
        i = 0
        while i < len(item):
            k = item[i]
            if not k in self.children:
                node = Trie()
                self.children[k] = node
            self = self.children[k]
            if i == len(item) - 1: 
                self.end_of_word = True
                self.weight = weight
            else:
                self.end_of_word = False
            i += 1

    def search(self, item):
        if self.end_of_word and len(item) == 0:
            return True
        first = item[:1]  
        str = item[1:]  
        if first in self.children:
            return self.children[first].search(str)
        else:
            return False
    
    def traversal(self, item):
        lst_words = []
        if self.end_of_word:
            print(item, self.weight)
        for i in self.children:
            s = item + i
            self.children[i].traversal(s)

    def autocomplete(self, item):
        i = 0
        s = ''
        while i < len(item):
            k = item[i]
            s += k
            if k in self.children:
                self = self.children[k]
            else:
                return 'NOT FOUND'
            i += 1
        self.traversal(s)
        return 'END'

    def sorted_autocomplete(self, word):
        self.autocomplete(word)
        return self.lst_of_words

if __name__ == "__main__":
    file = open( 'unigram_freq.csv' , 'r' )
    contents = file.read().split('\n')
    search_trie = Trie()
    for i, elem in enumerate(contents):
        try: 
            word, freq = elem.split(',')
            contents[i] = [word, int(freq)]
            search_trie.add(word, int(freq))
        except ValueError:
            continue    

    print(search_trie.sorted_autocomplete('hell'))
