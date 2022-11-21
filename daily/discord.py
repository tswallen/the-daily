import logging
from logging import INFO, DEBUG, ERROR
from websocket import WebSocket
import json
import time
import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from os import environ

from _thread import start_new_thread

from .classes.message import Message

class Discord:
    def __init__(self, token: str = environ["DISCORD_TOKEN"]):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['discord']
        self.token: str = token
        self.websocket: WebSocket = WebSocket()
        self.websocket.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        self.event = self.receive_json_response()
        self.heartbeat_interval = self.event['d']['heartbeat_interval']/1000

        start_new_thread(self.heartbeat, ())
        self.send_json_request({
            'op' : 2,
            'd':{
                'token' : self.token,
                'properties':{
                    '$os': "windows", # TODO: can we change this?
                'brower': "edge",
                "$device": "pc"
                }
            }
        })

    def log_messages(self, media_only: bool = False):
        '''
        Logs messages to Mongo
            
            Parameters:
                media_only (bool): Whether to only log messages with media
        '''
        while True:
            event = self.receive_json_response()
            try:
                if media_only and (len(event['d']['attachments']) > 0):
                    for attachment in event['d']['attachments']:
                        self.mongo.insert_one({
                            'author': event['d']['author']['username'],
                            'media': attachment['url']
                        })
                elif not media_only:
                    self.mongo.insert_one({
                        'author': event['d']['author']['username'],
                        'media': str(event['d']['attachments']),
                        'content': str(event['d']['content'])
                    })
            except:
                pass

    # TODO: log quotes to database
    def get_messages(self):
        '''Gets all messages from Mongo'''
        pass

    # Because of discord's live and secure nature, i used websocket
    def send_json_request(self, request):
        self.websocket.send(json.dumps(request))

    def receive_json_response(self):
        response = self.websocket.recv()
        if response:
            return json.loads(response)

    def heartbeat(self):
        while True:
            time.sleep(self.heartbeat_interval) # TODO: move to end?
            self.send_json_request({'op': 1, 'd': 'null'})

    def to_message(self, message: dict):
        '''
        Converts a message into the Message class

                Parameters:
                        message (dict): The message

                Returns:
                        message (Message): A proper instance of the Message class
        '''
        return Message(
            author = message['author'],
            media = message['media'],
            content = message['content']
        )