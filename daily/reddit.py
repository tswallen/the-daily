
from praw import Reddit as Praw
import logging
from logging import INFO, DEBUG, ERROR
from pymongo import MongoClient
from pymongo.collection import Collection
from os import environ

class Reddit:
    def __init__(self, target_subreddits: list = [], max_posts: int = 10):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['reddit']
        self.reddit = Praw(
            client_id = environ["REDDIT_CLIENT_ID"],
            client_secret = environ["REDDIT_CLIENT_SECRET"],
            password = environ["REDDIT_PASSWORD"],
            user_agent = environ["REDDIT_USERAGENT"],
            username = environ["REDDIT_USERNAME"],
        )
        self.target_subreddits = target_subreddits
        self.max_posts = max_posts

    
    def log_posts(self):
        '''Get all posts from the target subreddits'''
        for subreddit in self.target_subreddits:
            for post in self.reddit.subreddit(subreddit).hot(limit = self.max_posts):
                self.mongo.insert_one({'title': post.title, 'url': post.url})

    def get_posts(self, amount: int = 5):
        '''
        Returns an array of random posts

                Parameters:
                        amount (int): The number of posts to return
                Returns:
                        posts (list): An array of posts
        '''
        return list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))

    # TODO: create a reddit post class
    # def to_post(self, post: dict):
    #     '''
    #     Converts a post into the Post class

    #             Parameters:
    #                     post (dict): The post

    #             Returns:
    #                     post (Post): A proper instance of the Post class
    #     '''
    #     return Post(
    #         url = post['url']
    #     )