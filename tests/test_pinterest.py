from .context import daily

import unittest


class PinterestTestSuite(unittest.TestCase):

    pinterest = daily.Pinterest(['Travel'])

    def test_log_pins(self):
        self.assertIsNone(self.pinterest.log_pins())
        documents = list(self.pinterest.mongo.find({}))
        self.assertIsNotNone(documents) # Assumes we have pins
        self.assertIsInstance(documents, list)

    def test_get_pins(self):
        pins = self.pinterest.get_pins()
        self.assertIsNotNone(pins) # Assumes we have pins
        self.assertIsInstance(pins, list)
        self.assertIsInstance(pins[0], daily.Pin)

if __name__ == '__main__':
    unittest.main()
