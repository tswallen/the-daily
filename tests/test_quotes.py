from .context import daily

import unittest


class QuotesTestSuite(unittest.TestCase):

    quotes = daily.Quotes('https://www.goodreads.com/author/quotes/2622245.Lao_Tzu')

    def test_get_pages_count(self):
        self.assertIsNotNone(self.quotes.get_pages_count())
    
    def test_get_quotes(self):
        self.assertIsNotNone(self.quotes.get_quotes())


if __name__ == '__main__':
    unittest.main()
