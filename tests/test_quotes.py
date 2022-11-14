from .context import daily

import unittest


class QuotesTestSuite(unittest.TestCase):

    quotes = daily.Quotes('https://www.goodreads.com/author/quotes/2622245.Lao_Tzu', 'Lao Tzu')

    def test_get_pages_count(self):
        self.assertIsNotNone(self.quotes.get_pages_count())
    
    #@unittest.skip
    def test_log_quotes(self):
        self.assertIsNone(self.quotes.log_quotes())

    def test_get_quote(self):
        self.assertIsNotNone(self.quotes.get_quote())


if __name__ == '__main__':
    unittest.main()
