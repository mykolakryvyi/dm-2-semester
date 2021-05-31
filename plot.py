'''
Module for plotting and running a program.
'''
import requests
from flask import Flask, render_template, request


def plot_ngram():
    '''
    Return url to the google ngram plot.
    '''
    words = ['motive', 'sunlight', 'railway', 'abroad', 'supper']
    query_str = '%2C'.join(words)
    base_url = f'https://books.google.com/ngrams/interactive_chart?content=\
{query_str}&year_start=1800&year_end=2000&corpus=15&smoothing=3'
    return base_url

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    data = plot_ngram()
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
