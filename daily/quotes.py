from bs4 import BeautifulSoup
import requests
import re
import logging


import json

from pathlib import Path

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

import pandas as pd

class Quotes:
    def __init__(self, url: str, author: str):
        self.url: str = url
        self.author: str = author
        self.pages = self.get_pages_count()
        self.data_path: Path = Path.cwd() / 'data' / 'quotes.json'

    def get_pages_count(self):
        soup = BeautifulSoup(requests.get(self.url, headers = headers).content, 'html.parser')
        return int(soup.find(class_ = 'next_page').find_previous_sibling('a').get_text())
    
    def log_quotes(self):

        all_quotes = []

        for i in range(self.pages - 1):
            logging.info(f'Getting quotes from page {i + 1} of {self.pages}')
            soup = BeautifulSoup(requests.get(f'{self.url}?page={i}', headers = headers).content, 'html.parser')
            for quote in soup.find_all(class_ = 'quoteText'):
                match = re.search(r'.*?\“(.*)”.*', quote.getText('|'))
                if match is not None:
                    all_quotes.append({'body': match.group(1).replace('|', '\n'), 'author': self.author})
        
        with open(self.data_path, 'w') as outfile:
            json.dump(all_quotes, outfile, indent=4)

    def get_quotes(self, amount: int = None):
        logging.info(f'Getting quote(s) from {self.data_path}...')
        quotes = pd.read_json(self.data_path)
        logging.info(f'Got {len(quotes)} quote(s)...')
        return quotes