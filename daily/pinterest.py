import logging
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

from py3pin.Pinterest import Pinterest as Py3pin
from os import environ

from .classes.post import Post, to_post

class Pinterest:
    def __init__(self, target_boards: list = [], max_posts: int = 100):
        self.max_posts = max_posts
        self.target_boards = target_boards
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['pinterest']
        self.pinterest = Py3pin(email = environ['PINTEREST_EMAIL'],
                      password = environ['PINTEREST_PASSWORD'],
                      username = environ['PINTEREST_USERNAME'],
                      cred_root = 'credentials')
        self.pinterest.login(headless = False)
        self.boards = self.pinterest.boards()
    
    def log_posts(self): # TODO: add an amount limit here
        '''Get all posts from the target boards'''
        for board in self.boards:
            if board['name'] in self.target_boards:
                logging.info(f'Getting posts from {board["name"]}...')
                rec_pins = []
                rec_batch = self.pinterest.board_recommendations(board_id = board['id'])
                while len(rec_batch) > 0 and len(rec_pins) < self.max_posts:
                    rec_pins += rec_batch
                for pin in rec_pins:
                    if 'images' in pin:
                        self.mongo.insert_one(to_post({'id': pin['id'], 'title': pin['grid_title'], 'url': pin['link'], 'image': pin['images']['orig']['url']}).__dict__)

    def get_posts(self, amount: int = 5) -> List[Post]:
        '''
        Returns an array of posts

                Parameters:
                        amount (int): The number of posts to get
                Returns:
                        posts (List[Post] | None): An array of posts returned from Mongo expressed as an instance of the Post class
        '''
        posts = list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))
        logging.info(f'Getting {len(posts)} post(s)...')
        return [to_post(post) for post in posts]