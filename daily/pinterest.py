from py3pin.Pinterest import Pinterest as Py3pin
import logging
from logging import INFO, DEBUG, ERROR
from pymongo import MongoClient
from pymongo.collection import Collection
from os import environ

from .classes.post import Post
class Pinterest:
    def __init__(self, target_boards: list = [], max_posts: int = 100):
        self.max_posts = max_posts
        self.target_boards = target_boards
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['pinterest']
        self.pinterest = Py3pin(email = environ['PINTEREST_EMAIL'],
                      password = environ['PINTEREST_PASSWORD'],
                      username = environ['PINTEREST_USERNAME'],
                      cred_root = 'credentials')
        self.boards = self.pinterest.boards()
    
    def log_posts(self):
        '''Get all posts from the target boards'''
        for board in self.boards:
            if board['name'] in self.target_boards:
                rec_pins = []
                rec_batch = self.pinterest.board_recommendations(board_id = board['id'])
                while len(rec_batch) > 0 and len(rec_pins) < self.max_posts:
                    rec_pins += rec_batch
                for pin in rec_pins:
                    if 'images' in pin:
                        self.mongo.insert_one(self.to_post({'url': pin['images']['orig']['url']}).__dict__)

    def get_posts(self, amount: int = 5):
        '''
        Returns an array of random posts

                Parameters:
                        amount (int): The number of posts to return
                Returns:
                        posts (list): An array of posts
        '''
        return list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))

    def to_post(self, post: dict):
        '''
        Converts a post into the Post class

                Parameters:
                        post (dict): The post

                Returns:
                        post (Post): A proper instance of the Post class
        '''
        return Post(
            url = post['url']
        )