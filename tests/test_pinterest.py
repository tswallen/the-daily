from .context import daily

import unittest


class PinterestTestSuite(unittest.TestCase):

    pinterest = daily.Pinterest(['Travel'])

    def test_log_posts(self):
        self.assertIsNone(self.pinterest.log_posts())
        documents = list(self.pinterest.mongo.find({}))
        self.assertIsNotNone(documents) # Assumes we have posts
        self.assertIsInstance(documents, list)

    def test_get_posts(self):
        posts = self.pinterest.get_posts()
        self.assertIsNotNone(posts) # Assumes we have posts
        self.assertIsInstance(posts, list)
        self.assertIsInstance(posts[0], daily.Post)

if __name__ == '__main__':
    unittest.main()
