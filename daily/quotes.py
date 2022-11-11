from bs4 import BeautifulSoup
import requests
import re
import logging
from logging import INFO, DEBUG, ERROR

class Quotes:
    def __init__(self, url: str):
        self.url: str = url
        self.pages = self.get_pages_count()
        self.quotes = []

    def get_pages_count(self):
        '''Get the number of pages of quotes'''
        soup = BeautifulSoup(requests.get(self.url).content, 'html.parser')
        return int(soup.find(class_ = 'next_page').find_previous_sibling('a').get_text())
    
    # TODO: log quotes to database
    def get_quotes(self):
        '''Get all quotes from the url'''
        for i in range(self.pages - 1):
            logging.log(INFO, f'Getting quotes from page {i + 1} of {self.pages}')
            print(f'Getting quotes from page {i + 1} of {self.pages}')
            soup = BeautifulSoup(requests.get(f'{self.url}?page={i}').content, 'html.parser')
            for quote in soup.find_all(class_ = 'quoteText'):
                match = re.search(r'.*?\“(.*)”.*', quote.getText('|'))
                if match is not None:
                    self.quotes.append(match.group(1).replace('|', '\n'))
        logging.log(INFO ,f'Got {len(self.quotes)} quotes')
        return self.quotes