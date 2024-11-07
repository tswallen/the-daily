import logging

import json
from os import environ
from pathlib import Path

import pandas as pd

class Chrome:
    def __init__(self):
        self.bookmark_path: Path = Path.cwd() / 'data' / 'Bookmarks'
        self.data_path: Path = Path.cwd() / 'data' / 'chrome.json'
    
    def log_bookmarks(self, amount: int = None):
        with open(self.bookmark_path, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        
        logging.info(f'Importing bookmark(s) from {self.bookmark_path}...')
        
        def extract(bookmarks):
            return [b for bookmark in bookmarks for b in (extract(bookmark["children"]) if bookmark.get("type") == "folder" else [bookmark]) if b.get("type") == "url"]

        all_urls = extract([child for root in data.get("roots", {}).values() if "children" in root for child in root["children"]])
        
        with open(self.data_path, 'w') as outfile:
            json.dump(all_urls, outfile, indent=4)

    def get_bookmarks(self, with_screenshot: bool = False, amount: int = None):
        logging.info(f'Getting bookmark(s) from {self.data_path}...')
        bookmarks = pd.read_json(self.data_path)
        
        # if with_screenshot:
        #     for i, bookmark in enumerate(bookmarks):
        #         _id = bookmark['_id']
        #         bookmark = to_bookmark(bookmark)
        #         if bookmark.screenshot is None:
        #             bookmark.screenshot = bookmark.capture_screenshot()
        #             bookmarks[i]['screenshot'] = bookmark.screenshot
        #             self.mongo.update_one({'_id': _id}, {'$set': {'screenshot': bookmark.screenshot}})

        logging.info(f'Got {len(bookmarks)} bookmark(s)...')
        return bookmarks