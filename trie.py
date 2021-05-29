class Trie:
    def __init__(self) -> None:
        self.children = {}
        self.end_of_word = False
        self.weight = -1

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
        if self.end_of_word:
            print (item)
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

if __name__ == "__main__":
    list = [
    'sin',
    'singh',
    'sign',
    'sinus',
    'sit',
    'silly',
    'side',
    'son',
    'soda',
    'sauce',
    'sand',
    'soap',
    'sar',
    'solo',
    'sour',
    'sun',
    'sure',
    'an',
    'ant',
    'aunt',
    'hell',
    'hello',
    'help',
    'helps',
    'hellish',
    ]
x = Trie()
for i in list:
    x.add(i, 143)

print(x.autocomplete('sa'))
