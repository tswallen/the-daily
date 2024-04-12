import logging
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

from py3pin.Pinterest import Pinterest as Py3pin
from os import environ

from .classes.pin import Pin, to_pin

class Pinterest:
    def __init__(self, target_boards: list = [], max_pins: int = 100):
        self.max_pins = max_pins
        self.target_boards = target_boards
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['pinterest']
        self.pinterest = Py3pin(email = environ['PINTEREST_EMAIL'],
                      password = environ['PINTEREST_PASSWORD'],
                      username = environ['PINTEREST_USERNAME'],
                      cred_root = 'credentials')
        self.pinterest.login(headless = False)
        self.boards = self.pinterest.boards()
    
    def log_pins(self): # TODO: add an amount limit here
        '''Get all pins from the target boards'''
        for board in self.boards:
            if board['name'] in self.target_boards:
                logging.info(f'Getting pins from {board["name"]}...')
                rec_pins = []
                rec_batch = self.pinterest.board_recommendations(board_id = board['id'])
                while len(rec_batch) > 0 and len(rec_pins) < self.max_pins:
                    rec_pins += rec_batch
                for pin in rec_pins:
                    if 'images' in pin:
                        self.mongo.insert_one(to_pin({'id': pin['id'], 'title': pin['grid_title'], 'url': pin['link'], 'image': pin['images']['orig']['url']}).__dict__)

    def get_pins(self, amount: int = 5) -> List[Pin]:
        '''
        Returns an array of pins

                Parameters:
                        amount (int): The number of pins to get
                Returns:
                        pins (List[Pin] | None): An array of pins returned from Mongo expressed as an instance of the Pin class
        '''
        pins = list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))
        logging.info(f'Getting {len(pins)} pin(s)...')
        return [to_pin(pin) for pin in pins]