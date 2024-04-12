from .context import daily

import unittest


class TasksTestSuite(unittest.TestCase):

    tasks = daily.Tasks()

    # def test_log_tasks(self):
    #     self.assertIsNone(self.tasks.log_tasks())
    #     documents = list(self.tasks.mongo.find({}))
    #     self.assertIsNotNone(documents) # Assumes we have tasks
    #     self.assertIsInstance(documents, list)

    def test_get_tasks(self):
        tasks = self.tasks.get_tasks()
        self.assertIsNotNone(tasks) # Assumes we have tasks
        self.assertIsInstance(tasks, list)
        self.assertIsInstance(tasks[0], daily.Task)
        self.assertIsNotNone(tasks[0].title)

if __name__ == '__main__':
    unittest.main()