'''
An optimized Implementation of Suffix-Tree done by Yaroslav Romanus and Sasha Tsepilova
'''


leafEnd = -1
suffix_index = 0


class Node:
    '''
    The Suffix-tree's node.
    '''

    def __init__(self, leaf):
        '''
        Initializes the node of the suffix-tree.
        '''
        global suffix_index
        self.children = {}
        # for leaf nodes, it stores the index of suffix for
        # the path  from root to leaf"""
        self.leaf = leaf
        if leaf:
            self.suffix_index = suffix_index
            suffix_index += 1
        else:
            self.suffix_index = -1
        self.start = None
        self.end = None
        self.suffixLink = None

    def __eq__(self, node):
        return self.start == node.start and self.end == node.end and self.suffix_index == node.suffix_index

    def __ne__(self, node):
        return not self == node

    def __getattribute__(self, name):
        if name == 'end':
            if self.leaf:
                return leafEnd
        return super().__getattribute__(name)

    def __str__(self):
        return str(self.start)+', '+str(self.end)+', '+str(self.suffix_index)


class SuffixTree:
    '''
    The Suffix-Tree.
    '''

    def __init__(self, data):
        '''
        Initializes the tree.
        '''
        global suffix_index, leafEnd
        suffix_index = 0
        leafEnd = -1

        self._string = data
        self.lastNewNode = None
        self.active_node = None
        # active_edge is represeted as input string character
        # index (not the character itself)
        self.active_edge = -1
        self.active_len = 0
        # remain_suff_count tells how many suffixes yet to
        # be added in tree
        self.remain_suff_count = 0
        self.root_end = None
        self.split_end = None
        self.size = -1  # Length of input string
        self.root = None

    def edge_length(self, node):
        '''
        Returns the length of the edge.
        '''
        return node.end - node.start + 1

    def walk_down(self, current_node):
        '''
        Walk down from current node.
        activePoint change for walk down (APCFWD) using
        Skip/Count Trick  (Trick 1). If active_len is greater
        than current edge length, set next  internal node as
        active_node and adjust active_edge and active_len
        accordingly to represent same activePoint.
        '''
        length = self.edge_length(current_node)
        if self.active_len >= length:
            self.active_edge += length
            self.active_len -= length
            self.active_node = current_node
            return True
        return False

    def new_node(self, start, end=None, leaf=False):
        '''
        Adds new node.
        For root node, suffixLink will be set to NULL
        For internal nodes, suffixLink will be set to root
        by default in  current extension and may change in
        next extension.
        '''
        node = Node(leaf)
        node.suffixLink = self.root
        node.start = start
        node.end = end
        return node

    def extend_suffix_tree(self, pos):
        '''
        Extends sufix-tree (adds the character on given position).
        '''
        global leafEnd
        leafEnd = pos
        self.remain_suff_count += 1
        self.lastNewNode = None

        while self.remain_suff_count > 0:
            if self.active_len == 0:
                self.active_edge = pos

            if self.active_node.children.get(self._string[self.active_edge]) is None:
                self.active_node.children[self._string[self.active_edge]] = self.new_node(
                    pos, leaf=True)

                if self.lastNewNode is not None:
                    self.lastNewNode.suffixLink = self.active_node
                    self.lastNewNode = None

            else:
                _next = self.active_node.children.get(
                    self._string[self.active_edge])

                if self.walk_down(_next):
                    continue

                if self._string[_next.start + self.active_len] == self._string[pos]:
                    if((self.lastNewNode is not None) and (self.active_node != self.root)):
                        self.lastNewNode.suffixLink = self.active_node
                        self.lastNewNode = None
                    self.active_len += 1
                    break

                self.split_end = _next.start + self.active_len - 1
                split = self.new_node(_next.start, self.split_end)
                self.active_node.children[self._string[self.active_edge]] = split
                split.children[self._string[pos]
                               ] = self.new_node(pos, leaf=True)
                _next.start += self.active_len
                split.children[self._string[_next.start]] = _next

                if self.lastNewNode is not None:
                    self.lastNewNode.suffixLink = split

                self.lastNewNode = split
            self.remain_suff_count -= 1

            if (self.active_node == self.root) and (self.active_len > 0):  # APCFER2C1
                self.active_len -= 1
                self.active_edge = pos - self.remain_suff_count + 1

            elif self.active_node != self.root:  # APCFER2C2
                self.active_node = self.active_node.suffixLink

    def build_suffix_tree(self):
        '''
        Builds sufix tree for string.
        '''
        self.size = len(self._string)
        self.root_end = -1
        self.root = self.new_node(-1, self.root_end)
        self.active_node = self.root  # First active_node will be root

        for i in range(self.size):
            self.extend_suffix_tree(i)


if __name__ == "__main__":
    new_tree = SuffixTree('abcabxabcd$')
    new_tree.build_suffix_tree()
    for key in new_tree.root.children['a'].children:
        print(key, new_tree.root.children['a'].children[key])
