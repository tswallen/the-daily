from .context import daily

import unittest


class InstagramTestSuite(unittest.TestCase):

    instagram = daily.Instagram()

    def test_log_posts(self):
        self.assertIsNone(self.instagram.log_posts())

    def test_get_posts(self):
        posts = self.instagram.get_posts()
        self.assertIsNotNone(posts) # Assumes we have pins

if __name__ == '__main__':
    unittest.main()
