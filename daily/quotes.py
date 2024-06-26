from bs4 import BeautifulSoup
import requests
import re
import logging
from logging import INFO, DEBUG, ERROR
from pymongo import MongoClient
from pymongo.collection import Collection
from os import environ

from .classes.quote import Quote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

from .utils import log_raw

class Quotes:
    def __init__(self, url: str, author: str):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['quotes']
        self.url: str = url
        self.author: str = author
        self.pages = self.get_pages_count()

    def get_pages_count(self):
        '''Get the number of pages of quotes'''
        soup = BeautifulSoup(requests.get(self.url, headers = headers).content, 'html.parser')
        return int(soup.find(class_ = 'next_page').find_previous_sibling('a').get_text())
    
    def log_quotes(self):
        '''Get all quotes from the url'''
        for i in range(self.pages - 1):
            logging.log(INFO, f'Getting quotes from page {i + 1} of {self.pages}')
            soup = BeautifulSoup(requests.get(f'{self.url}?page={i}', headers = headers).content, 'html.parser')
            for quote in soup.find_all(class_ = 'quoteText'):
                match = re.search(r'.*?\“(.*)”.*', quote.getText('|'))
                if match is not None:
                    log_raw('quotes_raw', match)
                    self.mongo.insert_one(self.to_quote({'body': match.group(1).replace('|', '\n'), 'author': self.author}).__dict__)

    def get_quote(self):
        '''
        Returns a random quote
        
                Returns:
                        quote (Quote): A random quote
        '''
        return self.to_quote(list(self.mongo.aggregate([{ '$sample': { 'size': 1 } }]))[0])

    def to_quote(self, quote: dict):
        '''
        Converts a quote into the Quote class

                Parameters:
                        quote (dict): The quote

                Returns:
                        quote (Quote): A proper instance of the Quote class
        '''
        return Quote(
            body = quote['body'],
            author = quote['author']
        )