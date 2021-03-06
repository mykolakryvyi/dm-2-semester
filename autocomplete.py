'''
Module with autocomplete function realisation.
'''
from trie import Trie
from flask import Flask, render_template, request


class Autocompleter:
    '''
    Autocomplete realisation.
    '''
    def __init__(self, tree: object) -> None:
        '''
        Initialize class parameters.
        '''
        self.tree = tree


    def autocomplete(self, item: str) -> str:
        '''
        Realization of the autocomplete function.
        '''
        counter = 0
        string = ''

        while counter < len(item):
            key = item[counter]
            string += key

            if key not in self.tree.children:
                return 'NOT FOUND'

            self.tree = self.tree.children[key]
            counter += 1

        self.tree.traversal(string)

        return 'END'


    def sorted_autocomplete(self, word: str) -> list:
        '''
        Returns list with top 5 words that have the biggest weight.
        '''
        self.autocomplete(word)
        trie = Trie()
        trie.words.sort(key = lambda x: x[1])
        trie.words.reverse()
        needed_words = Trie.words[:5]
        top_5_words = []

        for elem in needed_words:
            top_5_words.append(elem[0])

        return top_5_words


    @staticmethod
    def read_file() -> list:
        '''
        Returns list from lines from a file that was read.
        '''
        with open('unigram_freq.csv' , 'r') as file:
            lines = file.read().split('\n')
        return lines


def start_completing():
    '''
    Runs the main program, returns words based on the input of the user.
    '''
    search_trie = Trie()
    autocompleter = Autocompleter(search_trie)
    contents = autocompleter.read_file()
    for index, element in enumerate(contents):
        try:
            one_word, freq = element.split(',')
            contents[index] = [one_word, int(freq)]
            search_trie.add(one_word, int(freq))
        except ValueError:
            continue
    return search_trie
