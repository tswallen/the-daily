from .context import daily

import unittest


class RedditTestSuite(unittest.TestCase):

    reddit = daily.Reddit(['tifu'])

    def test_log_posts(self):
        self.assertIsNone(self.reddit.log_posts())

    def test_get_posts(self):
        posts = self.reddit.get_posts()


if __name__ == '__main__':
    unittest.main()
