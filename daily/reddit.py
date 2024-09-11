
from typing import List
from praw import Reddit as Praw
import logging
from os import environ

from pathlib import Path
import json

import pandas as pd

class Reddit:
    def __init__(self, target_subreddits: list = []):
        self.reddit = Praw(
            client_id = environ["REDDIT_CLIENT_ID"],
            client_secret = environ["REDDIT_CLIENT_SECRET"],
            #password = environ["REDDIT_PASSWORD"],
            user_agent = environ["REDDIT_USERAGENT"],
            #username = environ["REDDIT_USERNAME"],
        )
        self.target_subreddits = target_subreddits
        self.data_path: Path = Path.cwd() / 'data' / 'reddit.json'

    def log_posts(self, amount: int = 10):
        all_posts = []

        logging.info(f'Logging {amount} post(s)...')

        for subreddit in self.target_subreddits:
            for post in self.reddit.subreddit(subreddit).hot(limit = amount):
                all_posts.append({'title': post.title, 'url': post.url})

        with open(self.data_path, 'w') as outfile:
            json.dump(all_posts, outfile, indent=4)

    def get_posts(self, amount: int = None):
        logging.info(f'Getting post(s) from {self.data_path}...')
        posts = pd.read_json(self.data_path)
        logging.info(f'Got {len(posts)} post(s)...')
        return posts