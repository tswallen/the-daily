from datetime import date

class Task:
    def __init__(self, id: str, title: str, date: date, tasklist_id: str, duedate: date | None, status: str):
        self.id = id
        self.title = title
        # Add conversion logic
        self.date = date
        self.tasklist_id = tasklist_id
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
        date = task['date'],
        tasklist_id = task['tasklist_id'],
        duedate = task.get('duedate'),
        status = task['status']
    )