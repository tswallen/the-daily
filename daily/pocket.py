import logging
import json

from os import environ

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import pocket

import pandas as pd

class Pocket:
    def __init__(self):
        self.access_token = environ.get('POCKET_ACCESS_TOKEN', None)
        if self.access_token is None:
            logging.warning("Access token not found in environment. Running authorization process.")
            self.access_token = self.get_access_token()
            environ['POCKET_ACCESS_TOKEN'] = self.access_token
            logging.info(f"Access token set: {self.access_token}")
        self.data_path: Path = Path.cwd() / 'data' / 'pocket.json'
    
    def get_access_token(self):
        request_token = pocket.Pocket.get_request_token(consumer_key=environ['POCKET_CONSUMER_KEY'], redirect_uri=environ['POCKET_REDIRECT_URI'])
        auth_url = pocket.Pocket.get_auth_url(code=request_token, redirect_uri=environ['POCKET_REDIRECT_URI'])

        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(auth_url)
            logging.info(f"Navigating to: {auth_url}")

            redirect_uri = "https://getpocket.com/home"

            while True:
                current_url = driver.current_url
                
                if current_url.startswith(redirect_uri):
                    logging.info("User successfully logged in and redirected.")
                    break

                time.sleep(1)

            user_credentials = pocket.Pocket.get_credentials(consumer_key=environ['POCKET_CONSUMER_KEY'], code=request_token)

            access_token = user_credentials['access_token']

        finally:
            driver.quit()

        return access_token

    def log_items(self, amount: int = 10):
        pocket_instance = pocket.Pocket(environ['POCKET_CONSUMER_KEY'], self.access_token)
        logging.info(f'Logging {amount} items(s)...')
        response = pocket_instance.get(count=amount)

        all_items = list(response[0]['list'].values())

        with open(self.data_path, 'w') as outfile:
            json.dump(all_items, outfile, indent=4)

    def get_items(self, amount: int = None):
        logging.info(f'Getting item(s) from {self.data_path}...')
        items = pd.read_json(self.data_path)

        logging.info(f'Got {len(items)} item(s)...')
        return items