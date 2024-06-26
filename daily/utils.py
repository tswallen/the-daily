from pymongo import MongoClient
from pymongo.collection import Collection

from os import environ

def log_raw(collection_name: str, data: dict):
    mongo: Collection = MongoClient(environ["MONGO_URL"])['daily'][collection_name]
    mongo.insert_one(data)