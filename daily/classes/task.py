from datetime import date

class Task:
    def __init__(self, id: str, title: str, duedate: date | None, status: str):
        self.id = id
        self.title = title
        self.duedate = duedate
        self.status = status

def to_task(task: dict):
    '''
    Converts a task into the Task class

            Parameters:
                    task (dict): The task

            Returns:
                    task (Task): A proper instance of the Task class
    '''
    return Task(
        id = task['id'],
        title = task['title'],
        duedate = task.get('duedate'),
        status = task['status']
    )