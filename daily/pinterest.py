import logging
from typing import List

from py3pin.Pinterest import Pinterest as Py3pin
from os import environ

import json
from pathlib import Path

import pandas as pd

class Pinterest:
    def __init__(self, target_boards: list = [], max_pins: int = 100, login: bool = False):
        self.max_pins = max_pins
        self.target_boards = target_boards
        self.data_path: Path = Path.cwd() / 'data' / 'pinterest.json'
        if login:
            self.pinterest = Py3pin(email = environ['PINTEREST_EMAIL'],
                        password = environ['PINTEREST_PASSWORD'],
                        username = environ['PINTEREST_USERNAME'],
                        cred_root = 'credentials')
            self.pinterest.login(headless = False)
            self.boards = self.pinterest.boards()
        
    
    def log_pins(self): # TODO: add an amount limit here
        '''Get all pins from the target boards'''

        all_pins = []

        for board in self.boards:
            if board['name'] in self.target_boards:
                logging.info(f'Getting pins from {board["name"]}...')
                rec_pins = []
                rec_batch = self.pinterest.board_recommendations(board_id = board['id'])
                while len(rec_batch) > 0 and len(rec_pins) < self.max_pins:
                    rec_pins += rec_batch
                for pin in rec_pins:
                    if 'images' in pin:
                        all_pins.append(pin)

        
        with open(self.data_path, 'w') as outfile:
            json.dump(all_pins, outfile, indent=4)

    # def log_my_pins(self): # TODO: add an amount limit here
    #     '''Get all pins from the target boards'''
    #     for board in self.boards:
    #         if board['name'] in self.target_boards:
    #             logging.info(f'Getting pins from {board["name"]}...')
    #             rec_pins = []
    #             rec_batch = self.pinterest.board_recommendations(board_id = board['id'])
    #             while len(rec_batch) > 0 and len(rec_pins) < self.max_pins:
    #                 rec_pins += rec_batch
    #             for pin in rec_pins:
    #                 if 'images' in pin:
    #                     log_raw('pinterest_raw', pin)
    #                     self.mongo.insert_one(to_pin({'id': pin['id'], 'title': pin['grid_title'], 'url': pin['link'], 'image': pin['images']['orig']['url']}).__dict__)

    def get_pins(self, amount: int = None):
        logging.info(f'Getting pin(s) from {self.data_path}...')
        pins = pd.read_json(self.data_path)
        
        # if with_screenshot:
        #     for i, bookmark in enumerate(bookmarks):
        #         _id = bookmark['_id']
        #         bookmark = to_bookmark(bookmark)
        #         if bookmark.screenshot is None:
        #             bookmark.screenshot = bookmark.capture_screenshot()
        #             bookmarks[i]['screenshot'] = bookmark.screenshot
        #             self.mongo.update_one({'_id': _id}, {'$set': {'screenshot': bookmark.screenshot}})

        logging.info(f'Got {len(pins)} pin(s)...')
        return pins