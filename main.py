'''
Module for plotting and running a program.
'''
import requests
from trie import Trie
from flask import Flask, render_template, request
from autocomplete import Autocompleter, start_completing


def plot_ngram(words: list):
    '''
    Return url to the google ngram plot.
    '''
    query_str = '%2C'.join(words)
    base_url = f'https://books.google.com/ngrams/interactive_chart?content=\
{query_str}&year_start=1800&year_end=2000&corpus=15&smoothing=3'
    return base_url


app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def index():
    data = words = None

    if request.method == "POST":
        msg = request.form.get('msg')
        trie = start_completing()
        words = Autocompleter(trie).sorted_autocomplete(msg)
        data = plot_ngram(words)
        Trie.words = []

    return render_template('index.html', data=data, words=words)

if __name__ == "__main__":
    app.run(debug=True)
