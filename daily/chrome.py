import logging
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

import json
from os import environ
from pathlib import Path

from .classes.bookmark import Bookmark, to_bookmark

class Chrome:
    def __init__(self):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['chrome']
    
    def log_bookmarks(self, amount: int = None):
        '''
        Logs all bookmarks to Mongo

                Parameters:
                        amount (int): The number of bookmarks to log
                Returns:
                        bookmarks (list): An array of bookmarks
        '''

        bookmarks_file = Path.home() / Path("AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks")
        folder_path = environ.get('CHROME_BOOKMARKS_PATH').split('/')

        logging.info(f'Reading bookmarks from {bookmarks_file}...')

        with open(bookmarks_file, 'r', encoding='utf-8') as file:
            bookmarks_data = json.load(file)

        def find_folder(bookmarks, folder_path):
            if not folder_path:
                return bookmarks
            current_folder_name = folder_path.pop(0)
            for item in bookmarks:
                if item['type'] == 'folder' and item['name'] == current_folder_name:
                    return find_folder(item['children'], folder_path)
            return []

        bookmarks_list = []
        for root_key in ['bookmark_bar', 'other', 'synced']:
            root_bookmarks = bookmarks_data['roots'].get(root_key, {}).get('children', [])
            bookmarks_list.extend(find_folder(root_bookmarks, folder_path.copy()))

        bookmarks = [{'title': bookmark['name'], 'url': bookmark['url']} for bookmark in bookmarks_list[:amount if amount is not None else len(bookmarks_list)] if bookmark.get('type') == 'url']        
        bookmarks = [to_bookmark(bookmark) for bookmark in bookmarks]
        
        logging.info(f'Logging {len(bookmarks)} bookmark(s)...')
        
        self.mongo.insert_many([bookmark.__dict__ for bookmark in bookmarks])

    def get_bookmarks(self, amount: int = 1) -> List[Bookmark]:
        '''
        Returns an array of bookmarks

                Parameters:
                        amount (int): The number of bookmarks to get
                Returns:
                        bookmarks (List[Bookmark] | None): An array of bookmarks returned from Mongo expressed as an instance of the Bookmark class
        '''
        bookmarks = list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))
        logging.info(f'Getting {len(bookmarks)} bookmark(s)...')
        return [to_bookmark(bookmark) for bookmark in bookmarks]