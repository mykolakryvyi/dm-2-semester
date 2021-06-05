'''Compare PostgreSQL Fell Text Search Engine and self-made one.'''

import postgresql
from time import time
from full_text_search_engine import full_text_search_engine


class Database:
    '''
    Database class.
    '''

    DB_NAME = 'pgfts'
    DB_HOST = 'localhost'
    DB_USER = 'fts_user'

    def __init__(self):
        '''
        Initialize a database.
        '''
        self.DB = postgresql.open(host=Database.DB_HOST,
                                  database=Database.DB_NAME,
                                  user=Database.DB_USER)

    def clear(self):
        '''
        Clear the database.
        '''
        sql = """DELETE FROM fulltext_search"""
        self.DB.prepare(sql)

    def insert_data(self, filepath=None):
        '''
        Insert data from the given file to the database.
        '''
        data = read_file(filepath) if filepath else read_file()
        sql = f"""
            INSERT INTO fulltext_search VALUES(2,'{data}', '')
        """
        self.DB.prepare(sql)

    def search(self, query):
        '''
        Search the given pattern in the database.
        '''
        sql = """
            WITH q AS (SELECT plainto_tsquery($1) AS query),
            ranked AS (
                SELECT id, doc, ts_rank(tsv, query) AS rank
                FROM fulltext_search, q
                WHERE q.query @@ tsv
                ORDER BY rank DESC
            )
            SELECT id, ts_headline(doc, q.query, 'MaxWords=75000,MinWords=25,ShortWord=3,MaxFragments=300,FragmentDelimiter="||||"')
            FROM ranked, q
            ORDER BY ranked DESC
        """
        return self.DB.prepare(sql)


def read_file(filepath='text.txt'):
    '''
    Return text data from the given file.
    '''
    with open(filepath, 'r') as input_file:
        data = input_file.read()

    return data.replace("'", "")


def perform_postgresql_tests():
    '''
    Perform tests on PostgreSQL database.
    '''
    DB = Database()
    DB.clear()
    DB.insert_data()
    start_time = time()
    DB.search('Odysseus')
    end_time = time()

    return end_time - start_time


def perform_fulltext_tests():
    '''
    Perform tests on Full Text Search Engine implementation.
    '''
    data = read_file()
    start_time = time()
    full_text_search_engine(data, 'Odysseus')
    end_time = time()

    return end_time - start_time


def perform_tests():
    '''
    Perform tests and compare results.
    '''
    postgresql_result = perform_postgresql_tests()
    fulltext_result = perform_fulltext_tests()

    print(f'PostgreSQL finished in {postgresql_result:.4f} seconds.')
    print(f'FullTextSearchEngine finished in {fulltext_result:.4f} seconds.')


if __name__ == '__main__':
    perform_tests()
