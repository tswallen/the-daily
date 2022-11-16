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
class Discord:
    def __init__(self, token: str = environ["DISCORD_TOKEN"]):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['discord']
        self.token: str = token
        self.websocket: WebSocket = WebSocket()
        self.websocket.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        self.event = self.receive_json_response()

        heartbeat_interval = self.event['d']['heartbeat_interval']/1000
        start_new_thread(self.heartbeat, (heartbeat_interval, self.websocket))
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
                print(f"{event['d']['author']['username']}: {event['d']['content']}:\n:{event['d']['attachments']}")
                op_code = event('op')
                if op_code == 11:
                    print('heartbeat recveived')
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

    # This starts the "heartbeat" or the initial connection to the discord server
    def heartbeat(self, interval, websocket): # TODO: does removing websocket break this?
        print('Heartbeat begin')
        while True:
            time.sleep(interval)
            heartbeatJSON = {
                "op": 1,
                "d": 'null'
            }
            self.send_json_request(heartbeatJSON)
            print("Heartbeat Sent")