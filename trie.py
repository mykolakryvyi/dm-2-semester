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

    def triestr(self) -> str:
        return self.children

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
