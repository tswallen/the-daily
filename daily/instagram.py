import logging

import json
from os import environ
from pathlib import Path

import instaloader

import pandas as pd

import os

class Instagram:
    def __init__(self):
        # Initialize Instaloader
        #self.L = instaloader.Instaloader(dirname_pattern='data/instagram/{shortcode}')
        #self.L.login(environ['INSTAGRAM_USERNAME'], environ['INSTAGRAM_PASSWORD'])

        # Load your own profile
        #self.profile = instaloader.Profile.from_username(self.L.context, environ['INSTAGRAM_USERNAME'])
        self.data_path: Path = Path.cwd() / 'data' / 'instagram.json'
    
    def log_posts(self, amount: int = 2):
        all_posts = []
        def get_info(post):
            post_info = {
                "shortcode": post.shortcode,  # Instagram post ID
                "url": f"https://www.instagram.com/p/{post.shortcode}/",  # Post URL
                "caption": post.caption,  # Post caption
                "likes": post.likes,  # Number of likes
                "comments": post.comments,  # Number of comments
                "date": post.date.strftime('%Y-%m-%d %H:%M:%S'),  # Post date in readable format
            }
            all_posts.append(post_info)
            return True

        
        self.L.download_feed_posts(max_count=amount, fast_update=True,
                           post_filter=lambda post: get_info(post))
        
        # # Get the 10 most recent posts from your profile
        # posts = self.L.get_feed_posts()

        # for index, post in enumerate(posts):
        #     if index >= 50:  # Limit to the top 10 posts
        #         break

        #     # Collect relevant post data

            
        #     all_posts.append(post_info)

        with open(self.data_path, 'w') as outfile:
            json.dump(all_posts, outfile, indent=4)

    def get_posts(self, amount: int = None):
        logging.info(f'Getting post(s) from {self.data_path}...')
        posts = pd.read_json(self.data_path)

        posts['image_urls'] = posts.apply(collect_image_urls, axis=1)

        logging.info(f'Got {len(posts)} post(s)...')
        return posts
    
# Define a function that collects image URLs for each row
def collect_image_urls(row):
    # Example logic to collect image URLs based on the shortcode or any other data in the row
    shortcode = row['shortcode']
    dir_name = f'data/instagram/{shortcode}'
    files = os.listdir(dir_name)
    files = [f for f in files if os.path.isfile(os.path.join(dir_name, f)) and not (f.endswith('.json.xz') or f.endswith('.txt'))]
    # Assume this function returns a list of URLs based on the shortcode
    image_urls = files
    return image_urls

# Apply the function to each row and create a new column
