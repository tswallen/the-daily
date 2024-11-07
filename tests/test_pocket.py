from .context import daily

import unittest


class PocketTestSuite(unittest.TestCase):

    pocket = daily.Pocket()

    @unittest.skip("Skipping test that requires manual interaction")
    def test_get_access_token(self):
        access_token = self.pocket.get_access_token()
        self.assertIsNotNone(access_token)

    def test_log_items(self):
        self.assertIsNone(self.pocket.log_items())

    def test_get_items(self):
        items = self.pocket.get_items()
        self.assertIsNotNone(items) # Assumes we have items

if __name__ == '__main__':
    unittest.main()