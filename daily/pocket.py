import logging
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

import pocket
from os import environ

class Pocket:
    def __init__(self):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['pocket']
        self.pocket_instance = pocket.Pocket()
    
    def log_pocket(self): # TODO: add an amount limit here
        
        things = self.pocket_instance.get(count=10)
        print(things)