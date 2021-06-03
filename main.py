'''
Module for plotting and running a program.
'''
from trie import Trie
from flask import Flask, render_template, request
from autocomplete import Autocompleter, start_completing
from full_text_search_engine import full_text_search_engine
from werkzeug.utils import secure_filename
import os


def plot_ngram(words: list):
    '''
    Return url to the google ngram plot.
    '''
    query_str = '%2C'.join(words)
    base_url = f'https://books.google.com/ngrams/interactive_chart?content=\
{query_str}&year_start=1800&year_end=2000&corpus=15&smoothing=3'
    return base_url


app = Flask(__name__)


def search_word(word):
    trie = start_completing()
    words = Autocompleter(trie).sorted_autocomplete(word)
    data = plot_ngram(words)
    Trie.words = []

    return words, data


@app.route("/", methods=["GET", "POST"])
def index():
    data = words = text_positions = pattern = None

    if request.method == "POST":
        word = request.form.get('word')
        text = request.form.get('text')
        pattern = request.form.get('pattern')

        try:
            f = request.files['textfile']
            f.save(secure_filename(f.filename))
            with open(secure_filename(f.filename), "r") as file:
                text = file.read()

            os.remove(secure_filename(f.filename))
        except:
            pass

        if word:
            words, data = search_word(word)

        if text:
            text_positions = full_text_search_engine(text, pattern)

    return render_template('index.html', data=data, words=words, text_positions=text_positions, pattern=pattern)


if __name__ == "__main__":
    app.run(debug=True)
