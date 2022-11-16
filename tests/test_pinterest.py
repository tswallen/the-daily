from .context import daily

import unittest


class PinterestTestSuite(unittest.TestCase):

    pinterest = daily.Pinterest(['Travel'])

    def test_log_posts(self):
        self.assertIsNone(self.pinterest.log_posts())


if __name__ == '__main__':
    unittest.main()
