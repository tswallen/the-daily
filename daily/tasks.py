import logging

from .classes.task import Task, to_task

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]

import json
from pathlib import Path
import pandas as pd

class Tasks:
    def __init__(self):
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
        self.data_path: Path = Path.cwd() / 'data' / 'tasks.json'
    
    def log_tasks(self):
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
        
        with open(self.data_path, 'w') as outfile:
            json.dump(tasks, outfile, indent=4)

    def get_tasks(self, amount: int = None):
        logging.info(f'Getting task(s) from {self.data_path}...')
        tasks = pd.read_json(self.data_path)
        logging.info(f'Got {len(tasks)} task(s)...')
        return tasks