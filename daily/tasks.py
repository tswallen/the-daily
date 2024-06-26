import logging
from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection

from os import environ

from .classes.task import Task, to_task

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]

class Tasks:
    def __init__(self):
        self.mongo: Collection = MongoClient(environ["MONGO_URL"])['daily']['tasks']
        self.credentials = None
        if os.path.exists("token.json"):
            self.credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.credentials.to_json())
        self.service = build("tasks", "v1", credentials = self.credentials)
    
    def log_tasks(self):
        '''
        Logs all tasks to Mongo

                Parameters:
                        amount (int): The number of tasks to log
                Returns:
                        tasks (list): An array of tasks
        '''

        tasklists = self.service.tasklists().list().execute().get("items", [])
        logging.info(f'Logging {len(tasklists)} tasklist(s)...')
        tasks = []
        for tasklist in tasklists:
            logging.info(f'Logging tasks from {tasklist["title"]}...')
            _tasks = self.service.tasks()
            request = _tasks.list(tasklist = tasklist['id'])
            while request is not None:
                _tasks_doc = request.execute()
                tasks.extend([{**item, 'tasklist_id': tasklist['id']} for item in _tasks_doc.get("items", [])])
                request = _tasks.list_next(request, _tasks_doc)

        tasks = [{'id': task['id'], 'title': task['title'], 'date': datetime.fromisoformat(task['updated'].replace("Z", "+00:00")), 'tasklist_id': task['tasklist_id'], 'duedate': task.get('due', None), 'status': task['status']} for task in tasks]
        tasks = [to_task(task) for task in tasks]

        logging.info(f'Logging {len(tasks)} task(s)...')
        
        self.mongo.insert_many([task.__dict__ for task in tasks])

    def get_tasks(self, amount: int = 1) -> List[Task]:
        '''
        Returns an array of tasks

                Parameters:
                        amount (int): The number of tasks to get
                Returns:
                        tasks (List[Task] | None): An array of tasks returned from Mongo expressed as an instance of the Task class
        '''
        # tasks = list(self.mongo.aggregate([{ '$sample': { 'size': amount } }]))
        tasks = list(self.mongo.find().limit(amount))
        logging.info(f'Getting {len(tasks)} task(s)...')
        return [to_task(task) for task in tasks]