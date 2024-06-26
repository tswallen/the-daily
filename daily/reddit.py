
from typing import List
from praw import Reddit as Praw
import logging
from logging import INFO, DEBUG, ERROR
from pymongo import MongoClient
from pymongo.collection import Collection
from os import environ

from .classes.post import Post, to_post

from .utils import log_raw

class Reddit:
    def __init__(self, target_subreddits: list = []):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['reddit']
        self.reddit = Praw(
            client_id = environ["REDDIT_CLIENT_ID"],
            client_secret = environ["REDDIT_CLIENT_SECRET"],
            #password = environ["REDDIT_PASSWORD"],
            user_agent = environ["REDDIT_USERAGENT"],
            #username = environ["REDDIT_USERNAME"],
        )
        self.target_subreddits = target_subreddits

    def log_posts(self, amount: int = 10):
        '''
        Logs all posts to Mongo

                Parameters:
                        amount (int): The number of posts to log
                Returns:
                        posts (list): An array of posts
        '''
        # TODO: optimise for memory + MongoDB

        # posts = [post for subreddit in self.target_subreddits for post in self.reddit.subreddit(subreddit).hot(limit=amount)]
        # posts = [to_post({'title': post.title, 'url': post.url}) for post in posts]

        # logging.info(f'Logging {len(posts)} post(s)...')

        # self.mongo.insert_many([post.__dict__ for post in posts])

        logging.info(f'Logging {amount} post(s)...')

        for subreddit in self.target_subreddits:
            for post in self.reddit.subreddit(subreddit).hot(limit = amount):
                log_raw('reddit_raw', post)
                self.mongo.insert_one(to_post({'title': post.title, 'url': post.url}).__dict__)

    def get_posts(self, amount: int = 5) -> List[Post]:
        '''
        Returns an array of posts

                Parameters:
                        amount (int): The number of posts to get
                Returns:
                        posts (List[Post] | None): An array of posts returned from Mongo expressed as an instance of the Post class
        '''
        posts = list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))
        logging.info(f'Getting {len(posts)} posts(s)...')
        return [to_post(post) for post in posts]