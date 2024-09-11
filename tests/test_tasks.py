from .context import daily

import unittest
import logging

logging.basicConfig(level = logging.INFO)

class TasksTestSuite(unittest.TestCase):

    tasks = daily.Tasks()

    def test_log_tasks(self):
        self.assertIsNone(self.tasks.log_tasks())

    def test_get_tasks(self):
        tasks = self.tasks.get_tasks()
        self.assertIsNotNone(tasks) # Assumes we have tasks

if __name__ == '__main__':
    unittest.main()